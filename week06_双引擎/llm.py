# W6 双引擎封装 —— 此后所有周统一经此调用
# 依赖：pip install openai requests python-dotenv
#
# 【作业1 增强项】调用耗时与费用估算打印（三选一选此项）
# 理由：W4 已有 token/费用估算习惯，封装进统一入口后，
# 本地/云端切换时能立刻看出「谁在答、花了多久、大概多少钱」，
# 方便写边界测试记录；多轮记忆留给 W8 助手更合适，重试可后续再加。
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  跨周导入 + 加载 .env

weekpath.load_env()

import requests  # noqa: E402
import openai  # noqa: E402

# DeepSeek 公开标价会变动；仅作课堂费用估算（元 / 百万 tokens）
_INPUT_PRICE_PER_M = 1.0
_OUTPUT_PRICE_PER_M = 2.0


class LocalEngine:
    """本地引擎（Ollama）：隐私任务优先、断网可用。"""

    def __init__(self, model=None):
        self.model = model or os.getenv("LOCAL_MODEL", "qwen2.5:0.5b")
        self.last_meta = {}

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        # 机房代理常把 localhost 也劫持；与 W5 笔记一致关掉环境代理
        session = requests.Session()
        session.trust_env = False
        t0 = time.time()
        r = session.post(
            "http://localhost:11434/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "options": {"temperature": temperature, "num_predict": max_tokens},
                "stream": False,
            },
            timeout=60,
        )
        r.raise_for_status()
        content = r.json()["message"]["content"]
        elapsed = time.time() - t0
        self.last_meta = {
            "engine": "local",
            "model": self.model,
            "elapsed_sec": round(elapsed, 2),
            "cost_cny": 0.0,
        }
        print(
            "[耗时] local/%s %.2fs | 费用 ¥0（本地不计费）"
            % (self.model, elapsed)
        )
        return content


class APIEngine:
    """云端引擎：复杂任务、本地失败兜底。

    注意：openai.OpenAI(...) 在 api_key 为 None 时会直接抛错。
    因此改为**按需创建**：第一次真正调用云端时才建客户端。
    """

    def __init__(self, base_url=None, model=None):
        self.base_url = base_url or "https://api.deepseek.com/v1"
        self.model = model or "deepseek-chat"
        self._client = None
        self.last_meta = {}

    def _get_client(self):
        if self._client is None:
            key = os.getenv("DEEPSEEK_API_KEY")
            if not key:
                raise RuntimeError(
                    "未配置 DEEPSEEK_API_KEY：请复制 .env.example 为 .env 并填入密钥，"
                    "或在系统环境变量中设置。纯本地模式请调用 ask(..., prefer='local')。"
                )
            self._client = openai.OpenAI(
                base_url=self.base_url, api_key=key, timeout=60.0
            )
        return self._client

    def ask(self, prompt, temperature=0.7, max_tokens=800):
        t0 = time.time()
        r = self._get_client().chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        elapsed = time.time() - t0
        usage = r.usage
        prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
        completion_tokens = getattr(usage, "completion_tokens", 0) or 0
        cost = (
            prompt_tokens * _INPUT_PRICE_PER_M
            + completion_tokens * _OUTPUT_PRICE_PER_M
        ) / 1_000_000
        self.last_meta = {
            "engine": "api",
            "model": self.model,
            "elapsed_sec": round(elapsed, 2),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_cny": round(cost, 6),
        }
        print(
            "[耗时] api/%s %.2fs | tokens %s+%s | 估算 ¥%.6f"
            % (self.model, elapsed, prompt_tokens, completion_tokens, cost)
        )
        return r.choices[0].message.content


class LLM:
    """统一入口：ask(prompt)。本地优先、云端兜底、**双向**异常自动切换。

    prefer='local'：本地挂了自动切云端；
    prefer='api'  ：云端挂了（断网/超时/未配密钥）自动切本地。
    """

    def __init__(self, local_model=None):
        self.local = LocalEngine(local_model)
        self.api = APIEngine()
        self.last_engine = None
        self.last_meta = {}

    def ask(self, prompt, prefer="local", **kw):
        if prefer == "local":
            first, second, tag = self.local, self.api, "本地失败，自动切换云端"
            first_name, second_name = "local", "api"
        else:
            first, second, tag = self.api, self.local, "云端失败，自动切换本地"
            first_name, second_name = "api", "local"
        try:
            ans = first.ask(prompt, **kw)
            self.last_engine = first_name
            self.last_meta = dict(first.last_meta)
            return ans
        except Exception as e:
            # 纪律：不吞异常、打印切换原因、返回真实结果（禁止空串 / 禁止 pass）
            print("[%s] %s" % (tag, e))
            try:
                ans = second.ask(prompt, **kw)
            except Exception as e2:
                print("[回退引擎也失败] %s" % e2)
                raise
            self.last_engine = second_name
            self.last_meta = dict(second.last_meta)
            self.last_meta["fallback_from"] = first_name
            return ans


if __name__ == "__main__":
    llm = LLM()
    print(llm.ask("用一句话说明什么是把字句", prefer="local"))
