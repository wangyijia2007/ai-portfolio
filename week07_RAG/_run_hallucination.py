# -*- coding: utf-8 -*-
"""跑裸答 vs RAG，输出到 hallucination_raw.txt 再整理进 md。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath

weekpath.load_env()

from llm import LLM
from rag_qa import rag_qa, retrieve

QUESTIONS = [
    "HSK4 需要掌握多少词汇？",
    "旧版 HSK3 要求掌握约多少个词语？",
    "《等级标准》中等四级词汇累计约多少？",
    "把字句教学难点有几个？分别是什么？",
    "本课最小对立对是哪两个词？纠正口令有几条？",
]

OUT = os.path.join(os.path.dirname(__file__), "hallucination_raw.txt")


def main():
    llm = LLM()
    lines = []
    # 强制重建向量库
    print("=== rebuild retriever ===")
    _ = retrieve(QUESTIONS[0], rebuild=True)
    print("rebuild ok, snippet:\n", _[:200])

    for i, q in enumerate(QUESTIONS, 1):
        print("\n==== Q%d" % i, q)
        bare = llm.ask(q, prefer="local")
        print("BARE:", bare[:180].replace("\n", " "))
        rag_ans, ctx, sources = rag_qa(q, prefer="local")
        print("RAG:", rag_ans[:220].replace("\n", " "))
        print("CTX_HEAD:", ctx[:160].replace("\n", " | "))
        lines.append("=" * 60)
        lines.append("Q%d: %s" % (i, q))
        lines.append("---BARE---")
        lines.append(bare)
        lines.append("---CTX---")
        lines.append(ctx[:500])
        lines.append("---RAG---")
        lines.append(rag_ans)
        lines.append("---SOURCES---")
        lines.append("; ".join(sources))

    # 可选：云端裸答对比（无密钥则记录失败信息）
    q0 = QUESTIONS[0]
    lines.append("=" * 60)
    lines.append("EXTRA: bare prefer=api for Q1")
    try:
        api_bare = llm.ask(q0, prefer="api")
        lines.append(api_bare)
        print("API_BARE:", api_bare[:180].replace("\n", " "))
    except Exception as e:
        lines.append("[api bare failed] %s" % e)
        print("API_BARE failed:", e)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
