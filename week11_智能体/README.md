# week11_智能体（第十次课课后作业 4 · 预习验收）

## 文件

| 文件 | 说明 |
|------|------|
| `planner_agent.py` | 讲义骨架：Plan-then-Execute 备课智能体 |
| `planner_run_log.txt` | 本机运行输出（证据） |

## 运行

```powershell
cd week11_智能体
python planner_agent.py
# 本地较慢时可：python planner_agent.py --cloud
```

默认课题：《愚公移山》，拆成 4 步：定教学要点 / 写教学目标 / 出教案框架 / 配 3 道练习。

## 本机证据

- 引擎：本地 Ollama `qwen2.5:0.5b` + W7 `retrieve`
- 完整 stdout：见 `planner_run_log.txt`
- 0.5b 步骤文本可能偏短或跑题，属模型能力限制；流程（先规划再逐步执行）已跑通
