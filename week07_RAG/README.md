# W7 RAG 入门

## 准备

```powershell
ollama pull nomic-embed-text
pip install langchain langchain-community langchain-chroma langchain-ollama chromadb langchain-text-splitters
```

语料：`data/等级标准节选.txt`（仓库根目录 `data/`）

## 运行

```powershell
cd week07_RAG
python rag_qa.py "HSK4 需要掌握多少词汇？"
python rag_qa.py --rebuild "HSK4 需要掌握多少词汇？"   # 换文本后重建
```

换语料后务必 `--rebuild`，否则仍用旧 `chroma_db`。

## 交付

- `rag_qa.py`：加载→分块→向量化→检索→生成（复用 `llm.ask`）
- `hallucination_log.md`：幻觉对照 ≥5 组
