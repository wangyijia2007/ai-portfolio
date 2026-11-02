# W7 RAG 学科知识库问答器
# 依赖：pip install langchain langchain-community langchain-chroma langchain-ollama chromadb langchain-text-splitters
# 准备：ollama pull nomic-embed-text
#
# 【作业1 进阶】给每段记来源，答案附出处：
# split 时写入 metadata["source_title"]；rag_qa 返回答案后追加【出处】列表。
# 理由：教学问答要可核对，出处比多轮追问更贴合本周“幻觉对照”目标。
import os
import sys

# 机房代理常劫持 localhost；嵌入请求必须直连本机 Ollama
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1,::1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1,::1")
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  数据路径 + 加载 .env

weekpath.load_env()

from langchain_community.document_loaders import TextLoader  # noqa: E402
from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: E402
from langchain_ollama import OllamaEmbeddings  # noqa: E402
from langchain_chroma import Chroma  # noqa: E402

CORPUS = weekpath.data_path("等级标准节选.txt")  # 不再依赖当前工作目录
PERSIST = weekpath.root_path("chroma_db")  # .gitignore 已排除
OLLAMA_BASE = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

_retriever = None


def _title_for_chunk(text):
    """用段首分隔标题作为来源标记，便于答案附出处。"""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("======="):
            return line.strip("= ").strip() or "等级标准节选"
    first = text.strip().splitlines()[0] if text.strip() else "等级标准节选"
    return first[:40]


def get_retriever(k=3, rebuild=False):
    """延迟构建：import 本模块不会触发 embedding；已有 chroma_db 则复用。"""
    global _retriever
    if rebuild:
        _retriever = None
    if _retriever is not None and not rebuild:
        return _retriever
    emb = OllamaEmbeddings(
        model="nomic-embed-text", base_url=OLLAMA_BASE
    )  # 本地嵌入，数据不出本机
    if not rebuild and os.path.exists(PERSIST) and os.listdir(PERSIST):
        vs = Chroma(persist_directory=PERSIST, embedding_function=emb)
    else:
        docs = TextLoader(CORPUS, encoding="utf-8").load()
        splits = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        ).split_documents(docs)
        for sp in splits:
            sp.metadata["source_title"] = _title_for_chunk(sp.page_content)
            sp.metadata.setdefault("source", os.path.basename(CORPUS))
        vs = Chroma.from_documents(splits, emb, persist_directory=PERSIST)
    _retriever = vs.as_retriever(search_kwargs={"k": k})
    return _retriever


def retrieve_docs(question, k=3, rebuild=False):
    return get_retriever(k=k, rebuild=rebuild).invoke(question)


def retrieve(question, k=3, rebuild=False):
    return "\n".join(d.page_content for d in retrieve_docs(question, k=k, rebuild=rebuild))


def build_prompt(question, ctx):
    return (
        "根据以下资料回答问题，资料中没有的内容就如实说“资料中未提及”：\n"
        "%s\n\n问题：%s" % (ctx, question)
    )


def rag_qa(question, prefer="local", k=3, rebuild=False):
    """检索 + 生成；复用 W6 llm.ask。返回 (answer, ctx, sources)。"""
    from llm import LLM

    docs = retrieve_docs(question, k=k, rebuild=rebuild)
    ctx = "\n".join(d.page_content for d in docs)
    sources = []
    for d in docs:
        title = d.metadata.get("source_title") or d.metadata.get("source") or "未知"
        if title not in sources:
            sources.append(title)
    llm = LLM()
    answer = llm.ask(build_prompt(question, ctx), prefer=prefer)
    if sources:
        answer = answer.rstrip() + "\n\n【出处】" + "；".join(sources)
    return answer, ctx, sources


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "HSK4 需要掌握多少词汇？"
    prefer = "local"
    if "--api" in sys.argv:
        prefer = "api"
        sys.argv.remove("--api")
        q = " ".join(a for a in sys.argv[1:] if a) or q
    rebuild = "--rebuild" in sys.argv
    if rebuild:
        sys.argv = [a for a in sys.argv if a != "--rebuild"]
        q = " ".join(sys.argv[1:]) or q

    ans, ctx, sources = rag_qa(q, prefer=prefer, rebuild=rebuild)
    print("【检索片段】\n", ctx[:400], "\n---")
    print("【出处】", sources)
    print(ans)
