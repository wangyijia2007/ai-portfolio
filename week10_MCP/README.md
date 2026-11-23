# W10 MCP · HSK 工具服务端

## 怎么跑

```powershell
python -m pip install "mcp[cli]"
cd week10_MCP
python demo_client.py          # 发现工具 + 调用证据
# 或单独起服务端（会挂起等待）：
python hsk_mcp_server.py
```

## 两个工具

| 工具 | 输入 | 输出示例 |
|------|------|----------|
| `hsk_level` | `word: str` | `把 -> 3 级` |
| `list_by_level` | `level: str` | `把、决定` / `该等级暂无词汇` |

## 离场交付

- `hsk_mcp_server.py`
- `demo_client.py`
- `mcp_practice.md`（配置 + 调用证据 + 三者辨析）
