# 第 8 周互评表（peer_review）

- **评阅人**：王一嘉（f25210117）
- **指定评阅对象**：陈心怡（更新版分配表；原对象陈彦妃已更换）
- **对象仓库**：github:cxy94/ai-portfolio  
  完整网址：https://github.com/cxy94/ai-portfolio
- **评阅依据**：《第8周指定互评分配表_（更新版）》；讲义四维度只描述现象、不打分
- **复现环境**：Windows、本机已有 Python / Ollama（`qwen2.5:0.5b`、`nomic-embed-text`）
- **复现时间**：2026-11-11（①②④）；**③ 于 2026-11-12 复查更新**（对象已补发 Release）

---

## ① 能不能跑

**步骤：**

1. 拉取远端 `main` 中 `week08_assistant_v1/` 及依赖周次代码、`data/`、`weekpath.py`。
2. 按 README「怎么用」在**仓库根目录**执行：  
   `python week08_assistant_v1/assistant_v1.py --demo`

**现象：**

- 若在 `week08_assistant_v1/` 目录下直接跑 `python assistant_v1.py`（不带问题、不用 `--demo`），会提示「没有输入问题」并进入 `问题>` 交互；按 README 回仓库根目录用 `--demo` 后可跑通。
- `--demo` 能启动：首次会建 `chroma_db/`（本机约数十秒），三问均有回答，未见未捕获崩溃。
- 本机实测要点（原样摘要）：
  - 「把字句的教学难点…」→ 给出词汇量/语法点/语境等条目与讲授方法；检索命中多段；提示「本次答案未标出处」。
  - 「HSK 4 级累计需要掌握多少词汇、多少汉字？」→ 答「资料中未提及。」（RAG 开着仍如此）。
  - 「《愚公移山》可以设计什么课堂活动？」→ 提到分角色朗读、辩论、成语接龙等。
  - 同一 HSK4 题 `--no-rag` 对照：裸答给出「词汇量约 2000、汉字约 1000」一类数字。
- 对象仓库另有 `answer_log.md` 作为其三问证据文件。

---

## ② README 能复现吗

**步骤：** 阅读 `week08_assistant_v1/README.md`，按「怎么装 / 怎么用」操作。

**现象：**

- README 含「功能 / 怎么装 / 怎么用 / 已知问题」四段；另附流水线映射与目录说明。
- 「怎么装」写明：`pip install -r week08_assistant_v1/requirements.txt`、拉取两个 Ollama 模型、可选 `.env`；仓库根有 `.env.example`。
- 「怎么用」明确要求在**仓库根目录**调用 `python week08_assistant_v1/assistant_v1.py ...`，并给出单问、`--no-rag`、`--demo` 三条命令；本机按第③条 `--demo` **复现成功**。
- 同目录有 `requirements.txt`；本机依赖此前已具备，未从零重装，也未配云端密钥（全程 local）。

---

## ③ Release 发了吗

**步骤：** 查 Tags 与 Releases API（11-11 初评时无 Release 页；**11-12 复查**）。

**现象（更新后）：**

- 远端仍有 git 标签 **`v1.0`**。
- 现已发布正式 Release（非 draft）：标题「v1.0 学科智能问答助手」。  
  页面：https://github.com/cxy94/ai-portfolio/releases/tag/v1.0
- Release 正文含「功能」等说明，并指向 `week08_assistant_v1/answer_log.md` 等路径；可从网页端打开核对。
- 说明：11-11 初评时 Releases 列表为 0（仅有 tag、无网页 Release）；对象补发后本条已按最新远端现象改写。

---

## ④ 有没有已知限制

**步骤：** 阅读 README「已知问题」。

**现象：**

- README **写了**「已知问题」，例如：首次建库慢、Ollama 未启动会失败、0.5b 常漏标出处、数字校验管不住语义幻觉等。
- 本机演示中「未标出处」、HSK4 题 RAG 下答「资料中未提及」，可与其自述的小模型/出处限制对照（只记现象，不评价好坏）。
