# 官方 RAG 流水线 ↔ 我的代码（5 行映射表）

> 对照：LangChain 官方 2-Step RAG；中文参考 Datawhale llm-universe C3/C4（只读思路，不复制其代码）。  
> 我的实现：`week07_RAG/rag_qa.py` + `week08_助手v1.0/assistant_v1.py`

| # | 官方流水线 | llm-universe | 我的代码 |
|---|------------|--------------|----------|
| 1 | Load + Split 加载与分块 | C3 数据处理：读取、清洗与切片 | `TextLoader` + `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`，语料 `data/等级标准节选.txt` |
| 2 | Embed + Store 向量化入库 | C3 词向量及向量知识库 | `OllamaEmbeddings(nomic-embed-text)` + `Chroma` 持久化到 `chroma_db/`（本地，数据不出机） |
| 3 | Retrieve 检索 | C4 检索问答链 | `retrieve(question)` 取 top-k；`assistant_v1.answer(use_rag=True)` 时先检索 |
| 4 | Prompt + Generate 拼词与生成 | C4 将 LLM 接入 LangChain | `SYSTEM_HINT` + `build_prompt(question, ctx)` → `LLM().ask(prefer=...)` |
| 5 | Deploy + Evaluate 部署与评估 | C4/C5 部署与评估 | 本周 `assistant_v1.py` 演示 + W7 `hallucination_log.md` 作朴素评估；正式 UI 留给后续周 |

**可迁移点（读懂即可）：** 组件可替换（embeddings/语料）；统一模型入口（`prefer`）；评估闭环（裸答 vs RAG）。
