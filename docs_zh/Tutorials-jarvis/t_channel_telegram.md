---
title: OmicClaw Telegram 教程
---

# OmicClaw Telegram 教程

Telegram 现在作为 gateway 支持的通道进行文档说明，不再作为独立的旧版 Jarvis 入口。

## 1. 创建 Telegram Bot

1. 在 Telegram 中打开 `@BotFather`。
2. 发送 `/newbot`。
3. 提供显示名称和用户名。
4. 将返回的 token 保存为 `TELEGRAM_BOT_TOKEN`。

## 2. 环境变量

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-..."
export ANTHROPIC_API_KEY="your_api_key"
```

## 3. 推荐启动命令

OmicClaw 品牌入口：

```bash
omicclaw --channel telegram --token "$TELEGRAM_BOT_TOKEN"
```

通用 gateway 入口：

```bash
omicverse gateway --channel telegram --token "$TELEGRAM_BOT_TOKEN"
```

## 4. 完整启动命令

```bash
omicclaw \
  --channel telegram \
  --token "$TELEGRAM_BOT_TOKEN" \
  --model claude-sonnet-4-6 \
  --api-key "$ANTHROPIC_API_KEY" \
  --auth-mode environment \
  --session-dir ~/.ovjarvis \
  --max-prompts 0 \
  --allowed-user your_telegram_username \
  --allowed-user 123456789 \
  --web-port 5050 \
  --verbose
```

## 5. 当前行为说明

- 通过 `omicclaw` 或 `omicverse gateway` 启动时，同时会启动 web gateway。
- 若仅需代码生成，请勿使用此路径；请使用 `omicverse claw -q ...`。

## 6. 常用命令

- `/workspace`
- `/load <filename>`
- `/save`
- `/status`
- `/kernel`
- `/kernel ls`
- `/kernel new <name>`
- `/kernel use <name>`
- `/cancel`
- `/reset`

## 7. 故障排查

1. 缺少 Telegram 依赖
   运行 `pip install -e ".[jarvis]"` 或 `pip install "omicverse[jarvis]"`。

2. 缺少 token 错误
   检查 `TELEGRAM_BOT_TOKEN` 或 `--token`。

3. `409 Conflict`
   停止使用相同 bot token 的其他进程。
