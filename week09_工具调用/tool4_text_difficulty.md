# 作业 2 · 第 4 个工具：课文难度评估 `text_difficulty`

## 输入 / 输出

| | 说明 |
|--|------|
| **工具名** | `text_difficulty` |
| **输入** | `text_or_alias: str`（课文原文，或别名 `"愚公移山"` 自动读 `data/愚公移山.txt`）；`target_level: str\|int`（目标等级，如 `4` / `"HSK4"`，默认 4） |
| **输出** | JSON 字符串：`source`、`target_level`、`matched`、`coverage`（达标词 / 命中词）、`in_level`、`over_level` |
| **示例调用** | `{"tool":"text_difficulty","args":["愚公移山","4"]}` |

## 设计说明

- 确定数据靠查表：用 `data/生词表.csv` 做最长匹配，不让模型「猜」哪个词超纲。
- 覆盖率 = 等级 ≤ 目标等级的命中词数 / 命中词总数；超纲词单独列出，方便备课删改。
- 已挂进 `TOOLS`，并写入 SYS，可与另外 3 个工具一起被模型点名。

## 本地自测（不经模型）

```text
text_difficulty("愚公移山", "4")
```

实测输出：

```json
{"source": "愚公移山.txt", "target_level": 4, "matched": 11, "coverage": 0.364, "in_level": ["商量(HSK4)", "感动(HSK4)", "坚持(HSK4)", "把(HSK3)"], "over_level": ["愚公移山(HSK5)", "子子孙孙(HSK5)", "无穷无尽(HSK5)", "叩石垦壤(HSK6)", "寒暑易节(HSK6)", "智叟(HSK6)", "愚公(HSK6)"]}
```

解读：命中 11 词，对 HSK4 覆盖率约 36.4%；超纲以专名与成语为主，备课需释义或降级改写。