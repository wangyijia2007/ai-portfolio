# 学科智能问答助手 v1.0

把 W2 提示词、W6 双引擎 `llm.py`、W7 知识库 `rag_qa.py` 组装成可演示助手。

## 功能

- 基于 RAG 的学科问答；支持纯对话 / 基于资料两种模式（`use_rag`）。
- 本地 Ollama 优先、云端 DeepSeek 兜底（`prefer=local|api`）。
- 三问演示：把字句难点、HSK4 词汇量、愚公移山课堂活动。

## 怎么装

```powershell
cd D:\workspace\ai-portfolio
pip install -r week08_助手v1.0/requirements.txt
ollama pull qwen2.5:0.5b
ollama pull nomic-embed-text
```

可选：复制根目录 `.env.example` 为 `.env`，填入 `DEEPSEEK_API_KEY`（纯本地可跳过）。

首次 RAG 需已有 `data/等级标准节选.txt`（W7 已入库）；换语料后在 `week07_RAG` 下用 `--rebuild` 重建。

## 怎么用

```powershell
cd D:\workspace\ai-portfolio\week08_助手v1.0
python assistant_v1.py
```

代码里调用示例：

```python
from assistant_v1 import answer
print(answer("HSK4 词汇量要求是多少", use_rag=True, prefer="local"))
print(answer("你好", use_rag=False, prefer="local"))
```

## 已知问题

- 未启动 Ollama / 未 pull `nomic-embed-text` 时，本地 RAG 会失败；可设 `prefer="api"`（需密钥）或先启动 Ollama。
- 机房代理可能劫持 localhost：脚本依赖 `rag_qa.py` 内已处理的 `NO_PROXY`；仍失败时先清代理再试。
- 小模型 `qwen2.5:0.5b` 生成质量有限，数字类问题务必开 `use_rag=True`。

> 为何要诚实写「已知问题」：见 [`known_issues_why.md`](./known_issues_why.md)（课后作业 2 · 约 200 字）。
