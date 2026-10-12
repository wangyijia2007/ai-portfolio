# W4 命令行学科问答机器人（API 版）
# 依赖：pip install openai python-dotenv
# 运行：python week4_api_bot.py "把字句的教学难点有哪些"
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  加载 .env

weekpath.load_env()

import openai  # noqa: E402

BASE_URL = "https://api.deepseek.com/v1"  # 通义：https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL = "deepseek-chat"  # 通义：qwen-plus

# DeepSeek 官方标价会变动；仅作费用估算参考（元 / 百万 tokens）
INPUT_PRICE_PER_M = 1.0
OUTPUT_PRICE_PER_M = 2.0

_client = None


def get_client():
    """按需创建客户端：这样"没配密钥"能在 __main__ 里被友好提示，
    而不是在 import 阶段就抛出看不懂的 OpenAIError。"""
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY")
        _client = openai.OpenAI(
            base_url=BASE_URL,
            api_key=key,
            timeout=60.0,
        )
    return _client


def ask(question, temperature=0.7, max_tokens=800):
    """返回 (answer, usage_dict)。usage 含 prompt/completion/total tokens 与耗时。"""
    t0 = time.time()
    r = get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    elapsed = time.time() - t0
    usage = {
        "prompt_tokens": getattr(r.usage, "prompt_tokens", 0) or 0,
        "completion_tokens": getattr(r.usage, "completion_tokens", 0) or 0,
        "total_tokens": getattr(r.usage, "total_tokens", 0) or 0,
        "elapsed_sec": round(elapsed, 2),
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    return r.choices[0].message.content, usage


def estimate_cost_cny(usage):
    prompt = usage["prompt_tokens"]
    completion = usage["completion_tokens"]
    return (prompt * INPUT_PRICE_PER_M + completion * OUTPUT_PRICE_PER_M) / 1_000_000


def append_log(question, answer, usage=None):
    path = weekpath.root_path("chat_log.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write("Q: %s\nA: %s\n" % (question, answer))
        if usage:
            cost = estimate_cost_cny(usage)
            f.write(
                "meta: tokens=%s+%s=%s | %.2fs | T=%.2f max_tokens=%s | ~¥%.6f\n"
                % (
                    usage["prompt_tokens"],
                    usage["completion_tokens"],
                    usage["total_tokens"],
                    usage["elapsed_sec"],
                    usage["temperature"],
                    usage["max_tokens"],
                    cost,
                )
            )
        f.write("\n")
    return path


if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：未设置 DEEPSEEK_API_KEY。")
        print("  处理：复制 .env.example 为 .env 并填入密钥，重启终端后重试。")
        sys.exit(1)
    q = " ".join(sys.argv[1:]) or "把字句的教学难点有哪些"
    try:
        ans, usage = ask(q)
    except openai.APITimeoutError:
        print("错误：请求超时，请检查网络或调大 timeout。")
        sys.exit(1)
    except openai.APIConnectionError:
        print("错误：连不上 API 域名，请换网络（如手机热点）或检查 BASE_URL。")
        sys.exit(1)
    except openai.AuthenticationError:
        print("错误：密钥无效（401）。请检查 .env 里的 DEEPSEEK_API_KEY 是否复制正确。")
        sys.exit(1)
    print(ans)
    print(
        "\n[用量] 输入 %d + 输出 %d = %d tokens，耗时 %.2fs，估算约 ¥%.6f"
        % (
            usage["prompt_tokens"],
            usage["completion_tokens"],
            usage["total_tokens"],
            usage["elapsed_sec"],
            estimate_cost_cny(usage),
        )
    )
    log_path = append_log(q, ans, usage)
    print("已追加日志：%s" % log_path)
