---
title: OmicClaw Gateway 概述
---

# OmicClaw Gateway 概述

OmicClaw 现在作为统一的 gateway 产品进行文档说明，而不再是旧版的"仅消息机器人"启动器。

当前入口点为：

- `omicclaw`：OmicClaw 品牌启动器。启动 gateway 模式并强制触发 web 登录流程。
- `omicverse gateway`：通用 gateway 启动器。启动 web UI 并自动启动已配置的通道。
- `omicverse claw`：默认进入 gateway 模式。仅在需要一次性代码生成时使用 `-q/--question`。

## 1. 推荐启动模式

当您希望 OmicClaw 品牌产品体验时使用 `omicclaw`：

```bash
omicclaw
```

当您希望相同的 gateway 运行时但不带 OmicClaw 品牌时，使用 `omicverse gateway`：

```bash
omicverse gateway
```

仅在需要纯代码生成时使用 `omicverse claw -q`：

```bash
omicverse claw -q "basic qc and clustering"
```

## 2. 每个入口点实际执行的操作

| 入口点 | 当前行为 | 推荐用途 |
| --- | --- | --- |
| `omicclaw` | 以强制登录和 OmicClaw 品牌启动 gateway 模式 | 面向用户的主产品入口 |
| `omicverse gateway` | 启动 gateway web UI 和后台通道运行时 | 通用部署 / 运维 |
| `omicverse claw` | 除非给定 `-q`、`--daemon`、`--use-daemon` 或 `--stop-daemon`，否则启动 gateway 模式 | 混合 CLI，特别是纯代码模式 |

## 3. 仅 Gateway 模式 vs 通道支持模式

若在不添加 `--channel` 的情况下启动 gateway 模式，OmicVerse 以仅 Web 模式保持 web UI 运行。

示例：

```bash
omicclaw
```

或：

```bash
omicverse gateway
```

若添加通道，相同的 gateway 运行时将同时启动 web UI 和所选消息通道。

示例：

```bash
omicclaw --channel telegram --token "$TELEGRAM_BOT_TOKEN"
```

## 4. 共享运行时布局

当前 gateway/通道技术栈仍将运行时状态存储在：

```text
~/.ovjarvis
```

典型内容包括：

- `config.json`：持久化的启动器和通道默认值
- `auth.json`：已保存的认证状态
- `workspace/`：用户可见的文件和提示词
- `sessions/`：运行时会话数据
- `context/`：缓存的上下文
- `memory/`：每日摘要和记忆 artifact

## 5. 推荐阅读顺序

1. [配置与认证](t_setup_auth.md)
2. 针对您部署目标的通道教程
3. [会话工作流程](t_session_commands.md)
4. [常见问题](t_troubleshooting.md)

通道页面：

- [Telegram 教程](t_channel_telegram.md)
- [飞书教程](t_channel_feishu.md)
- [iMessage 教程](t_channel_imessage.md)
- [QQ 教程](t_channel_qq.md)

## 6. 相关页面

- 配置：[配置与认证](t_setup_auth.md)
- 会话工作流程：[会话工作流程](t_session_commands.md)
