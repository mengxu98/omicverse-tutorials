---
title: OmicVerse MCP 客户端与部署
---

# OmicVerse MCP 客户端与部署

本页面介绍如何将客户端连接到 OmicVerse MCP，以及何时使用各种传输方式。

## 架构

```
┌─────────────────┐     MCP transport      ┌──────────────────────┐
│   Claude Code   │◄──────────────────────►│  OmicVerse MCP Server│
│   or another    │   adata_id / results   │  (local or remote)   │
│   MCP client    │                        │                      │
└─────────────────┘                        │  AnnData in memory   │
                                           │  Artifacts on disk   │
                                           └──────────────────────┘
```

原始 `AnnData` 不会越过协议边界。服务器将其存储在内存中，并返回轻量级句柄（如 `adata_id`）。

## 传输模式

## 常用启动命令

```bash
# 仅核心
python -m omicverse.mcp --phase P0

# 默认本地工作流程
python -m omicverse.mcp --phase P0+P0.5

# 启用高级的基于类的工具
python -m omicverse.mcp --phase P0+P0.5+P2
```

### `stdio`

Claude 或其他 MCP 客户端将 `python -m omicverse.mcp` 作为子进程启动，并通过标准输入/输出进行 JSON-RPC 通信。

适用场景：

- 您希望最简单的配置
- 客户端应管理 MCP 进程的生命周期
- 本地的短到中等时长分析

### `streamable-http`

您自行启动 OmicVerse MCP，客户端连接到本地 URL（如 `http://127.0.0.1:8765/mcp`）。

适用场景：

- 您希望 MCP 进程在重新连接后仍然保持运行
- 您希望直接访问服务器端日志
- 您希望对较大或较长时间运行的任务进行更清晰的故障隔离

## Claude Code

### 选项 A：`stdio`

```json
{
  "mcpServers": {
    "omicverse": {
      "command": "python",
      "args": ["-m", "omicverse.mcp", "--phase", "P0+P0.5"]
    }
  }
}
```

从 Claude Code 暴露 P2 工具：

```json
{
  "mcpServers": {
    "omicverse": {
      "command": "python",
      "args": ["-m", "omicverse.mcp", "--phase", "P0+P0.5+P2"]
    }
  }
}
```

### 选项 B：本地 HTTP

启动服务器：

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/mpl \
python -m omicverse.mcp \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8765 \
  --http-path /mcp \
  --phase P0+P0.5
```

然后配置 Claude Code：

```json
{
  "mcpServers": {
    "omicverse": {
      "type": "http",
      "url": "http://127.0.0.1:8765/mcp"
    }
  }
}
```

本地 HTTP 模式包含一个专为本地客户端设计的最简本地 OAuth 流程。

## Claude Desktop

Claude Desktop 使用相同的两种模式：

- 当 Claude 应直接启动 OmicVerse 时使用 `stdio`
- 当 OmicVerse 作为独立的本地 MCP 服务器运行时使用本地 HTTP

配置格式与 Claude Code 完全相同。

## 远程 / SSH 部署

您也可以在远程机器上运行 OmicVerse MCP，并让 Claude 通过 SSH 启动它：

```json
{
  "mcpServers": {
    "omicverse-remote": {
      "type": "stdio",
      "command": "ssh",
      "args": [
        "user@remote-host",
        "cd /path/to/project && python -m omicverse.mcp --phase P0+P0.5+P2 --persist-dir /data/ov_persist"
      ]
    }
  }
}
```

需要时可添加明确的 SSH 选项：

```json
{
  "mcpServers": {
    "omicverse-remote": {
      "type": "stdio",
      "command": "ssh",
      "args": [
        "-i", "/path/to/ssh/key",
        "-p", "22",
        "-o", "StrictHostKeyChecking=no",
        "user@remote-host",
        "cd /path/to/project && python -m omicverse.mcp --phase P0+P0.5+P2 --persist-dir /data/ov_persist"
      ]
    }
  }
}
```

适用场景：

- 数据已存储在远程存储上
- RAM 或 GPU 需求超出笔记本电脑限制
- 需要持久的共享持久化目录

## 本地与远程并行使用

您可以在一个配置中同时定义本地和远程服务器：

```json
{
  "mcpServers": {
    "omicverse-local": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "omicverse.mcp", "--phase", "P0+P0.5", "--persist-dir", "/tmp/ov_persist_local"]
    },
    "omicverse-remote": {
      "type": "stdio",
      "command": "ssh",
      "args": [
        "user@gpu-server",
        "cd /data/project && python -m omicverse.mcp --phase P0+P0.5+P2 --persist-dir /data/ov_persist"
      ]
    }
  }
}
```

适用场景：

- 本地服务器处理快速预处理和检查
- 远程服务器处理更大的数据集或带有可选依赖的 P2 工具

### 句柄隔离

每个服务器都有自己的会话命名空间。来自一个服务器的 `adata_id` 不能在另一个服务器上使用。若需在服务器之间移动数据，请使用持久化和恢复功能。

## 哪种模式更好

### 对于大多数用户

使用 `stdio`。

它更简短、更简单，通常也是最不容易出错的配置。

### 对于大型数据集或较长任务

使用本地 `streamable-http`。

传输速度并无差异，但进程边界更易于观察和管理。当长时间的 PCA、邻域图构建或 UMAP 步骤需要调试或重连处理时，这一点尤为重要。

## 推荐模式

### 小到中型本地分析

- `stdio`
- `P0+P0.5`

### 大型本地分析

- 本地 `streamable-http`
- 持久化日志
- 可选 `--persist-dir`

### 远程计算

- SSH 启动的 `stdio`
- 远程持久化
- 若已安装扩展依赖则使用 `P0+P0.5+P2`

## 部署对比

| | 本地 | 远程 (SSH) |
|---|---|---|
| **延迟** | 即时 | SSH 开销 |
| **数据位置** | 必须在本地 | 保留在远程文件系统 |
| **计算能力** | 笔记本电脑受限 | 高 RAM / GPU / 多核 |
| **典型阶段** | `P0+P0.5` | `P0+P0.5+P2` |
| **持久化** | 本地磁盘 | 远程共享存储 |

## 远程环境提示

- 如需可使用明确的 `conda` 或 `micromamba` Python 路径
- 添加 MCP 配置前请先验证 SSH 连接
- 确保远程机器上已安装 `omicverse[mcp]`
- 对非标准 SSH 端口使用 `-p <port>`
- 对 SSH 密钥认证使用 `-i /path/to/key`
- 强烈推荐使用无密码登录

## 相关页面

- 快速配置：[快速开始](t_mcp_quickstart.md)
- Claude 专属演练：[在 Claude Code 中使用 OmicVerse MCP](t_mcp_claude_code.md)
- 运行时行为：[运行时与故障排查](t_mcp_runtime.md)
