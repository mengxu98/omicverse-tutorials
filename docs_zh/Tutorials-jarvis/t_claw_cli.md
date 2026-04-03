---
title: OmicVerse Claw CLI
---

# OmicVerse Claw CLI

`omicverse claw` 是基于 `ov.Agent` 构建的纯代码入口点。

适用场景：

- 仅需 Python 代码
- 不直接在当前机器上执行
- 快速的 CLI 工作流程，可从 Shell、脚本或外部工具调用

若您希望聊天式 gateway 工作流程，请使用 `omicclaw` 或 `omicverse gateway`。
若您希望为 Claude Code 或其他 MCP 客户端提供工具服务器，请使用 `omicverse mcp`。

## 1. 安装

本地开发安装：

```bash
pip install -e .
```

或安装发布版本：

```bash
pip install -U omicverse
```

检查 CLI 是否可用：

```bash
omicverse claw --help
```

## 2. 基本用法

最简单的形式：

```bash
omicverse claw "basic qc and clustering"
```

这将把生成的 Python 代码输出到 `stdout`。

更多示例：

```bash
omicverse claw "annotate lung scRNA-seq with a minimal workflow"
omicverse claw "find marker genes for each leiden cluster"
omicverse claw "write a basic PCA + neighbors + UMAP pipeline"
```

## 3. 将输出保存到文件

```bash
omicverse claw "basic qc and clustering" --output workflow.py
```

这样既能在 `stdout` 上保持生成代码整洁，同时将相同代码写入 `workflow.py`。

## 4. 常用选项

选择模型：

```bash
omicverse claw --model gpt-5.2 "basic qc and clustering"
```

使用显式 API 密钥：

```bash
omicverse claw --api-key "$OPENAI_API_KEY" "basic qc and clustering"
```

使用自定义端点：

```bash
omicverse claw \
  --endpoint http://127.0.0.1:11434/v1 \
  --model my-model \
  "basic qc and clustering"
```

禁用轻量级反思阶段：

```bash
omicverse claw --no-reflection "basic qc and clustering"
```

## 5. 调试模式

当您希望检查初始化、运行时注册表命中和内部进度时，使用 `--debug-registry`。

```bash
omicverse claw --debug-registry "basic qc and clustering"
```

调试模式下：

- 生成的 Python 代码仍输出到 `stdout`
- 初始化日志输出到 `stderr`
- 匹配的运行时注册表条目输出到 `stderr`
- `tqdm` 进度条显示当前阶段

典型阶段包括：

- `init agent`
- `inspect registry`
- `prepare prompt`
- `request model`
- `extract code`
- `review code`
- `rewrite scanpy`
- `finalize`

## 6. 运行时行为

`omicverse claw` 首先初始化 `OmicVerseAgent`，然后进入纯代码模式。

这意味着在代码生成之前，您会看到正常的 Agent 初始化日志，例如：

```text
🧭 Loaded 32 skills (progressive disclosure) (32 built-in)
Model: OpenAI GPT-5.2
Provider: Openai
Endpoint: https://api.openai.com/v1
✅ OpenAI API key available
📚 Function registry loaded: 90 functions in 4 categories
...
✅ Smart Agent initialized successfully!
```

然后 CLI 要求已初始化的 agent 仅返回代码，而不执行分析代码。

## 7. 守护进程模式

若重复启动的开销明显，可运行持久化的本地守护进程：

```bash
omicverse claw --daemon
```

然后向守护进程发送请求：

```bash
omicverse claw --use-daemon "basic qc and clustering"
```

带调试模式：

```bash
omicverse claw --use-daemon --debug-registry "basic qc"
```

守护进程将 OmicVerse 和默认的 `OmicVerseAgent` 保留在内存中，因此重复调用可以避免冷启动的导入和 agent 初始化开销。

停止守护进程：

```bash
omicverse claw --stop-daemon
```

## 8. 自定义 Socket 路径

默认守护进程 socket 为：

```text
~/.cache/omicverse/claw.sock
```

您可以覆盖它：

```bash
omicverse claw --daemon --socket /tmp/ov-claw.sock
omicverse claw --use-daemon --socket /tmp/ov-claw.sock "basic qc"
omicverse claw --stop-daemon --socket /tmp/ov-claw.sock
```

## 9. 推荐使用模式

单次生成：

```bash
omicverse claw "basic qc and clustering"
```

频繁本地实验：

```bash
omicverse claw --daemon
omicverse claw --use-daemon "basic qc and clustering"
omicverse claw --use-daemon "find marker genes"
```

调试运行时行为：

```bash
omicverse claw --debug-registry "basic qc and clustering"
```

## 10. 何时使用 Claw vs Jarvis

使用 `claw` 的场景：

- 您只需要代码
- 您希望自己检查或编辑生成的脚本
- 您希望从其他 CLI 或自动化层调用 OmicVerse

使用 `jarvis` 的场景：

- 您需要消息机器人工作流程
- 您需要会话记忆和交互式后续跟进
- 您需要面向人类的聊天界面

## 11. 相关页面

- OpenClaw 集成：[OpenClaw 集成](t_claw_openclaw.md)
- Gateway 概述：[OmicClaw Gateway 概述](t_msg_bot_overview.md)
- MCP 快速开始：[OmicVerse MCP 快速开始](../Tutorials-llm/t_mcp_quickstart.md)
