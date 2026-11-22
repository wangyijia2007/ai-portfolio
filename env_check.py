# -*- coding: utf-8 -*-
"""第十周预习 · 环境自检（python env_check.py）"""
from __future__ import annotations

import importlib.util
import os
import sys
import urllib.request


def ok(msg: str):
    print("[OK]", msg)


def bad(msg: str):
    print("[!!]", msg)


def main():
    print("当前解释器:", sys.executable)
    print("版本:", sys.version.split()[0])
    print("-" * 50)

    # openai / dotenv（W9 底子）
    for mod in ("openai", "dotenv"):
        if importlib.util.find_spec(mod):
            ok("%s 已安装" % mod)
        else:
            bad("%s 缺失 → pip install openai python-dotenv" % mod)

    # mcp 1.x / 2.x
    mcp_ok = False
    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401

        ok("mcp 1.x 路径 OK（FastMCP）")
        mcp_ok = True
    except Exception as e1:
        try:
            from mcp.server import MCPServer  # noqa: F401

            ok("mcp 2.x 路径 OK（MCPServer）")
            mcp_ok = True
        except Exception as e2:
            bad("mcp 未就绪：%s / %s" % (e1, e2))
            bad('修复：python -m pip install "mcp[cli]"')

    # 数据与 W9
    root = os.path.dirname(os.path.abspath(__file__))
    vocab = os.path.join(root, "data", "生词表.csv")
    tool = os.path.join(root, "week09_工具调用", "tool_agent.py")
    srv = os.path.join(root, "week10_MCP", "hsk_mcp_server.py")
    if os.path.isfile(vocab):
        ok("生词表.csv 存在")
    else:
        bad("找不到 data/生词表.csv")
    if os.path.isfile(tool):
        ok("W9 tool_agent.py 存在")
    else:
        bad("找不到 week09_工具调用/tool_agent.py")
    if os.path.isfile(srv):
        ok("W10 hsk_mcp_server.py 存在")
    else:
        bad("找不到 week10_MCP/hsk_mcp_server.py")

    # Ollama（可选）
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as r:
            ok("Ollama 服务可访问 (%s)" % r.status)
    except Exception:
        bad("Ollama 服务未检测到（本地模型可选；云端需 .env 密钥）")

    key = os.getenv("DEEPSEEK_API_KEY")
    # also try load .env via weekpath if present
    try:
        sys.path.insert(0, root)
        import weekpath

        weekpath.load_env()
        key = os.getenv("DEEPSEEK_API_KEY") or key
    except Exception:
        pass
    if key:
        ok("DEEPSEEK_API_KEY 已配置（长度 %d）" % len(key))
    else:
        bad("未配置 DEEPSEEK_API_KEY（纯本地可忽略）")

    print("-" * 50)
    if mcp_ok and os.path.isfile(tool) and os.path.isfile(srv):
        print("结论：可运行（预习入场券：mcp + W9 + W10 服务端文件就绪）")
    else:
        print("结论：需修复上述 [!!] 项后再上课")


if __name__ == "__main__":
    main()
