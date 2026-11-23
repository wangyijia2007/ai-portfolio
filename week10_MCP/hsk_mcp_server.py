# W10 MCP 服务端（与讲义骨架一致）
# 运行：在 week10_MCP 目录执行 python hsk_mcp_server.py
# 挂起等待客户端连接 = 成功。兼容 mcp 1.x / 2.x。
from __future__ import annotations

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402

weekpath.load_env()
VOCAB = weekpath.data_path("生词表.csv")

# ---- 版本自适应：1.x FastMCP / 2.x MCPServer ----
try:
    from mcp.server.fastmcp import FastMCP  # mcp 1.x
except ImportError:
    try:
        from mcp.server import MCPServer as FastMCP  # mcp 2.x
    except ImportError:
        raise SystemExit(
            '未找到 MCP 服务端库。请先安装：pip install "mcp[cli]"\n'
            "（若使用 mcp 2.x，本文件会自动改用 MCPServer，无需改代码。）"
        )

mcp = FastMCP("hsk-tools")


def _rows():
    with open(VOCAB, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@mcp.tool()
def hsk_level(word: str) -> str:
    """查询某个词属于 HSK 几级。"""
    for row in _rows():
        if row["词汇"].strip() == str(word).strip():
            return "%s -> %s 级" % (word, row["HSK等级"])
    return "未找到 %s" % word


@mcp.tool()
def list_by_level(level: str) -> str:
    """列出某一 HSK 等级的全部词汇。"""
    out = [row["词汇"] for row in _rows() if row["HSK等级"] == str(level).strip()]
    return "、".join(out) if out else "该等级暂无词汇"


if __name__ == "__main__":
    print("HSK MCP server waiting on stdio …", file=sys.stderr)
    print("Tools: hsk_level / list_by_level", file=sys.stderr)
    mcp.run()
