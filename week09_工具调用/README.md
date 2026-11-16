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
python tool_agent.py "评估愚公移山对 HSK4 的难度"
python tool_agent.py --demo   # 3 条轨迹 + AST 拒绝 → call_trace.md
```

## 四个工具

| 工具 | 输入 | 输出 |
|------|------|------|
| `get_time` | 无 | 当前时间 |
| `calc` | 算式字符串 | 结果（白名单 AST，禁裸 eval） |
| `hsk_level` | 生词 | HSK 等级（查 `data/生词表.csv`） |
| `text_difficulty` | 课文或别名「愚公移山」+ 目标等级 | 覆盖率、达标词、超纲词 JSON |

## 交付清单

**当堂**

- `tool_agent.py`、`call_trace.md`

**课后**

- `failure_case.md`（作业 1 · 失败会诊）
- `tool4_text_difficulty.md`（作业 2 · 第 4 工具说明）
- `w10_preview.md`（作业 3 · 三者辨析）
- `smolagents_map.md`（作业 4 · C 路径 5 行映射 + 反思）
