---
title: OmicVerse MCP 服务器指南
---

# OmicVerse MCP 服务器

OmicVerse MCP 服务器通过[模型上下文协议](https://modelcontextprotocol.io/)将已注册的分析函数作为工具暴露出来。Claude Code、Claude Desktop 以及其他 MCP 客户端可以发现并调用这些工具，同时底层的 `AnnData` 对象保留在服务器端。

!!! tip "如何阅读 MCP 文档"

    本页面现在是概述入口。原来的长篇指南已按主题拆分，以便您可以直接跳转到所需部分，而无需阅读一篇很长的页面。

## 阅读路线图

- **最快路径**：[快速开始](t_mcp_quickstart.md)
- **完整入门路径**：[完整启动](t_mcp_full_start.md)
- **完整工具目录**：[工具目录](t_mcp_tools.md)
- **Claude / HTTP / SSH 配置**：[客户端与部署](t_mcp_clients.md)
- **`adata_id`、持久化、取消、日志、故障排查**：[运行时与故障排查](t_mcp_runtime.md)
- **标志、JSON-RPC、错误码、精确计数**：[参考文档](t_mcp_reference.md)
- **带截图的 Claude Code 演练**：[在 Claude Code 中使用 OmicVerse MCP](t_mcp_claude_code.md)

## OmicVerse MCP 提供的功能

- 作为 MCP 工具暴露的 OmicVerse 分析工具
- 稳定的句柄，如 `adata_id`、`artifact_id` 和 `instance_id`
- 内置数据集，如 `ov.datasets.pbmc3k`、`ov.datasets.pbmc8k` 和 `ov.datasets.seqfish`
- AnnData 检查工具，如 `ov.adata.describe`、`ov.adata.peek` 和 `ov.adata.inspect`
- 两种本地传输方式：`stdio` 和 `streamable-http`

## 当前范围

在当前实现中：

- `P0`：15 个分析工具
- `P0.5`：13 个额外分析工具
- `P2`：5 个高级基于类的工具
- 元工具：25 个始终可用的工具
- `P0+P0.5+P2` 合计：58 个工具

## 内容迁移说明

### 安装、启动和首次分析

已迁移至：

- [快速开始](t_mcp_quickstart.md)
- [完整启动](t_mcp_full_start.md)

### 阶段系统、工具目录和依赖层

已迁移至：

- [工具目录](t_mcp_tools.md)

### 客户端配置

已迁移至：

- [客户端与部署](t_mcp_clients.md)

包括：

- `stdio`
- 本地 `streamable-http`
- Claude Code / Claude Desktop
- 远程 SSH 启动
- 本地与远程并行部署

### 会话、句柄、持久化、可观测性和故障排查

已迁移至：

- [运行时与故障排查](t_mcp_runtime.md)

### JSON-RPC 和原始客户端示例

已迁移至：

- [参考文档](t_mcp_reference.md)

## 最简示例

如果您只想要最短的有效流程：

```text
Load the built-in pbmc3k dataset
Describe the current adata
Run QC, scale, PCA with 50 components, build neighbors, compute UMAP, and run Leiden clustering
Plot the UMAP colored by leiden
```

使用[快速开始](t_mcp_quickstart.md)获取该流程背后的命令和配置片段。
