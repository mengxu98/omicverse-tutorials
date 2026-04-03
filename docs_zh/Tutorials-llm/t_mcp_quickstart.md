---
title: OmicVerse MCP 快速开始
---

# OmicVerse MCP 快速开始

这是搭建 OmicVerse MCP 的最短路径。

## 前提条件

开始之前，请确认您已准备好：

- Claude Code 或其他 MCP 客户端
- Python `>=3.10`
- 本地 `.h5ad` 文件，或愿意使用内置数据集

## 安装

```bash
pip install omicverse[mcp]
python -m omicverse.mcp --version
```

## 启动服务器

### 常用阶段选项

```bash
# 仅核心
python -m omicverse.mcp --phase P0

# 默认：核心 + 分析/可视化
python -m omicverse.mcp --phase P0+P0.5

# 完整部署，包含 P2 基于类的工具
python -m omicverse.mcp --phase P0+P0.5+P2
```

### 默认 `stdio` 模式

```bash
python -m omicverse.mcp --phase P0+P0.5
```

### 本地 HTTP 模式

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/mpl \
python -m omicverse.mcp \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8765 \
  --http-path /mcp \
  --phase P0+P0.5
```

默认使用 `stdio`。当您希望独立管理 MCP 进程或进行服务器端调试时，使用本地 HTTP。

如需高级的基于类的工具，使用相同的启动方式，但加上 `--phase P0+P0.5+P2`。

## Claude Code 配置

### 选项 A：Claude 直接启动 OmicVerse

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

使用 P2：

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

### 选项 B：Claude 连接到您的本地 HTTP MCP

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

更多部署模式请参阅[客户端与部署](t_mcp_clients.md)。

## 首先尝试的命令

### 加载内置数据集

```text
Load the built-in pbmc3k dataset
```

或加载文件：

```text
Load the pbmc3k.h5ad file
```

### 检查数据集

```text
Describe the current adata
What is the first gene in var?
Does CD3D exist in var_names?
Inspect adata.uns
Inspect adata.obsm
```

### 运行标准预处理工作流程

```text
Run QC, scale, PCA with 50 components, build neighbors, compute UMAP, and run Leiden clustering at resolution 1.0
```

### 绘图与汇总

```text
Plot the UMAP colored by leiden
Find marker genes for each Leiden cluster
Plot a marker gene dotplot
```

## 服务器实际在做什么

在底层，OmicVerse MCP 调用如下工具：

1. `ov.datasets.pbmc3k` 或 `ov.utils.read`
2. `ov.pp.qc`
3. `ov.pp.scale`
4. `ov.pp.pca`
5. `ov.pp.neighbors`
6. `ov.pp.umap`
7. `ov.pp.leiden`

数据集保留在服务器端，通过 `adata_id` 引用。

## 您将看到的最简 JSON 格式

加载数据通常返回如下对象引用：

```json
{
  "ok": true,
  "tool_name": "ov.utils.read",
  "outputs": [
    {
      "type": "object_ref",
      "ref_type": "adata",
      "ref_id": "adata_a1b2c3d4e5f6"
    }
  ]
}
```

通常您不需要手动管理 `adata_id`，因为 Claude 会在对话中自动追踪它。

## 一个简短的演练

1. `Load the built-in pbmc3k dataset`
2. `Describe the current adata`
3. `Run QC, scale, PCA with 50 components, build neighbors, compute UMAP, and run Leiden clustering`
4. `Plot the UMAP colored by leiden`
5. `Find marker genes for each Leiden cluster and show the top 5`

## 后续页面

- 完整入门路径：[完整启动](t_mcp_full_start.md)
- 完整工具列表：[工具目录](t_mcp_tools.md)
- Claude 和部署详情：[客户端与部署](t_mcp_clients.md)
- 运行时行为和故障排查：[运行时与故障排查](t_mcp_runtime.md)
