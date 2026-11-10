# 第 8 周互评表（peer_review）

- **评阅人**：王一嘉（f25210117）
- **指定评阅对象**：陈彦妃
- **对象仓库**：github:echo921201/AI-portfolio  
  完整网址：https://github.com/echo921201/AI-portfolio
- **评阅依据**：《第8周指定互评分配表_20261109》；讲义四维度只描述现象、不打分
- **复现环境**：Windows 10、本机已有 Python / Ollama（`qwen2.5:0.5b`、`nomic-embed-text`）
- **复现时间**：2026-11-10

---

## ① 能不能跑

**步骤：**

1. 用 GitHub API 拉取远端 `main`（含 `week8/`、`week06_双引擎/`、`week07_RAG/`、`data/`、`weekpath.py`）。
2. 按 README「怎么用」进入 `week8/课堂作业`，执行：`python assistant_v1.py`。

**现象：**

- 脚本能启动，三个问题都有回答，过程中**没有**抛出未捕获异常；每题后打印分隔线，与入口里的三问列表一致。
- 本机实测摘要（原样要点）：
  - 「把字句的教学难点有哪些」→ 给出语言结构、语义、语法点等若干条（偏泛）。
  - 「HSK4 词汇量要求是多少」→ 答成「HSK4的词汇量要求是8个。」（数字与常见等级标准不一致）。
  - 「《愚公移山》可以设计什么课堂活动」→ 列出角色扮演、小组讨论、辩论等活动条目。
- 对象自带的 `week8/课堂作业/answer_log.md` 也记录了三问结果与点评；其中写「跑法：进 week8 目录」，与同目录 README 写的「在本目录（week8/课堂作业）运行」**路径表述不一致**（按 README 进「课堂作业」可以跑通）。

---

## ② README 能复现吗

**步骤：** 打开 `week8/课堂作业/README.md`，按四段式逐步对照安装与运行说明。

**现象：**

- README 具备「功能 / 怎么装 / 怎么用 / 已知问题」四段。
- 「怎么装」写明：`pip install -r requirements.txt`、拉取 `qwen2.5:0.5b` 与 `nomic-embed-text`、可选复制 `.env.example`；仓库根目录可见 `.env.example`。
- 「怎么用」写明在 `week8/课堂作业` 运行 `python assistant_v1.py`；本机按此路径**跑通**。
- `requirements.txt` 与 README 同目录；本机依赖此前已具备，未因缺包装失败。本次未从零重装全套依赖，也未配置 DeepSeek 密钥（全程本地）。
- 同 README 提到的 `week8/课后作业/compare_rag.py`、`rag_mapping.md` 在远端均存在。

---

## ③ Release 发了吗

**步骤：** 查询仓库 Releases 与 Tags。

**现象：**

- 存在 tag **`v1.0`**。
- 存在正式 Release：**「学科智能问答助手 v1.0」**（非 draft）。
- Release 正文写明了本周文件路径（`assistant_v1.py`、`answer_log.md`、`compare_rag.py`、`rag_mapping.md`）、用法（进 `week8/课堂作业` 运行）与安装提示（`pip install -r week8/课堂作业/requirements.txt`）。功能 / 安装 / 用法在 Release 页有对应文字。

---

## ④ 有没有已知限制

**步骤：** 阅读 README「已知问题」栏目。

**现象：**

- README **写了**「已知问题」，例如：知识库只有等级标准节选、库外问题会「资料中未提及」或自编；0.5b 对资料利用不稳、HSK4 数字曾答偏；首次加载可能超时、Ollama 未启动会失败。
- 本机跑出的 HSK4「8 个」这类偏离，与其「已知问题」里写的小模型不稳、数字不准，方向一致（现象可对照）。

---

## 附件：对照路径一览（现象）

| 讲义期望 | 对象仓库实际路径 |
|----------|------------------|
| 助手入口 | `week8/课堂作业/assistant_v1.py`（目录名 `week8`，非 `week08_助手v1.0`） |
| README / requirements / answer_log | 同在 `week8/课堂作业/` |
| Release / tag | `v1.0` 已发布 |
