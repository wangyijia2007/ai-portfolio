# 作业 3（后半）· 第 9 周「工具调用」预习

> 互评表 `peer_review.md` 暂缓，先完成工具清单。希望助手 v1.x 再拥有下列 2 个工具。

## 工具 1：查生词表（HSK 词级查询）

| | 说明 |
|--|------|
| **用途** | 输入一个汉语词，返回它在 HSK 大纲中的等级与释义摘要，便于备课筛词。 |
| **输入** | `word: str`（必填，如 `"把"`）；可选 `dict_version: str`（如 `"旧版HSK"` / `"新汉语水平考试"`，默认旧版）。 |
| **输出** | `{"word": str, "level": str\|null, "gloss": str, "found": bool}`。未收录时 `found=false`，`level=null`，`gloss` 给简短提示。 |
| **示例** | 入 `"把"` → 出 `{"word":"把","level":"HSK3","gloss":"介词/处置义……","found":true}` |

## 工具 2：课堂小测算分

| | 说明 |
|--|------|
| **用途** | 根据客观题对错与题分，汇总总分、正确率，并标出错题号，方便课后反馈。 |
| **输入** | `items: list[{"id": str, "score": float, "correct": bool}]`（每题编号、满分、是否答对）；可选 `pass_line: float`（及格线，默认 60）。 |
| **输出** | `{"total": float, "earned": float, "accuracy": float, "passed": bool, "wrong_ids": list[str]}`。 |
| **示例** | 入三题各 10 分、对对错 → 出 `{"total":30,"earned":20,"accuracy":0.67,"passed":true,"wrong_ids":["Q3"]}` |

**与现有助手的关系：** 当前 `answer()` 只做检索+生成；W9 工具调用后，模型可在需要时主动调用「查生词」「算分」，而不是把查表和加减法都塞进自由文本生成。
