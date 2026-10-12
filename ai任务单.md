# AI 任务单

记录使用 AI 对话工具完成学科任务的过程与结果。

## 任务 1：创建个人作品集仓库

### 任务目标

在 GitHub 上创建名为 `ai-portfolio` 的个人作品集仓库，并包含基础文件：

- `README.md`
- `hello.py`
- `ai任务单.md`

### 使用的 AI 工具

- Cursor（AI 编程助手）

### 完成过程

1. 向 AI 说明作业要求：提交 GitHub 仓库链接，仓库名为 `ai-portfolio`。
2. 请 AI 协助创建仓库所需的三个基础文件。
3. 在本地完成文件编写后，将仓库推送到 GitHub。
4. 将仓库链接提交到作业平台。

### 结果

- [ ] 已创建 GitHub 仓库 `ai-portfolio`
- [ ] 仓库包含 `README.md`、`hello.py`、`ai任务单.md`
- [ ] 已在 VS Code 中成功运行 `hello.py`
- [ ] 已提交仓库链接完成作业

### 反思

（可在此补充：AI 如何帮助你完成任务、遇到的问题及解决方法）

## 任务 2：第 4 周 API 问答机器人

### 任务目标

完成 `week04_API/week4_api_bot.py`：命令行提问 → 调用大模型 API → 终端打印 → 追加 `chat_log.txt`。

### 使用的 AI 工具

- Cursor（AI 编程助手）
- DeepSeek Chat API（OpenAI 兼容接口）

### 完成过程

1. 按讲义安装 `openai`、`python-dotenv`，复制 `.env.example` 为 `.env` 并填入密钥。
2. 走读骨架：`weekpath.load_env()`、按需 `get_client()`、友好错误提示、日志写根目录。
3. 增强脚本：返回 token 用量与费用估算，补齐超时/断连/鉴权失败提示。
4. 用 `run_w04_demo.py` 跑 3 个学科问题与 temperature / max_tokens 对比，写入参数体验记录。
5. 完成密钥安全自查后 push（确认仓库无 `.env`）。

### 结果

- [ ] `week4_api_bot.py` 能跑通并打印
- [ ] `chat_log.txt` 中有 3 次学科问答（本地文件，不提交）
- [ ] 参数体验记录已填写
- [ ] 密钥安全自查表已打钩，仓库无 `.env`

### 反思

API 与网页聊天的差别在于可程序化：可批量、可嵌进脚本、可留痕、按 token 计费。密钥绝不能写进代码或推进仓库。
