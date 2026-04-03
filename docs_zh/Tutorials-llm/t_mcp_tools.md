---
title: OmicVerse MCP 工具目录
---

# OmicVerse MCP 工具目录

当前 MCP 服务器最多暴露 58 个工具：

- `P0`：15 个分析工具
- `P0.5`：13 个额外分析工具
- `P2`：5 个高级基于类的工具
- 元工具：25 个始终可用的工具

## 阶段系统概述

| 阶段 | 工具数 | 描述 |
|-------|-------|-------------|
| **P0** | 15 | 核心单细胞流程、内置数据集和基本预处理 |
| **P0.5** | 13 | 标记基因、通路分析和可视化 |
| **P2** | 5 | 高级基于类的工具 |
| **Meta** | 25 | 发现、AnnData 检查、会话、可观测性、artifact、安全 |
| **总计** | **58** | |

## P0：核心流程与数据访问

| 工具 | 描述 | 关键参数 |
|------|-------------|----------------|
| `ov.utils.read` | 加载文件并返回 `adata_id` | `path` |
| `ov.datasets.pbmc3k` | 加载内置 PBMC3k | — |
| `ov.datasets.pbmc8k` | 加载内置 PBMC8k | — |
| `ov.datasets.seqfish` | 加载内置 seqFISH | — |
| `ov.pp.qc` | 计算 QC 指标 | `adata_id` |
| `ov.pp.filter_cells` | 筛选细胞 | `adata_id`，阈值 |
| `ov.pp.filter_genes` | 筛选基因 | `adata_id`，阈值 |
| `ov.pp.log1p` | 对数转换表达量 | `adata_id` |
| `ov.pp.highly_variable_genes` | 识别高变基因 | `adata_id` |
| `ov.pp.scale` | 缩放表达量并创建 `scaled` 层 | `adata_id` |
| `ov.pp.pca` | 计算 PCA | `adata_id`, `n_pcs` |
| `ov.pp.neighbors` | 构建邻域图 | `adata_id` |
| `ov.pp.umap` | 计算 UMAP | `adata_id` |
| `ov.pp.leiden` | Leiden 聚类 | `adata_id`, `resolution` |
| `ov.pp.louvain` | Louvain 聚类 | `adata_id`, `resolution` |

**流程顺序**：`read` 或 `ov.datasets.*` -> `qc` / 筛选 -> `log1p` / HVG -> `scale` -> `pca` -> `neighbors` -> `umap` / 聚类

典型提示词：

- `Load the built-in seqfish dataset`
- `Run QC and identify highly variable genes`
- `Run PCA with 50 components`

## P0.5：分析与可视化

| 工具 | 描述 | 关键参数 |
|------|-------------|----------------|
| `ov.single.find_markers` | 差异标记基因发现 | `adata_id` |
| `ov.single.get_markers` | 提取标记基因表格 | `adata_id`, `n_markers` |
| `ov.single.cosg` | 使用 COSG 对标记基因排序 | `adata_id` |
| `ov.single.pathway_enrichment` | 通路富集分析 | 标记基因集或结果句柄 |
| `ov.single.pathway_enrichment_plot` | 绘制富集结果 | 富集结果 |
| `ov.pl.embedding` | 通用嵌入图 | `adata_id`, `color`, `save` |
| `ov.pl.violin` | 小提琴图 | `adata_id`, `keys`, `groupby` |
| `ov.pl.dotplot` | 点图 | `adata_id`, `var_names`, `groupby` |
| `ov.pl.markers_dotplot` | 标记基因点图 | `adata_id` |
| `ov.pl.umap` | UMAP 绘图助手 | `adata_id`, `color` |
| `ov.pl.tsne` | tSNE 绘图助手 | `adata_id`, `color` |
| `ov.pl.rank_genes_groups_dotplot` | 排序标记基因点图 | `adata_id` |
| `ov.pl.marker_heatmap` | 标记基因热图 | `adata_id` |

典型提示词：

- `Find marker genes for each Leiden cluster`
- `Run COSG to rank marker genes`
- `Perform pathway enrichment on the markers`
- `Plot a marker heatmap`

## P2：高级基于类的工具

这些工具暴露了 `create -> run -> results -> destroy` 等生命周期。

| 工具 | 描述 |
|------|-------------|
| `ov.bulk.pydeg` | 差异表达分析 |
| `ov.single.pyscsa` | 自动细胞注释 |
| `ov.single.metacell` | Metacell 构建 |
| `ov.single.dct` | 差异细胞组成 |
| `ov.utils.lda_topic` | 主题建模 |

这些工具可能出现在 `ov.list_tools` 中，但若可选依赖缺失，仍会返回 `tool_unavailable`。

P2 工具使用多操作生命周期，例如：

1. `create`
2. `run` / `annotate` / `train`
3. `results` / `predict`
4. `destroy`

### 运行时环境状态

OmicVerse 根据经过测试的依赖栈验证工具可用性：

- **core-runtime**：已验证（`anndata`、`scanpy`、`scipy`）
- **scientific-runtime**：已验证（`+ scvelo`、`squidpy`）
- **extended-runtime**：受限（`SEACells` 可用；`mira-multiome` 当前被阻止）

使用 `ov.describe_tool` 检查特定工具是否可在您的环境中运行。

## AnnData 检查工具

这些工具很重要，因为它们让客户端可以检查当前数据集，而不是靠猜测。

| 工具 | 用途 |
|------|-----|
| `ov.adata.describe` | 形状、名称、层、嵌入、元数据的高级摘要 |
| `ov.adata.peek` | 预览 `obs`、`var`、`obsm`、`layers` 或 `uns` 等槽 |
| `ov.adata.find_var` | 在 `var_names` 中搜索基因，如 `CD3D` |
| `ov.adata.value_counts` | 统计 `obs` 列中的值 |
| `ov.adata.inspect` | 检查 `obsm`、`obsp`、`layers`、`varm` 或 `uns` 中的嵌套条目 |

典型提示词：

- `Describe the current adata`
- `What is the first gene in var?`
- `Does CD3D exist in var_names?`
- `Show value counts for leiden`
- `Inspect adata.obsm X_pca`
- `Inspect adata.uns`

## 元工具

元工具始终可用，与阶段选择无关。

### 发现

- `ov.list_tools`
- `ov.search_tools`
- `ov.describe_tool`

### 会话与持久化

- `ov.get_session`
- `ov.list_handles`
- `ov.persist_adata`
- `ov.restore_adata`

### 可观测性

- `ov.get_metrics`
- `ov.list_events`
- `ov.get_trace`
- `ov.list_traces`

### Artifact 管理

- `ov.list_artifacts`
- `ov.describe_artifact`
- `ov.register_artifact`
- `ov.delete_artifact`
- `ov.cleanup_artifacts`
- `ov.export_artifacts_manifest`

Artifact 类型：`file`、`image`、`table`、`json`、`plot`、`report`、`export`

### 运行时安全

- `ov.get_limits`
- `ov.cleanup_runtime`
- `ov.get_health`

## 依赖层级

| 层级 | 包 | 解锁的工具 | 安装方式 |
|------|----------|----------------|---------|
| **核心** | `anndata`、`scanpy`、`numpy`、`scipy`、`matplotlib` | P0 + P0.5 | `pip install omicverse[mcp]` |
| **科学** | + `scvelo`、`squidpy` | 速度分析与空间分析 | `pip install -r requirements/mcp-scientific-runtime.txt` |
| **扩展** | + `SEACells`、`pertpy` | P2 类工具 | `pip install -r requirements/mcp-extended-runtime.txt` |

### 检查您的环境

- 请客户端运行 `ov.get_health` 以获取轻量级运行时摘要。
- 运行 `ov.get_limits` 查看配额和句柄使用情况。
- 若需要某个特定工具的可用性和依赖详情，运行 `ov.describe_tool`。

## 在相似工具之间做选择

- 当内置教程数据集足够时，优先使用 `ov.datasets.*` 而非文件加载。
- 在请求模型推断 `obs`、`var`、`obsm` 或 `uns` 中的内容之前，优先使用 `ov.adata.*`。
- 当您希望一个通用的嵌入绘图入口时，优先使用 `ov.pl.embedding`。
- 当您希望明确指定图表类型时，使用 `ov.pl.umap` 或 `ov.pl.tsne`。

## 相关页面

- 配置：[快速开始](t_mcp_quickstart.md)
- 部署：[客户端与部署](t_mcp_clients.md)
- 运行时行为：[运行时与故障排查](t_mcp_runtime.md)
