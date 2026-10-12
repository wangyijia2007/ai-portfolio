# 一键跑完第 4 周课堂实验：3 个学科问题 + 参数对比
# 运行：python week04_API/run_w04_demo.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath

weekpath.load_env()

from week4_api_bot import ask, append_log, estimate_cost_cny  # noqa: E402


QUESTIONS = [
    "把字句的教学难点有哪些",
    "HSK4 级对词汇量的要求是多少",
    "给一篇中级汉语作文写三段式评语：学生写了一次迟到的经历，用了因为……所以……，约 80 字",
]

PARAM_PROMPTS = [
    ("用一句话说明什么是把字句", 0.0, 15),
    ("用一句话说明什么是把字句", 1.5, 60),
    ("用一句话说明什么是把字句", 0.0, 800),
]


def main():
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：未设置 DEEPSEEK_API_KEY。请先配置 .env")
        sys.exit(1)

    print("=== 第 2 步：3 个学科问题 ===")
    for q in QUESTIONS:
        print("\nQ:", q)
        ans, usage = ask(q)
        print(ans)
        print(
            "[用量]",
            usage["prompt_tokens"],
            "+",
            usage["completion_tokens"],
            "tokens,",
            usage["elapsed_sec"],
            "s, ~¥%.6f" % estimate_cost_cny(usage),
        )
        append_log(q, ans, usage)

    print("\n=== 第 3 步：参数体验 ===")
    rows = []
    for q, temperature, max_tokens in PARAM_PROMPTS:
        ans, usage = ask(q, temperature=temperature, max_tokens=max_tokens)
        print("\nT=%.1f max_tokens=%d -> %s" % (temperature, max_tokens, ans))
        append_log(
            "%s [T=%.1f max_tokens=%d]" % (q, temperature, max_tokens),
            ans,
            usage,
        )
        rows.append((temperature, max_tokens, ans.replace("\n", " "), usage))

    note = weekpath.root_path("week04_API", "参数体验记录.md")
    with open(note, "w", encoding="utf-8") as f:
        f.write("# W4 参数体验记录\n\n")
        f.write("| 参数 | 你填的值 | 观察到的现象 |\n")
        f.write("| --- | --- | --- |\n")
        for temperature, max_tokens, ans, usage in rows:
            preview = ans[:80] + ("…" if len(ans) > 80 else "")
            f.write(
                "| temperature=%.1f, max_tokens=%d | 实测 | 耗时 %.2fs；输出：%s |\n"
                % (temperature, max_tokens, usage["elapsed_sec"], preview)
            )
        f.write("\n## 结论\n\n")
        f.write("- temperature 越低，输出越稳、越短；越高越发散。\n")
        f.write("- max_tokens 过小会硬截断成半句；调大后才能说完整。\n")
        f.write("- 费用按 token 计：本次日志 `chat_log.txt` 中有每次用量。\n")
    print("\n已写入：", note)
    print("日志：", weekpath.root_path("chat_log.txt"))


if __name__ == "__main__":
    main()
