---
title: OmicClaw 配置与认证
---

# OmicClaw 配置与认证

本页面记录了新版 OmicClaw / gateway 启动器技术栈的当前配置路径。

## 1. 安装

开发用途：

```bash
pip install -e ".[jarvis]"
```

常规使用：

```bash
pip install "omicverse[jarvis]"
```

对于 macOS iMessage 支持，还需安装：

```bash
brew install steipete/tap/imsg
```

## 2. 推荐的首次运行

OmicClaw 品牌首次运行：

```bash
omicclaw --setup --setup-language zh
```

通用 gateway 首次运行：

```bash
omicverse gateway --setup --setup-language zh
```

## 3. 持久化配置与认证文件

默认情况下，启动器将状态存储在：

```text
~/.ovjarvis
```

重要文件：

- `~/.ovjarvis/config.json`：已保存的启动器、模型和通道默认值
- `~/.ovjarvis/auth.json`：已保存的提供商认证或 OAuth 状态

可使用以下命令重定向配置向导：

```bash
omicclaw \
  --setup \
  --config-file ~/.ovjarvis/config.json \
  --auth-file ~/.ovjarvis/auth.json
```

## 4. 认证来源

当前运行时支持：

- 提供商环境变量，如 `ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 和 `GEMINI_API_KEY`
- 由配置向导写入的已保存提供商认证
- 保存到 `auth.json` 中的 OpenAI Codex OAuth
- 通过 `--endpoint` 指定的自定义 OpenAI 兼容端点

示例：

```bash
export ANTHROPIC_API_KEY="your_api_key"
omicclaw --model claude-sonnet-4-6 --channel telegram --token "$TELEGRAM_BOT_TOKEN"
```

## 5. 当前启动器行为

新版入口逻辑为：

- `omicclaw`：以强制登录和 OmicClaw 品牌启动 gateway 模式
- `omicverse gateway`：以通用 OmicVerse 品牌启动 gateway 模式
- `omicverse claw`：默认启动 gateway 模式；仅在需要纯代码生成时使用 `-q/--question`

若在不添加 `--channel` 的情况下启动 gateway 模式，web UI 以仅 Web 模式运行。

## 6. 常用运行时标志

- `--channel`：`telegram`、`feishu`、`imessage` 或 `qq`
- `--model`：LLM 模型名称
- `--api-key`：显式提供商密钥
- `--auth-mode`：`environment`、`openai_oauth`、`saved_api_key` 或 `no_auth`
- `--endpoint`：自定义 OpenAI 兼容的基础 URL
- `--session-dir`：会话根目录
- `--max-prompts`：内核重启前的提示词配额；`0` 禁用自动重启
- `--web-host` / `--web-port`：gateway web 绑定设置
- `--no-browser`：阻止启动器自动打开浏览器
- `--verbose`：启用详细日志

## 7. 推荐使用模式

以 Web 优先的 OmicClaw 产品入口：

```bash
omicclaw
```

Gateway 加通道：

```bash
omicclaw --channel feishu --feishu-connection-mode websocket
```

纯代码生成：

```bash
omicverse claw -q "basic qc and clustering"
```
