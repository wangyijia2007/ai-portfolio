# W10 MCP · HSK 工具服务端

把 W9 里「查等级 / 查时间」做成 MCP 工具，供客户端发现与调用。

## 预习怎么跑

```powershell
# 仓库根目录
python env_check.py
python -m pip install "mcp[cli]"

cd week10_MCP
python hsk_mcp_server.py
# 卡住等待连接 = 成功；Ctrl+C 停止
```

## 工具

- `hsk_level(word: str)` → 查 `data/生词表.csv`
- `get_time()` → 本机时间

参数怎么被客户端知道？→ 类型注解 + docstring（`Args:`）。
