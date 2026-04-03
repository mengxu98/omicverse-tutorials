---
title: OmicClaw iMessage 教程
---

# OmicClaw iMessage 教程

iMessage 仍然是仅限 macOS 的通道，但现在通常通过 gateway 技术栈启动。

## 1. 安装依赖

```bash
brew install steipete/tap/imsg
```

## 2. 推荐启动命令

```bash
omicclaw \
  --channel imessage \
  --imessage-cli-path "$(which imsg)" \
  --imessage-db-path ~/Library/Messages/chat.db
```

等效的通用 gateway 入口：

```bash
omicverse gateway \
  --channel imessage \
  --imessage-cli-path "$(which imsg)" \
  --imessage-db-path ~/Library/Messages/chat.db
```

## 3. 完整启动命令

```bash
omicclaw \
  --channel imessage \
  --imessage-cli-path "$(which imsg)" \
  --imessage-db-path ~/Library/Messages/chat.db \
  --imessage-include-attachments \
  --model claude-sonnet-4-6 \
  --api-key "$ANTHROPIC_API_KEY" \
  --auth-mode environment \
  --session-dir ~/.ovjarvis \
  --max-prompts 0 \
  --verbose
```

## 4. 当前注意事项

- 通过 `omicclaw` 或 `omicverse gateway` 启动可保持 web gateway 可用。
- 仅在代码生成时使用 `omicverse claw -q ...`，不适用于 iMessage 机器人运行时。

## 5. 故障排查

1. 找不到 `imsg`
   检查 `which imsg`。

2. 无法读取 `chat.db`
   验证数据库路径和 macOS 权限提示。

3. 附件丢失
   添加 `--imessage-include-attachments` 启动。
