# -*- coding: utf-8 -*-
"""本机跑边界测试，输出写入 stdout，再整理进 week06_test_log.md。"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath

weekpath.load_env()

from llm import LLM, LocalEngine  # noqa: E402


PROMPT = "用一句话说明什么是把字句"


def run(label, fn):
    print("\n" + "=" * 60)
    print("TEST:", label)
    print("=" * 60)
    t0 = time.time()
    try:
        ans = fn()
        print("ANSWER:", (ans or "")[:200].replace("\n", " "))
        print("TOTAL_WALL_SEC:", round(time.time() - t0, 2))
    except Exception as e:
        print("CRASH:", type(e).__name__, e)
        print("TOTAL_WALL_SEC:", round(time.time() - t0, 2))


def main():
    llm = LLM()

    # 1 正常本地
    run("1 正常本地 prefer=local", lambda: llm.ask(PROMPT, prefer="local"))
    print("last_engine:", llm.last_engine, llm.last_meta)

    # 2 本地挂 → 切云端（把本地地址指到死端口模拟关掉 Ollama）
    real_ask = LocalEngine.ask

    def broken_ask(self, prompt, temperature=0.7, max_tokens=800):
        import requests

        s = requests.Session()
        s.trust_env = False
        r = s.post(
            "http://127.0.0.1:9/api/chat",
            json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "stream": False},
            timeout=3,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]

    LocalEngine.ask = broken_ask
    llm2 = LLM()
    run("2 本地挂 prefer=local（应切云端或再失败）", lambda: llm2.ask(PROMPT, prefer="local"))
    print("last_engine:", llm2.last_engine, getattr(llm2, "last_meta", {}))
    LocalEngine.ask = real_ask

    # 3 prefer=api（无密钥时应切本地）
    llm3 = LLM()
    run("3 prefer=api（无密钥预期切本地）", lambda: llm3.ask(PROMPT, prefer="api"))
    print("last_engine:", llm3.last_engine, llm3.last_meta)

    # 4 max_tokens 调小观察截断
    llm4 = LLM()
    run(
        "4 prefer=local max_tokens=20",
        lambda: llm4.ask("用三句话介绍把字句的教学要点", prefer="local", max_tokens=20),
    )
    print("last_engine:", llm4.last_engine, llm4.last_meta)

    # 5 正常本地再测一道学科题
    llm5 = LLM()
    run(
        "5 prefer=local 学科题《愚公移山》出题",
        lambda: llm5.ask("给《愚公移山》出一道很短的 HSK4 阅读题（题干+两个选项即可）", prefer="local"),
    )
    print("last_engine:", llm5.last_engine, llm5.last_meta)


if __name__ == "__main__":
    main()
