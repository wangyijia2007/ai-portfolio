# W9 工具调用 · tool_agent.py

手写最小 Function Calling 循环（不用框架）：模型只输出「调哪个工具 + 参数」，Python 执行后再回喂作答。

## 怎么装

```powershell
pip install openai python-dotenv
```

密钥：在仓库根目录把 `.env.example` 复制为 `.env`，填 `DEEPSEEK_API_KEY`（**勿提交 .env**）。

纯本地 Ollama 也可：

```powershell
$env:DEEPSEEK_BASE_URL="http://127.0.0.1:11434/v1"
$env:DEEPSEEK_API_KEY="ollama"
$env:DEEPSEEK_MODEL="qwen2.5:0.5b"
```

## 怎么用

```powershell
cd week09_工具调用
python tool_agent.py
python tool_agent.py "帮我算一下 35*24 等于多少"
python tool_agent.py --demo   # 跑 3 条轨迹 + AST 拒绝记录 → call_trace.md
```

## 三个工具

| 工具 | 输入 | 输出 |
|------|------|------|
| `get_time` | 无 | 当前时间 |
| `calc` | 算式字符串 | 结果（白名单 AST，禁裸 eval） |
| `hsk_level` | 生词 | HSK 等级（查 `data/生词表.csv`） |

## 当堂交付

- `tool_agent.py`（可运行，3 工具）
- `call_trace.md`（≥3 条：问句 / 模型输出 / 工具返回 / 最终回答；含 AST 越权拒绝）
