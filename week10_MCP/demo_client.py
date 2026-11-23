# W10 最小客户端：发现工具 → 调用工具（讲义第五节）
# 用法：在 week10_MCP 目录执行 python demo_client.py
from __future__ import annotations

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(HERE, "hsk_mcp_server.py")


async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER],
        cwd=HERE,
    )
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()  # 第一步：发现
            names = [t.name for t in tools.tools]
            print("工具列表:", names)

            res = await s.call_tool("hsk_level", {"word": "把"})  # 第二步：调用
            text = res.content[0].text if res.content else str(res)
            print("hsk_level('把'):", text)

            res2 = await s.call_tool("list_by_level", {"level": "3"})
            text2 = res2.content[0].text if res2.content else str(res2)
            print("list_by_level('3'):", text2)

            res3 = await s.call_tool("list_by_level", {"level": "1"})
            text3 = res3.content[0].text if res3.content else str(res3)
            print("list_by_level('1'):", text3)

            res4 = await s.call_tool("count_by_level", {"level": "4"})
            text4 = res4.content[0].text if res4.content else str(res4)
            print("count_by_level('4'):", text4)


if __name__ == "__main__":
    asyncio.run(main())
