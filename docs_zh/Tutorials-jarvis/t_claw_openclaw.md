---
title: OpenClaw 与 OmicVerse Claw 的集成
---

# OpenClaw 与 OmicVerse Claw 的集成

OpenClaw 集成应理解为：

- OpenClaw 加载一个 skill
- 该 skill 教会 agent 调用本地 `omicverse claw` CLI
- `omicverse claw` 成为 OmicVerse 工作流程的代码生成接口

这与将 OpenClaw 视为通用 Shell 包装器不同。正确的思维模型是：将 `omicverse claw` 作为本地能力暴露给 OpenClaw。

## 1. OpenClaw 实际提供的功能

根据 OpenClaw 文档：

- skill 位于 `<workspace>/skills` 或 `~/.openclaw/skills`
- skill 是包含 `SKILL.md` 的目录
- 用户可调用的 skill 可通过 `/skill <name> ...` 触发
- skill 可以要求 `PATH` 中存在特定二进制文件
- agent 使用 `exec` 工具运行本地 Shell 命令

因此 OmicVerse 的集成点不是自定义 OpenClaw 协议，而是一个指示 OpenClaw 运行 OmicVerse CLI 的 skill。

## 2. 集成目标

目标是给 OpenClaw 提供一个稳定的接口，例如：

```bash
omicverse claw -q "basic qc and clustering"
```

或者，当需要确定性输出文件时：

```bash
omicverse claw -q "basic qc and clustering" --output omicverse_generated.py
```

换言之，OpenClaw 应将 `omicverse claw` 视为将自然语言请求转换为 OmicVerse 代码的本地后端。

## 3. 推荐架构

最实用的架构是：

1. 在 OpenClaw 可以运行 `exec` 的同一台机器上安装 `omicverse`
2. 创建一个 OpenClaw skill，如 `omicverse_claw`
3. 在该 skill 中，指示 OpenClaw 调用本地 `omicverse claw` 命令
4. 让 OpenClaw 返回或保存生成的 Python 代码

这样职责划分清晰：

- OpenClaw 负责对话和 skill 路由
- `omicverse claw` 负责 OmicVerse 代码生成
- 代码执行仍是独立的下游决策

## 4. 创建工作区 Skill

在 OpenClaw 支持的位置之一创建 skill 目录：

- 工作区 skill：`<workspace>/skills/omicverse-claw`
- 用户 skill：`~/.openclaw/skills/omicverse-claw`

对于项目本地集成，工作区路径通常是最佳选择。

示例：

```bash
mkdir -p ./skills/omicverse-claw
```

然后创建 `./skills/omicverse-claw/SKILL.md`，内容如下：

```md
---
name: omicverse_claw
description: Generate OmicVerse analysis code by calling the local omicverse claw CLI.
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["omicverse"]}}}
---

# OmicVerse Claw

Use this skill when the user wants OmicVerse analysis code, pipelines, or function-based workflow snippets.

Treat the user input after `/skill omicverse_claw` as the exact natural-language prompt for OmicVerse code generation.

Always call the local OmicVerse CLI with OpenClaw's `exec` tool instead of inventing the workflow directly.

Preferred command:

`omicverse claw -q "<user request>" --output "{baseDir}/omicverse_claw_latest.py"`

Rules:

- Preserve the user's request faithfully.
- Prefer `--output` so the generated code is saved deterministically.
- If the user asks for debugging or registry details, add `--debug-registry`.
- After the command succeeds, read `{baseDir}/omicverse_claw_latest.py` and return the generated Python code.
- If the command fails, report stderr and explain whether the `omicverse` binary is missing from `PATH`.
```

这给了 OpenClaw 一个专用的 OmicVerse 代码生成 skill。

推荐的目录结构：

```text
your-openclaw-workspace/
├── skills/
│   └── omicverse-claw/
│       └── SKILL.md
└── ...
```

## 5. 如何从 OpenClaw 调用它

OpenClaw 刷新 skill 后，可以通过以下任一方式调用。

显式 skill 调用：

```text
/skill omicverse_claw basic qc and clustering
```

另一个示例：

```text
/skill omicverse_claw generate code for harmony batch correction and leiden clustering
```

若您的 OpenClaw 界面暴露了原生 skill 命令，该 skill 也可以直接通过以下方式调用：

```text
/omicverse_claw basic qc and clustering
```

`/skill <name> ...` 是最安全的已文档化形式。

若 skill 未立即出现，请启动新的 OpenClaw 会话。OpenClaw 在会话开始时对符合条件的 skill 进行快照，并在整个对话中复用该列表。

## 6. OpenClaw 应运行的命令

对于一次性生成，skill 通常应运行：

```bash
omicverse claw -q "<user request>" --output "{baseDir}/omicverse_claw_latest.py"
```

用于调试：

```bash
omicverse claw -q "<user request>" --output "{baseDir}/omicverse_claw_latest.py" --debug-registry
```

对于同一机器上的重复使用，skill 可以优先使用守护进程路径：

```bash
omicverse claw -q "<user request>" --output "{baseDir}/omicverse_claw_latest.py" --use-daemon
```

这才是 OpenClaw 应依赖的真实接口。

## 7. 宿主机 vs 沙箱

OpenClaw 的 `exec` 工具可以在沙箱中或 gateway 宿主机上运行。

对于 OmicVerse，常见情况是：

- 若 `omicverse` 安装在 OpenClaw 宿主机上，在宿主机上运行
- 若您的 OpenClaw agent 被沙箱化，可在沙箱内安装 `omicverse`，或将执行路由到宿主机

若 OpenClaw 找不到二进制文件，请检查：

- `omicverse` 是否在 `PATH` 中
- skill 的 `requires.bins` 是否与实际安装匹配
- 您的 `exec` 宿主机/安全设置是否允许该命令运行

## 8. 插件打包

若希望以 OpenClaw 插件风格分发此集成，可将相同的 skill 打包在插件仓库的 `skills/.../SKILL.md` 目录中。

OpenClaw 插件可以包含 skill，这些 skill 在插件启用时加载。在这种模式下：

- 插件提供 skill
- skill 教会 agent 调用 `omicverse claw`
- OmicVerse 仍然是实际的本地 CLI 后端

对于大多数用户，工作区 skill 已经足够。只有当您希望分发或版本化集成时，才需要插件。

实用的划分方式：

- 仅在单个仓库中需要集成时，使用工作区 skill
- 希望跨项目使用时，使用 `~/.openclaw/skills`
- 希望提供带有清单和配置的可分发包时，使用 OpenClaw 插件

## 9. 推荐的用户提示词

以下内容作为 OpenClaw skill 输入效果良好：

```text
basic qc and clustering
generate code for PCA, neighbors, UMAP, and leiden
find marker genes for each leiden cluster
write a minimal scRNA-seq annotation workflow with OmicVerse
prepare a harmony-based batch correction workflow
```

## 10. 重要说明

- `omicverse claw -q` 是代码生成接口，而非聊天运行时
- OpenClaw 应使用它生成 OmicVerse 代码，而非用临时 Shell 逻辑替代
- `stdout` 是代码输出；`stderr` 用于初始化日志和调试信息
- `-q "<request>" --output <file>` 是 OpenClaw skill 使用最稳定的模式
- 守护进程模式（`--use-daemon`）仅在 OpenClaw 需要重复调用 `omicverse claw` 时才有用

## 11. 相关页面

- 完整 CLI 教程：[OmicVerse Claw CLI](t_claw_cli.md)
- Gateway 概述：[OmicClaw Gateway 概述](t_msg_bot_overview.md)
