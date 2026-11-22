# W10 MCP 服务端骨架（约 60 行）
# 预习：python hsk_mcp_server.py —— stdio 服务端会「卡住」等待客户端，属成功。
# 兼容 mcp 1.x（FastMCP）与 2.x（MCPServer）。
from __future__ import annotations

import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402

weekpath.load_env()
VOCAB = weekpath.data_path("生词表.csv")

# ---- 版本自适应：1.x FastMCP / 2.x MCPServer ----
try:
    from mcp.server.fastmcp import FastMCP as _Server  # type: ignore

    _VER = "1.x"
except ModuleNotFoundError:
    from mcp.server.mcpserver import MCPServer as _Server  # type: ignore

    _VER = "2.x"

mcp = _Server("hsk-tools")


@mcp.tool()
def hsk_level(word: str) -> str:
    """查课程生词表里词语的 HSK 等级。

    Args:
        word: 要查询的汉字或词语
    """
    with open(VOCAB, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["词汇"].strip() == str(word).strip():
                return "%s 是 %s 级" % (word, row["HSK等级"])
    return "未找到 %s" % word


@mcp.tool()
def get_time() -> str:
    """返回本机当前时间（无参数）。"""
    return str(datetime.datetime.now())


if __name__ == "__main__":
    # 标准输出给 MCP 客户端；提示打到 stderr，避免污染协议流
    print("HSK MCP server starting (%s) … waiting on stdio" % _VER, file=sys.stderr)
    print("Tools: hsk_level(word: str), get_time()", file=sys.stderr)
    print("Ctrl+C to stop. 卡住不退出 = 成功。", file=sys.stderr)
    # 2.x: run(transport='stdio')；1.x FastMCP 同样支持 run()
    try:
        mcp.run(transport="stdio")
    except TypeError:
        mcp.run()
