# M1 会话协议草案（一页）

> 课程：第十次课课后作业 3 · 多端阶段第一优先级文档  
> 作者：王一嘉 · 仓库 `wangyijia2007/ai-portfolio`  
> 范围：教学助手会话（听→想→调工具→说），含打断与断线补发

---

## ① 事件类型与字段

每条事件统一信封：

| 字段 | 类型 | 说明 |
|------|------|------|
| `session_id` | string | 一次会话唯一 ID |
| `seq` | uint | 会话内单调递增序号（客户端发送侧从 1 起） |
| `ts` | ISO-8601 | 发送端时间戳 |
| `type` | enum | 见下表 |
| `payload` | object | 类型相关正文 |

| type | 方向 | payload 要点 |
|------|------|----------------|
| `user_audio` / `user_text` | C→S | 用户输入片段或完整文本 |
| `asr_partial` / `asr_final` | S→C | 识别中间结果 / 最终文本 |
| `assistant_delta` / `assistant_final` | S→C | 流式回复片段 / 收束 |
| `tool_call` / `tool_result` | S↔工具侧再回 C | 工具名、参数、返回摘要 |
| `interrupt` | C→S | 用户打断（说话/点停） |
| `state` | S→C | 当前状态机状态广播 |
| `ack` / `nack` | 双向 | 确认 `seq`；`nack` 带原因 |
| `resync` | C→S | 断线重连：带本端已收最大 `seq` |

---

## ② 状态机

```text
idle → listening → thinking → tool_calling → speaking → idle
```

- **idle**：无进行中轮次；可接受新用户输入。
- **listening**：采集/识别用户话轮；`asr_final` 后进入 `thinking`。
- **thinking**：模型规划是否调工具；若需工具 → `tool_calling`，否则 → `speaking`。
- **tool_calling**：执行 MCP/本地工具；结果回灌模型后 → `speaking`（或再进 `thinking` 多步）。
- **speaking**：播报/推送助手输出；正常结束 → `idle`。

**打断回退：** 任意非 `idle` 收到 `interrupt` → 取消未完成生成与未确认工具副作用（只读工具可丢弃结果）→ 回到 `listening`（若用户继续说）或 `idle`。

---

## ③ 权威与幂等

- **服务端为会话唯一权威**：以服务端状态机与事件日志为准；客户端 UI 只是投影。
- **按 `seq` 去重**：同一 `session_id` 下重复 `seq` 只处理一次；重放返回原 `ack`。
- **工具调用幂等键**：`tool_call` 带 `call_id`；只读工具可重试；有副作用工具须服务端记账，相同 `call_id` 不二次执行。

---

## ④ 断线语义

1. 客户端重连后发 `resync{ last_seq }`（本端已成功处理的最大服务端 `seq`）。
2. 服务端自 `last_seq+1` **补发**仍有效的事件（`assistant_*` / `state` / 未确认的 `tool_result` 摘要）；过期流式片段可折叠为一条 `assistant_final`。
3. 客户端补发期间本地未 `ack` 的上行事件，按原 `seq` 重传；服务端去重后继续。
4. 若服务端会话已过期：返回 `nack{ reason: session_expired }`，客户端开新 `session_id`。

---

*下周课上收；字段名以本页为准，避免多端各写一套。*
