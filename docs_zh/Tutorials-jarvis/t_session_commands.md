---
title: OmicClaw 会话工作流程
---

# OmicClaw 会话工作流程

当前 OmicClaw 部署模型是共享的 gateway 运行时：

- web UI 在 gateway 模式内运行
- Telegram、飞书、iMessage 和 QQ 等可选通道连接到同一运行时
- 交互状态仍存储在 `~/.ovjarvis` 下

## 1. 推荐工作流程

1. 启动 `omicclaw` 或 `omicverse gateway`。
2. 如需添加通道，使用 `--channel ...`。
3. 通过聊天或 web 工作区上传 `.h5ad` 文件。
4. 加载数据集并发出自然语言分析请求。
5. 检查状态和内核健康情况。
6. 使用 `/save` 或通过 web UI 导出结果。

## 2. 当前会话根目录

默认根目录：

```text
~/.ovjarvis
```

常见条目：

- `config.json`
- `auth.json`
- `workspace/`
- `sessions/`
- `context/`
- `memory/`

## 3. 消息通道命令

当前命令集包括：

- `/workspace`
- `/ls [path]`
- `/find <pattern>`
- `/load <filename>`
- `/save`
- `/status`
- `/usage`
- `/model [name]`
- `/memory`
- `/cancel`
- `/reset`
- `/kernel`
- `/kernel ls`
- `/kernel new <name>`
- `/kernel use <name>`

## 4. Gateway 与 Web 行为

通过 `omicclaw` 或 `omicverse gateway` 启动时：

- 即使没有配置通道，web gateway 仍保持可用
- 若配置了通道，通道对话轮次和 web 运行时共享同一启动器技术栈
- 缺少通道凭据不会阻止 gateway 模式；启动器可以回退到仅 Web 模式

## 5. 纯代码模式是独立的

此会话工作流程不适用于一次性代码生成。

纯代码生成请使用：

```bash
omicverse claw -q "basic qc and clustering"
```
