# W9 手写最小工具调用循环（不用框架）
# 依赖：pip install openai python-dotenv
#
# 当堂交付：3 个工具（get_time / calc / hsk_level）+ 调用轨迹
# 安全：calc 用白名单 AST，绝不裸 eval
import os
import csv
import sys
import ast
import json
import re
import operator
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  数据路径 + 加载 .env

weekpath.load_env()

# 机房代理常劫持 localhost；本地 Ollama 必须直连
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1,::1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1,::1")
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)

import openai  # noqa: E402

VOCAB = weekpath.data_path("生词表.csv")

# 默认走 DeepSeek 云端；本机演示可切 Ollama（OpenAI 兼容）：
#   DEEPSEEK_BASE_URL=http://127.0.0.1:11434/v1
#   DEEPSEEK_API_KEY=ollama
#   DEEPSEEK_MODEL=qwen2.5:0.5b
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

_client = None


def get_client():
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY，请先在 .env 中填写（本地 Ollama 可填 ollama）")
        base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        _client = openai.OpenAI(base_url=base, api_key=key)
    return _client


def get_time():
    return str(datetime.datetime.now())


# ---- 安全计算：白名单 AST，绝不使用裸 eval ----
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("只允许数字与 + - * / ** % 运算")


def calc(expr):
    """教学演示用：只做四则运算。为什么不用 eval？
    因为 eval 会执行任意 Python 代码，是典型的安全反模式（本课程伦理红线之一）。"""
    try:
        return str(_eval_node(ast.parse(str(expr), mode="eval")))
    except ZeroDivisionError:
        return "错误：除数为 0"
    except Exception as e:
        return "拒绝计算：%s" % e


def hsk_level(word):
    with open(VOCAB, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["词汇"].strip() == str(word).strip():
                return "%s 是 %s 级" % (word, row["HSK等级"])
    return "未找到 %s" % word


def _load_vocab():
    with open(VOCAB, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def text_difficulty(text_or_alias, target_level="4"):
    """课文难度评估（作业 2 · 第 4 工具）。

    输入：
      text_or_alias: 课文原文，或别名「愚公移山」加载 data/愚公移山.txt
      target_level: 目标 HSK 等级（如 3 / 4 / \"HSK4\"）
    输出：JSON 字符串，含覆盖率、达标词、超纲词。
    """
    alias = str(text_or_alias).strip()
    if alias in ("愚公移山", "愚公移山.txt", "yugong"):
        path = weekpath.data_path("愚公移山.txt")
        text = open(path, encoding="utf-8").read()
        source = "愚公移山.txt"
    else:
        text = alias
        source = "inline"
    try:
        target = int(re.sub(r"[^0-9]", "", str(target_level)) or "4")
    except ValueError:
        target = 4
    rows = _load_vocab()
    # 长词优先，避免「把」吃掉「把字句」
    words = sorted({r["词汇"].strip(): r for r in rows if r.get("词汇")}.items(),
                   key=lambda x: len(x[0]), reverse=True)
    hits = []
    for w, row in words:
        if w and w in text:
            try:
                lv = int(str(row["HSK等级"]).strip())
            except ValueError:
                continue
            hits.append({"word": w, "level": lv, "gloss": row.get("释义", "")})
    if not hits:
        return json.dumps({
            "source": source, "target_level": target, "matched": 0,
            "coverage": 0.0, "in_level": [], "over_level": [],
            "note": "生词表中没有词出现在该课文里",
        }, ensure_ascii=False)
    in_level = [h for h in hits if h["level"] <= target]
    over_level = [h for h in hits if h["level"] > target]
    coverage = round(len(in_level) / len(hits), 3)
    return json.dumps({
        "source": source,
        "target_level": target,
        "matched": len(hits),
        "coverage": coverage,
        "in_level": ["%s(HSK%d)" % (h["word"], h["level"]) for h in in_level],
        "over_level": ["%s(HSK%d)" % (h["word"], h["level"]) for h in over_level],
    }, ensure_ascii=False)


TOOLS = {
    "get_time": get_time,
    "calc": calc,
    "hsk_level": hsk_level,
    "text_difficulty": text_difficulty,
}

SYS = ("你是国际中文助教。可用工具只有这 4 个："
       "get_time（查当前时间，无参数）、"
       "calc（四则运算，参数必须是完整算式字符串，如 calc('35*24')）、"
       "hsk_level（查生词 HSK 等级，参数必须是词语本身，如 hsk_level('把')）、"
       "text_difficulty（课文难度评估，如 text_difficulty('愚公移山','4')，"
       "返回覆盖率与超纲词）。"
       '如需调用，只输出 JSON，格式：{"tool": "工具名", "args": [参数]}；'
       "只调用问题真正需要的工具，绝不编造不存在的工具名；无需工具时直接回答。"
       "复合问题时可输出多个 JSON 对象。")


def _repair_jsonish(blk):
    """修补小模型常见非法 JSON：裸算式、未加引号参数、单引号、错分号等。"""
    s = (blk or "").strip()
    s = s.replace("'", '"')
    s = s.replace(";}", "}")
    s = re.sub(r',\s*}', "}", s)
    # args: [35*24] / [35 * 24] → args: ["35*24"]
    s = re.sub(
        r'("args"\s*:\s*)\[\s*([0-9]+(?:\s*(?:\*\*|[+\-*/%])\s*[0-9]+)+)\s*\]',
        lambda m: '%s["%s"]' % (m.group(1), re.sub(r"\s+", "", m.group(2))),
        s,
    )
    def _fix_arg(_m):
        prefix, inner = _m.group(1), _m.group(2).strip()
        if inner in ("", '""', "null", "None"):
            return "%s[]" % prefix
        if inner in ("current_time", "now", "time"):
            return "%s[]" % prefix
        if inner.startswith('"') and inner.endswith('"'):
            return "%s[%s]" % (prefix, inner)
        if re.fullmatch(r"-?\d+(?:\.\d+)?", inner):
            return "%s[%s]" % (prefix, inner)
        return '%s["%s"]' % (prefix, inner.strip('"'))
    s = re.sub(r'("args"\s*:\s*)\[([^\]]*)\]', _fix_arg, s)
    return s


def parse_calls(txt):
    """容错解析：剥掉 ```json 围栏与前后客套话，返回全部工具调用（0/1/多个）。"""
    s = (txt or "").strip()
    s = s.replace("```json", "").replace("```", "").strip()
    # 小模型常把两个 JSON 粘成 {...};{...} 或 {...}{...}
    s = s.replace("}{", "}\n{").replace("};{", "}\n{")

    def _load_one(blob):
        for candidate in (blob, _repair_jsonish(blob)):
            try:
                obj = json.loads(candidate)
                if isinstance(obj, dict):
                    return obj
            except Exception:
                continue
        return None

    calls = []
    for blk in re.findall(r"\{[^{}]*\}", s):
        obj = _load_one(blk)
        if obj is not None:
            calls.append(obj)
    if calls:
        return calls
    obj = _load_one(s)
    return [obj] if obj is not None else []


def run(user_msg, max_calls=2, collect_trace=None):
    """工具调用循环。collect_trace 若传入 list，会追加本轮轨迹步骤。"""
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user_msg}]
    trace = collect_trace if collect_trace is not None else []
    for round_i in range(max_calls):
        txt = get_client().chat.completions.create(
            model=MODEL, messages=msgs).choices[0].message.content
        calls = [c for c in parse_calls(txt)
                 if isinstance(c.get("tool"), str) and c.get("tool") in TOOLS]
        # 同名工具去重，保留首次
        seen, uniq = set(), []
        for c in calls:
            if c["tool"] in seen:
                continue
            seen.add(c["tool"])
            uniq.append(c)
        calls = uniq
        trace.append({"round": round_i + 1, "model_output": txt, "parsed_calls": calls})
        if not calls:
            return txt
        results = []
        for call in calls:
            args = call.get("args") or []
            if not isinstance(args, list):
                results.append("工具参数格式错误：%r" % (args,))
                continue
            if call["tool"] == "get_time":
                args = []
            elif call["tool"] == "calc":
                if len(args) >= 2 and all(
                    isinstance(a, (int, float)) or re.fullmatch(r"-?\d+(?:\.\d+)?", str(a))
                    for a in args
                ):
                    # 小模型常把 35*24 拆成 [35, 24]
                    args = ["*".join(str(a) for a in args)]
                elif args:
                    args = [str(args[0])]
                else:
                    args = [""]
            elif call["tool"] == "hsk_level":
                if args and str(args[0]).strip():
                    args = [str(args[0]).strip()]
                else:
                    # 从原问句里抓第一个汉字词作兜底（0.5b 常漏填 args）
                    m = re.search(r"[\u4e00-\u9fff]{1,4}", user_msg)
                    args = [m.group()] if m else [""]
            elif call["tool"] == "text_difficulty":
                if not args:
                    args = ["愚公移山", "4"]
                elif len(args) == 1:
                    args = [str(args[0]), "4"]
                else:
                    args = [str(args[0]), str(args[1])]
            try:
                out = TOOLS[call["tool"]](*args)
                results.append("%s%r → %s" % (call["tool"], args, out))
            except Exception as e:
                results.append("工具执行失败：%s" % e)
        trace[-1]["tool_returns"] = results
        # 拿到工具结果后强制收口：禁止小模型继续刷 JSON
        msgs += [
            {"role": "assistant", "content": txt},
            {"role": "user", "content": (
                "工具返回：%s。\n"
                "请用中文直接回答用户原来的问题；禁止再输出 JSON；禁止再次调用工具。"
            ) % "；".join(results)},
        ]
        final = get_client().chat.completions.create(
            model=MODEL, messages=msgs).choices[0].message.content
        # 若仍吐 JSON，再强制一次纯文本
        if parse_calls(final):
            msgs += [
                {"role": "assistant", "content": final},
                {"role": "user", "content": "不要 JSON。根据上面的工具返回，用一两句中文给出最终答案。"},
            ]
            final = get_client().chat.completions.create(
                model=MODEL, messages=msgs).choices[0].message.content
        trace.append({"round": "final", "model_output": final, "parsed_calls": [], "tool_returns": []})
        return final
    final = get_client().chat.completions.create(
        model=MODEL, messages=msgs).choices[0].message.content
    trace.append({"round": "final", "model_output": final, "parsed_calls": [], "tool_returns": []})
    return final


def _format_trace(idx, question, steps, final):
    lines = ["## 轨迹 %d" % idx, "", "**原始问句：** %s" % question, ""]
    for st in steps:
        lines.append("### 第 %s 轮" % st.get("round"))
        lines.append("")
        lines.append("**模型输出：**")
        lines.append("")
        lines.append("```")
        lines.append(str(st.get("model_output") or "").strip() or "(空)")
        lines.append("```")
        lines.append("")
        if st.get("parsed_calls"):
            lines.append("**解析到的工具调用：** `%s`" % json.dumps(st["parsed_calls"], ensure_ascii=False))
            lines.append("")
        if st.get("tool_returns"):
            lines.append("**工具返回：**")
            for r in st["tool_returns"]:
                lines.append("- `%s`" % r)
            lines.append("")
    lines.append("**最终回答：**")
    lines.append("")
    lines.append(str(final).strip())
    lines.append("")
    return "\n".join(lines)


def demo_and_write_trace(out_path):
    """当堂交付：跑 3 条轨迹 + AST 越权拒绝记录，写入 call_trace.md。"""
    cases = [
        "请依次查询两件事：1. '把'字的 HSK 等级是多少？2. 现在的时间是多少？",
        "帮我算一下 35*24 等于多少",
        "商量 这个词是 HSK 几级？",
    ]
    blocks = [
        "# W9 工具调用轨迹记录（当堂交付）",
        "",
        "> 引擎：`%s` @ `%s`" % (MODEL, os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")),
        "> 工具：`get_time` / `calc`（白名单 AST）/ `hsk_level`",
        "> 每条含：原始问句、模型输出、工具返回、最终回答",
        "",
    ]
    for i, q in enumerate(cases, 1):
        print("=" * 60)
        print("CASE", i, q)
        steps = []
        ans = run(q, collect_trace=steps)
        print("FINAL:", ans)
        blocks.append(_format_trace(i, q, steps, ans))
        blocks.append("---")
        blocks.append("")

    # AST 越权拒绝（不经模型，直接测 calc 安全边界）
    bad_exprs = ["__import__('os').system('dir')", "open('x.txt')", "35*24+abs(1)"]
    blocks.append("## 附录：计算器 AST 越权拒绝记录")
    blocks.append("")
    blocks.append("下列表达式不应被执行；`calc` 必须返回「拒绝计算…」。")
    blocks.append("")
    for expr in bad_exprs:
        out = calc(expr)
        blocks.append("- 输入 `%s` → 输出 `%s`" % (expr, out))
        print("AST reject:", expr, "=>", out)
    blocks.append("")
    blocks.append("合法对照：`calc('35*24')` → `%s`" % calc("35*24"))
    blocks.append("")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_path)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks))
    print("wrote", path)
    return path


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo_and_write_trace("call_trace.md")
    else:
        q = " ".join(a for a in sys.argv[1:] if a != "--demo") or (
            "请依次查询两件事：1. '把'字的 HSK 等级是多少？2. 现在的时间是多少？"
        )
        print("用户输入：", q)
        steps = []
        ans = run(q, collect_trace=steps)
        for st in steps:
            print("--- round", st.get("round"), "---")
            print("模型输出：", st.get("model_output"))
            if st.get("tool_returns"):
                print("工具返回：", st.get("tool_returns"))
        print("助手：", ans)
