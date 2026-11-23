# 作业 2 · 第 3 个 MCP 工具：`count_by_level`

## 输入 / 输出

| | 说明 |
|--|------|
| **工具名** | `count_by_level` |
| **输入** | `level: str`（HSK 等级，如 `"3"` / `"4"`） |
| **输出** | `"HSK 4 级共 N 个词"`；若无词则 `"该等级暂无词汇（数量 0）"` |
| **示例** | `count_by_level("4")` → `HSK 4 级共 4 个词`（以当前 `data/生词表.csv` 为准） |

## 客户端验证（本机实测）

`python demo_client.py`：

```text
工具列表: ['hsk_level', 'list_by_level', 'count_by_level']
hsk_level('把'): 把 -> 3 级
list_by_level('3'): 把、决定
list_by_level('1'): 该等级暂无词汇
count_by_level('4'): HSK 4 级共 4 个词
```
