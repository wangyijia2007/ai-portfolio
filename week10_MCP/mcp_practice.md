# W10 实验 3 · mcp_practice.md（离场交付）

> 仓库：`wangyijia2007/ai-portfolio`  
> 目录：`week10_MCP/`  
> 环境：Windows · Python 3.13 · mcp 2.x（`MCPServer`）

---

## 一、配置记录

### 1. 依赖

```powershell
python -m pip install "mcp[cli]"
python -c "from mcp.server import MCPServer; print('mcp 2.x 路径 OK')"
```

本机验证输出：`mcp 2.x 路径 OK`

### 2. 服务端启动方式

```powershell
cd week10_MCP
python hsk_mcp_server.py
```

挂起等待客户端连接 = 成功（stdio）。stderr 可见：

```text
HSK MCP server waiting on stdio …
Tools: hsk_level / list_by_level
```

### 3. 客户端配置原文（最小客户端 / 桌面客户端通用）

本机用讲义最小客户端 `demo_client.py`（把服务端当子进程拉起）：

```python
params = StdioServerParameters(
    command=sys.executable,
    args=[r"…/week10_MCP/hsk_mcp_server.py"],
    cwd=r"…/week10_MCP",
)
```

若粘贴到支持 MCP 的桌面客户端，配置 JSON 为：

```json
{
  "mcpServers": {
    "hsk-tools": {
      "command": "python",
      "args": ["D:/workspace/ai-portfolio/week10_MCP/hsk_mcp_server.py"]
    }
  }
}
```

（路径按本机作品集根目录调整；勿把 `.env` 写进配置。）

---

## 二、调用证据（发现 → 调用）

运行：`python demo_client.py`（目录：`week10_MCP/`）

### 1. 工具列表（发现）

```text
工具列表: ['hsk_level', 'list_by_level']
```

### 2. 调用返回

```text
hsk_level('把'): 把 -> 3 级
list_by_level('3'): 把、决定
list_by_level('1'): 该等级暂无词汇
```

说明：生词表中无 HSK 1 级词，返回「该等级暂无词汇」符合讲义口径，属正确行为。

---

## 三、三者辨析（各一句话）

| 概念 | 哪一侧 | 解决什么 |
|------|--------|----------|
| **Function Calling** | 模型侧 | 模型怎么「点名」要调哪个工具、带什么参数 |
| **MCP** | 工具侧 | 工具怎么被统一发现和调用（协议） |
| **普通 API 调用** | 程序侧 | 代码怎么直接请求一个服务（无「模型现场决定」） |

课程对应：W9 `tool_agent.py` ≈ Function Calling；W10 `hsk_mcp_server.py` ≈ MCP；W4 调 DeepSeek ≈ 普通 API。

---

## 四、离场自查

- [x] mcp 库装好，服务端能启动（挂起等待）
- [x] 客户端列出 `hsk_level` / `list_by_level`
- [x] `hsk_level("把")` → `把 -> 3 级`；`list_by_level` 可按等级查询
- [x] 本文三样齐全：配置 / 调用证据 / 三者辨析
- [x] 无 `.env` 入仓；commit + push
