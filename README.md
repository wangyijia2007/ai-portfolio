# ai-portfolio

汉语国际教育 ·《人工智能在学习环境中的应用与实践》个人作品集（16 周）。

仓库：https://github.com/wangyijia2007/ai-portfolio

## W1–W4 交付索引

| 周次 | 交付物 |
|------|--------|
| W1 | `hello.py`、`ai任务单.md`、`README.md` |
| W2 | `prompt-library/`（6 个模板 + `prompt_iteration_log.md`） |
| W3 | `week03_Python/vocab_tool.py`、`练习.txt`、`week03_Python/AI辅助编程实录.md` |
| W4 | `week04_API/week4_api_bot.py`、`chat_log.txt`、`week04_API/密钥安全自查表.md` |
| W5 | `week05_本地部署/ollama_notes.md`（安装步骤、选型理由、本地 vs 云端 ≥5 题对比） |

## 快速运行

```bash
python hello.py
python week03_Python/vocab_tool.py
# 配置 .env 中的 DEEPSEEK_API_KEY 后：
python week04_API/week4_api_bot.py "把字句的教学难点有哪些"
```

## 安全

密钥只写在本地 `.env`，绝不提交。模板见 `.env.example`。
