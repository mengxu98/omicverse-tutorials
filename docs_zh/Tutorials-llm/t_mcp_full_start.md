---
title: OmicVerse MCP 完整启动
---

# OmicVerse MCP 完整启动

本页面是 OmicVerse MCP 的完整入门路径。它位于简短的[快速开始](t_mcp_quickstart.md)与更专业的参考页面之间。

## 适用对象

如果符合以下情况，请阅读本页面：

- 快速开始内容过于简短
- 您希望一次性完成从配置到分析的完整演练
- 您希望了解命令和默认选择背后的原因

## 完成后您将拥有

阅读完本页面后，您将拥有：

- 一个运行中的 OmicVerse MCP 服务器
- 通过 `stdio` 或本地 HTTP 连接的客户端
- 以 `adata_id` 形式加载的数据集
- 完成的标准预处理工作流程
- 生成的图表和标记基因分析
- 可稍后恢复的持久化 `.h5ad` 文件

## 第 1 步：安装

```bash
pip install omicverse[mcp]
python -m omicverse.mcp --version
```

如果您从源码克隆工作：

```bash
pip install -e ".[mcp]"
```

## 第 2 步：选择传输方式

OmicVerse MCP 支持两种本地传输方式。

### 常用阶段选项

```bash
# 仅核心
python -m omicverse.mcp --phase P0

# 默认
python -m omicverse.mcp --phase P0+P0.5

# 包含高级 P2 工具
python -m omicverse.mcp --phase P0+P0.5+P2
```

### 选项 A：`stdio`

当您希望最简单的配置并让 Claude 管理 MCP 进程生命周期时使用此选项。

```bash
python -m omicverse.mcp --phase P0+P0.5
```

### 选项 B：`streamable-http`

当您希望独立管理 MCP 进程、获得更清晰的日志或更简便的重连行为时使用此选项。

```bash
NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/mpl \
python -m omicverse.mcp \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8765 \
  --http-path /mcp \
  --phase P0+P0.5
```

### 默认建议

从 `stdio` 开始。当需要调试、使用更大数据集或希望在重新连接后保持一个 MCP 进程活跃时，切换到本地 HTTP。

## 第 3 步：连接客户端

### 使用 `stdio` 的 Claude Code

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

如果您希望 Claude Code 直接启动完整的 P2 部署：

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

### 使用本地 HTTP 的 Claude Code

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

如果您使用 Claude Code，还可以阅读 [Claude Code 演练](t_mcp_claude_code.md)。

## 第 4 步：了解边界传递的内容

`AnnData` 对象保留在服务器端。客户端不会收到完整的内存对象，而是接收轻量级句柄，例如：

- 数据集的 `adata_id`
- 图表和文件的 `artifact_id`
- P2 基于类的工具的 `instance_id`

因此，典型的成功加载响应如下：

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

## 第 5 步：加载数据

您可以从内置数据集开始：

```text
Load the built-in pbmc3k dataset
```

或从本地文件加载：

```text
Load the pbmc3k.h5ad file
```

当前内置加载器包括：

- `ov.datasets.pbmc3k`
- `ov.datasets.pbmc8k`
- `ov.datasets.seqfish`

## 第 6 步：分析前先检查

在请求预处理之前，先检查当前数据集。这很重要，因为它可以让模型了解 `obs`、`var`、`obsm` 和 `uns` 中实际存在的内容。

有用的提示词：

```text
Describe the current adata
What is the first gene in var?
Does CD3D exist in var_names?
Inspect adata.obsm
Inspect adata.uns
Show value counts for leiden
```

这些会路由到：

- `ov.adata.describe`
- `ov.adata.peek`
- `ov.adata.find_var`
- `ov.adata.inspect`
- `ov.adata.value_counts`

## 第 7 步：运行标准工作流程

默认分析链为：

1. `ov.pp.qc`
2. `ov.pp.scale`
3. `ov.pp.pca`
4. `ov.pp.neighbors`
5. `ov.pp.umap`
6. `ov.pp.leiden`

自然语言请求：

```text
Run QC, scale, PCA with 50 components, build neighbors, compute UMAP, and run Leiden clustering at resolution 1.0
```

服务器强制执行前提条件。例如，PCA 需要 `scaled` 层，邻域图需要 `X_pca`。

## 第 8 步：绘图与解读

嵌入和聚类完成后，请求绘图：

```text
Plot the UMAP colored by leiden
Show me a violin plot of n_genes grouped by leiden cluster
Create a dot plot for genes CD3D, CD79A, LYZ, NKG7 grouped by leiden
```

通常使用：

- `ov.pl.embedding`
- `ov.pl.violin`
- `ov.pl.dotplot`

绘图输出会注册为 artifact。

## 第 9 步：标记基因分析与富集

聚类完成后，请求标记基因分析：

```text
Find marker genes for each Leiden cluster and show me the top 5 per cluster
Plot a marker gene dotplot
Run COSG to rank marker genes
Perform pathway enrichment on the marker genes
Plot the pathway enrichment results
```

可使用：

- `ov.single.find_markers`
- `ov.single.get_markers`
- `ov.pl.markers_dotplot`
- `ov.single.cosg`
- `ov.single.pathway_enrichment`
- `ov.single.pathway_enrichment_plot`

## 第 10 步：持久化与恢复

分析状态保存在内存中，直到您将其持久化。

保存：

```text
Save the current dataset to disk
```

稍后恢复：

```text
Restore the dataset from /path/to/file.h5ad
```

底层使用：

- `ov.persist_adata`
- `ov.restore_adata`

## 可选第 11 步：切换至 P2

如果您需要高级的基于类的工具，例如 DEG、注释、metacell、DCT 或主题建模，请以如下方式启动服务器：

```bash
python -m omicverse.mcp --phase P0+P0.5+P2
```

P2 工具可能出现在工具列表中，但若其可选依赖未安装，仍会不可用。

## 故障排查清单

### 工具缺失

- 验证 `--phase` 设置
- 让客户端运行 `ov.list_tools`

### 工具不可用

- 让客户端运行 `ov.describe_tool`
- 检查缺少的可选依赖

### 数据集句柄消失

- 服务器可能已重启
- 重新加载数据或使用 `ov.restore_adata`

### 长时间运行的任务难以调试

- 优先使用本地 HTTP 模式
- 使用 `ov.list_traces`、`ov.get_trace`、`ov.list_events` 和 `ov.get_health` 进行检查

## 提示与最佳实践

1. 从 `P0+P0.5` 开始。仅在需要高级基于类的工具时才添加 `+P2`。
2. 若希望保存的数据集跨会话保留，使用 `--persist-dir`。
3. 让客户端为您追踪 `adata_id`，而不是手动管理句柄。
4. 在请求解读 `obs`、`var`、`obsm` 或 `uns` 之前，使用 `ov.adata.*` 检查工具。
5. 需要前提条件或可用性详情时，使用 `ov.describe_tool`。
6. 当数据集或依赖栈超出本地机器能力时，使用远程部署。
7. 如计划稍后继续，在停止前请持久化数据。

## 后续步骤

- 最短路径：[快速开始](t_mcp_quickstart.md)
- 完整工具目录：[工具目录](t_mcp_tools.md)
- 部署模式：[客户端与部署](t_mcp_clients.md)
- 运行时详情：[运行时与故障排查](t_mcp_runtime.md)
- 精确的标志和信封：[参考文档](t_mcp_reference.md)
