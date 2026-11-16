# 作业 4 · C 路径：手写 tool_agent ↔ smolagents 5 行映射表

> 对照：Hugging Face `smolagents`（Apache-2.0）；官方文档 https://huggingface.co/docs/smolagents/index  
> 我的实现：`week09_工具调用/tool_agent.py`  
> 本机路径：C（离线 / 小模型）— 交映射表 + 约 300 字反思；不要求跑通框架示例。

| # | 我写的 `tool_agent.py` | smolagents 里对应什么 |
|---|------------------------|------------------------|
| 1 | `TOOLS` 字典：名字 → 函数 | `@tool` 装饰器把带类型注解与 `Args:` 文档的函数变成 `Tool`，交给 `ToolCallingAgent(tools=[...])` |
| 2 | `SYS` 提示词要求输出 JSON | `ToolCallingAgent` 用模型原生 tool calling（JSON-like），提示模板在框架的 `prompts/toolcalling_agent.yaml` |
| 3 | `parse_calls` 剥围栏、兜底抓 JSON | 框架内部解析 `ChatMessageToolCall`，不用自己写正则 |
| 4 | `TOOLS[name](*args)` 执行 + 异常兜底 | 框架按 `Tool.inputs` 校验参数后调用，执行结果进入多步消息 |
| 5 | `run()` 手动回喂 + `max_calls` 收口 | `MultiStepAgent` 的多步循环由框架管理步数与停止条件 |

## 约 300 字反思（手写循环 vs 框架）

手写 `tool_agent.py` 把「决定 → 解析 → 执行 → 回喂 → 收口」五步摊在纸面上：工具名进 `TOOLS`、格式进 `SYS`、坏 JSON 靠 `parse_calls`、危险运算靠 AST 白名单、死循环靠 `max_calls`。这样做的代价是啰嗦，收益是排障时能看见模型原文和工具返回——本周失败会诊就是这么定位「裸算式参数」的。smolagents 把解析、校验、多步循环收进 `ToolCallingAgent`，用 `@tool` 的类型注解当文档，省掉正则和手写回喂；但也拿走了一部分控制权——模型到底点了什么，默认藏在框架消息里，要主动打开日志才看得见。课程建议「先手写再看框架」说得对：没有 60 行循环，就分不清框架替你省的是哪一层。W10 的 MCP 会继续问：若工具在别人机器上，登记方式是否也要标准化——那是协议层，不是再写一套 `parse_calls`。
