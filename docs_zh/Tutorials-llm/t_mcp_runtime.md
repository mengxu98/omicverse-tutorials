---
title: OmicVerse MCP 运行时与故障排查
---

# OmicVerse MCP 运行时与故障排查

本页面介绍服务器如何管理数据、持久化、取消操作和日志。

## 句柄

### `adata_id`

`adata_id` 是数据集的稳定 MCP 句柄。数据集本身保留在服务器端。

- 使用 `ov.utils.read` 或 `ov.datasets.*` 加载
- 将返回的句柄传递给下游工具
- 使用 `ov.persist_adata` 持久化
- 使用 `ov.restore_adata` 恢复

### `artifact_id`

绘图和导出工具可以将文件注册为 artifact，通过 `artifact_id` 引用。

### `instance_id`

P2 基于类的工具使用 `instance_id` 来支持多步骤分析器，如 DEG 或 metacell 工作流程。

### 句柄类型一览

| 句柄类型 | 前缀 | 可持久化 | 示例 |
|-------------|--------|-------------|---------|
| `adata` | `adata_` | 是 | 加载的数据集 |
| `artifact` | `artifact_` | 若文件存在于磁盘则是 | 图表、导出文件 |
| `instance` | `inst_` | 否 | P2 分析器 |

## 持久化

使用 `ov.persist_adata` 写入 `.h5ad` 文件及元数据 sidecar。使用 `ov.restore_adata` 在之后的会话中恢复。

这是跨客户端重连或进程重启后的推荐恢复路径。

### 持久化示例

```json
{"tool_name": "ov.persist_adata", "arguments": {"adata_id": "adata_a1b2c3d4e5f6"}}
```

```json
{"tool_name": "ov.restore_adata", "arguments": {"path": "/data/ov_persist/adata_a1b2c3d4e5f6.h5ad"}}
```

## 会话与可观测性

常用工具：

- `ov.get_session`
- `ov.list_handles`
- `ov.get_metrics`
- `ov.list_events`
- `ov.get_trace`
- `ov.list_traces`
- `ov.get_health`
- `ov.get_limits`

示例问题：

- `What's the current session status?`
- `Show me the recent tool call traces`
- `Show me session metrics`
- `List all image artifacts from this session`
- `Clean up artifacts older than 1 hour, but show me what would be deleted first`
- `Export the full artifact manifest as JSON`

示例响应通常如下：

```json
{
  "session_id": "default",
  "adata_count": 1,
  "artifact_count": 3,
  "instance_count": 0
}
```

```json
[
  {"trace_id": "abc...", "tool_name": "ov.pp.pca", "duration_ms": 245.3, "ok": true}
]
```

```json
{
  "adata_count": 1,
  "artifact_count": 3,
  "tool_calls_total": 8,
  "tool_calls_failed": 0,
  "artifacts_registered_total": 3
}
```

## AnnData 检查

在让模型分析数据之前，让其检查当前状态：

- `ov.adata.describe`
- `ov.adata.peek`
- `ov.adata.find_var`
- `ov.adata.value_counts`
- `ov.adata.inspect`

这些工具减少了幻觉，使工作流程可审计。

## 取消操作与 `Esc`

对于 `adata_id` 工具，OmicVerse MCP 现在通过持久化的内核支持的运行时来执行它们。

这意味着：

- 客户端仍然看到正常的 `Running...` 状态
- 取消时可以中断运行时
- 中断后内核通常可以重用
- 目标是尽可能保留状态，而不是为每个工具调用重建工作进程

实际上，取消操作取决于客户端和底层数值计算代码：

- 若客户端发送适当的取消或断开信号，服务器可以中断当前运行时
- 一些深层数值调用可能对中断响应较慢
- 若运行时变得不健康，服务器可能需要在下次请求前恢复

## 日志

### `stdio`

- 协议流量使用 `stdout`
- 服务器日志写入 `stderr`
- 工具调用的开始/结束/失败摘要写入 `stderr`

### `streamable-http`

- 自行运行服务器
- 直接检查 uvicorn 和服务器日志
- 这通常是调试连接问题最简单的方法

## P2 生命周期

P2 工具使用多步骤生命周期：

1. `create`
2. `run` 或特定任务操作，如 `annotate` / `train`
3. `results` 或 `predict`
4. `destroy`

示例：

```text
ov.bulk.pydeg create -> run -> results -> destroy
```

`instance_id` 值仅保存在内存中，服务器重启后会丢失。

## 限制

- P2 工具可能出现在列表中，但在运行时仍可能不可用
- 扩展运行时在某些环境中受到约束
- 本地 HTTP 认证仅用于本地开发环境
- 内置的本地 OAuth 流程仅在内存中，不应暴露给不受信任的网络
- 服务器在工具执行方面实际上是单进程的
- 一些长时间的数值步骤可能对中断响应较慢
- 无结果流式传输：大型输出以完整结果返回
- 类实例仅保存在内存中，服务器重启后会丢失
- 并非每个扩展依赖栈在每个环境中都可用

## 常见问题

### 工具缺失

- 验证启动时使用的 `--phase`
- 让客户端运行 `ov.list_tools`
- 对于 P2 工具，检查 `ov.describe_tool` 中的依赖可用性

### `adata_id` 未找到

句柄从未创建、已过期或属于另一个会话。使用 `ov.list_handles` 和 `ov.get_session`。

### 图表存在但难以找到

使用：

- `ov.list_artifacts`
- `ov.describe_artifact`
- `ov.export_artifacts_manifest`

### 长时间运行的分析阻碍进度

- 优先使用本地 HTTP 模式以获得可观测性
- 在特别耗时的步骤前持久化数据集
- 使用 `ov.get_trace`、`ov.list_traces` 和 `ov.list_events` 了解已运行的内容

### 服务器崩溃或连接丢失

- 检查 `stderr` 或 HTTP 服务器日志
- 检查 `stderr` 中的 Python traceback 或导入错误
- 重启 MCP 服务器
- 若之前已持久化数据集，使用 `ov.restore_adata`

### 工具不可用

- 请求 `ov.describe_tool`
- 检查缺少的可选依赖
- 安装缺失包后重启

### 远程服务器连接失败

- 单独验证 SSH 连接，例如 `ssh -i /path/to/key -p <port> user@host echo ok`
- 确保远程机器上已安装 `omicverse[mcp]`
- 检查客户端配置中的远程 Python 路径

### 预处理步骤因缺少数据需求而失败

- 服务器强制执行流程顺序
- 遵循错误响应中 `suggested_next_tools` 的建议
- 典型前提条件：
  - `ov.pp.pca` 需要 `layers["scaled"]`
  - `ov.pp.neighbors` 需要 `obsm["X_pca"]`
  - `ov.pp.umap` 需要 `uns["neighbors"]`

### 服务器立即退出

- 确保已安装 `mcp>=1.0`
- 若使用 `streamable-http`，确保已安装 `uvicorn` 和 `starlette`

### Claude Code HTTP 连接显示认证/发现错误

- 确认服务器以 `--transport streamable-http` 启动
- 验证配置的 URL 完全匹配，例如 `http://127.0.0.1:8765/mcp`
- 在认证或传输方式更改后重启本地 MCP 服务器，因为本地 OAuth 注册仅在内存中

这些可观测性工具是工作流程出现意外行为时首先应使用的工具。

## 相关页面

- 配置：[快速开始](t_mcp_quickstart.md)
- 工具目录：[工具目录](t_mcp_tools.md)
- 精确 CLI 和 JSON 格式：[参考文档](t_mcp_reference.md)
