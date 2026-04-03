---
title: OmicClaw 故障排查
---

# OmicClaw 故障排查

## 1. 启动器行为

1. `omicverse claw` 打开了 web UI 而非返回代码
   这是当前预期行为。`omicverse claw` 默认进入 gateway 模式，除非您传递 `-q`、`--question` 或守护进程标志。

2. 我只需要代码
   使用：

   ```bash
   omicverse claw -q "basic qc and clustering"
   ```

3. `omicclaw` 总是要求登录
   这也是预期行为。`omicclaw` 入口点会启用强制登录的 web 行为，这是设计使然。

4. Gateway 已启动但没有机器人在线
   若未配置 `--channel`，gateway 以仅 Web 模式运行。

## 2. 配置与认证

1. 配置向导未启动
   运行 `omicclaw --setup --setup-language zh` 或 `omicverse gateway --setup --setup-language zh`。

2. 模型或提供商设置未生效
   检查 `~/.ovjarvis/config.json` 和 `~/.ovjarvis/auth.json`，然后重启启动器。

3. 未找到提供商密钥
   导出对应的环境变量或使用 `--api-key`。

## 3. Telegram

1. 缺少依赖
   运行 `pip install -e ".[jarvis]"` 或 `pip install "omicverse[jarvis]"`。

2. 缺少 token
   检查 `TELEGRAM_BOT_TOKEN` 或 `--token`。

3. `409 Conflict`
   另一个进程正在使用相同的 bot token。

## 4. 飞书

1. 缺少 WebSocket SDK
   安装 `lark-oapi`。

2. Webhook 验证失败
   验证回调 URL 与 `--feishu-host/--feishu-port/--feishu-path` 是否一致。

3. 能收发文字但无法收发图片/文件
   检查飞书应用权限和部署可达性。

## 5. iMessage

1. 找不到 `imsg`
   检查 `which imsg`。

2. 无法访问 `chat.db`
   验证数据库路径和 macOS 权限。

## 6. QQ

1. 凭据缺失
   检查 `QQ_APP_ID` 和 `QQ_CLIENT_SECRET`。

2. 图片发送失败
   检查 `--qq-image-host` 的公网可达性。

3. Markdown 不生效
   验证 QQ 机器人是否已获得 markdown 消息权限。
