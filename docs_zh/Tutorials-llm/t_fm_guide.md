---
title: "ov.fm — 基础模型模块"
---

# ov.fm — 基础模型模块

`ov.fm` 提供了一个**统一 API**，用于发现、选择、验证、运行和解读单细胞基础模型。它通过一致的基于 AnnData 的接口封装了 17+ 个模型（scGPT、Geneformer、UCE、scFoundation、CellPLM 等），并具备自动数据分析和模型选择功能。

!!! note "何时使用 ov.fm"

    当您希望将预训练基础模型应用于单细胞数据，同时无需手动配置每个模型的预处理流程时，请使用 `ov.fm`。它会自动为您处理基因 ID 转换、兼容性检查以及输出标准化。

---

## 快速开始

```python
import omicverse as ov

# 1. 查看可用模型
models = ov.fm.list_models(task="embed")

# 2. 分析您的数据
profile = ov.fm.profile_data("pbmc3k.h5ad")

# 3. 哪个模型最适合？
selection = ov.fm.select_model("pbmc3k.h5ad", task="embed")
print(selection["recommended"]["name"])

# 4. 数据是否准备就绪？
check = ov.fm.preprocess_validate("pbmc3k.h5ad", "scgpt", "embed")

# 5. 运行模型
result = ov.fm.run(task="embed", model_name="scgpt", adata_path="pbmc3k.h5ad",
                   output_path="pbmc3k_embedded.h5ad")

# 6. 可视化与评估
metrics = ov.fm.interpret_results("pbmc3k_embedded.h5ad", task="embed")
```

---

## 六步工作流程

`ov.fm` 围绕六个可组合步骤设计。您可以单独使用任何步骤，也可以将它们全部串联起来。

```
发现 ──▸ 分析 ──▸ 选择 ──▸ 验证 ──▸ 运行 ──▸ 解读
```

| 步骤 | 函数 | 目的 |
|------|----------|---------|
| **发现** | `list_models()`, `describe_model()` | 浏览可用模型及其功能 |
| **分析** | `profile_data()` | 检测物种、基因方案、模态及每个模型的兼容性 |
| **选择** | `select_model()` | 对模型进行评分和排序，以适配您的数据和任务 |
| **验证** | `preprocess_validate()` | 检查数据兼容性，获取自动修复建议 |
| **运行** | `run()` | 执行模型推理（嵌入、注释、整合等） |
| **解读** | `interpret_results()` | 计算指标（轮廓系数），生成 UMAP 可视化 |

---

## API 参考

### `ov.fm.list_models`

```python
ov.fm.list_models(task=None, skill_ready_only=False) -> dict
```

列出可用的基础模型，支持可选过滤。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `task` | str \| None | `None` | 按任务过滤：`"embed"`、`"annotate"`、`"integrate"`、`"perturb"`、`"spatial"`、`"drug_response"` |
| `skill_ready_only` | bool | `False` | 仅返回具有完整实现适配器的模型 |

**返回值：** 包含 `count`（整数）和 `models`（模型摘要列表）的字典。

```python
result = ov.fm.list_models(task="embed")
for m in result["models"]:
    print(f"{m['name']:15s} status={m['status']:10s} tasks={m['tasks']}")
```

---

### `ov.fm.describe_model`

```python
ov.fm.describe_model(model_name: str) -> dict
```

获取单个模型的完整规格，包括输入/输出约束、硬件要求和资源链接。

**返回值：** 包含 `model`、`input_contract`、`output_contract`、`resources` 键的字典。

```python
spec = ov.fm.describe_model("scgpt")
print(spec["input_contract"]["gene_id_scheme"])   # "symbol"
print(spec["output_contract"]["embedding_key"])    # "X_scGPT"
print(spec["output_contract"]["embedding_dim"])    # 512
```

---

### `ov.fm.profile_data`

```python
ov.fm.profile_data(adata_path: str) -> dict
```

分析 `.h5ad` 文件，返回包含自动物种/基因方案检测及每个模型兼容性评估的数据概况。

**返回值：** 包含 `n_cells`、`n_genes`、`species`、`gene_scheme`、`modality`、`has_raw`、`layers`、`obs_columns`、`obsm_keys`、`batch_columns`、`celltype_columns`、`model_compatibility` 的字典。

```python
profile = ov.fm.profile_data("pbmc3k.h5ad")
print(f"物种：{profile['species']}")
print(f"基因 ID：{profile['gene_scheme']}")

# 查看哪些模型兼容
for name, compat in profile["model_compatibility"].items():
    status = "OK" if compat["compatible"] else "ISSUES"
    print(f"  {name}: {status}")
```

---

### `ov.fm.select_model`

```python
ov.fm.select_model(
    adata_path: str,
    task: str,
    prefer_zero_shot: bool = True,
    max_vram_gb: int = None,
) -> dict
```

对给定数据集和任务的模型进行评分和排序。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `adata_path` | str | — | `.h5ad` 文件路径 |
| `task` | str | — | 任务类型（必填） |
| `prefer_zero_shot` | bool | `True` | 优先选择无需微调的模型 |
| `max_vram_gb` | int \| None | `None` | 最大显存限制 |

**返回值：** 包含 `recommended`（名称 + 理由）、`fallbacks`（列表）、`preprocessing_notes`、`data_profile` 的字典。

**评分逻辑：**

- Skill-ready 适配器：+100（就绪），+50（部分），0（参考）
- 零样本匹配：+30
- 基因方案匹配：+20
- 支持 CPU 回退：+10
- 低显存：+5

```python
result = ov.fm.select_model("pbmc3k.h5ad", task="embed", prefer_zero_shot=True)
print(f"推荐：{result['recommended']['name']}")
print(f"理由：{result['recommended']['rationale']}")
print(f"备选：{[f['name'] for f in result['fallbacks']]}")
```

---

### `ov.fm.preprocess_validate`

```python
ov.fm.preprocess_validate(
    adata_path: str,
    model_name: str,
    task: str,
) -> dict
```

验证数据与特定模型和任务的兼容性。返回诊断信息和自动修复建议。

**返回值：** 包含 `status`（`"ready"` | `"needs_preprocessing"` | `"incompatible"`）、`diagnostics`、`auto_fixes`、`data_summary` 的字典。

```python
result = ov.fm.preprocess_validate("pbmc3k.h5ad", "scgpt", "embed")
if result["status"] == "ready":
    print("数据已准备好用于 scGPT")
else:
    for diag in result["diagnostics"]:
        print(f"[{diag['severity']}] {diag['message']}")
    for fix in result["auto_fixes"]:
        print(f"建议修复：{fix['action']}")
        if "code" in fix:
            print(fix["code"])
```

---

### `ov.fm.run`

```python
ov.fm.run(
    task: str,
    model_name: str,
    adata_path: str,
    output_path: str = None,
    batch_key: str = None,
    label_key: str = None,
    device: str = "auto",
    batch_size: int = None,
    checkpoint_dir: str = None,
) -> dict
```

在您的数据上执行基础模型。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `task` | str | — | 任务类型（必填） |
| `model_name` | str | — | 模型名称（必填） |
| `adata_path` | str | — | 输入 `.h5ad` 的路径（必填） |
| `output_path` | str \| None | `None` | 输出路径（默认覆盖输入文件） |
| `batch_key` | str \| None | `None` | 批次对应的 `.obs` 列（`integrate` 任务需要） |
| `label_key` | str \| None | `None` | 细胞类型标签对应的 `.obs` 列 |
| `device` | str | `"auto"` | `"auto"`、`"cuda"`、`"cpu"`、`"mps"` |
| `batch_size` | int \| None | `None` | 覆盖模型默认批次大小 |
| `checkpoint_dir` | str \| None | `None` | 模型检查点目录路径 |

**返回值：** 成功时返回包含 `output_path`、`output_keys`、`n_cells`、`status` 的字典；失败时返回包含 `error`、`status` 的字典。

**执行流程：**

1. 通过 `preprocess_validate()` 验证数据
2. 尝试 conda 子进程执行（隔离环境）
3. 若 conda 不可用，回退至进程内适配器
4. 将结果和溯源元数据写入输出 AnnData

```python
result = ov.fm.run(
    task="embed",
    model_name="scgpt",
    adata_path="pbmc3k.h5ad",
    output_path="pbmc3k_embedded.h5ad",
    device="cuda",
)
if "error" not in result:
    print(f"输出键：{result['output_keys']}")
    print(f"处理细胞数：{result['n_cells']}")
```

---

### `ov.fm.interpret_results`

```python
ov.fm.interpret_results(
    adata_path: str,
    task: str,
    output_dir: str = None,
    generate_umap: bool = True,
    color_by: list = None,
) -> dict
```

为模型输出生成质量指标和可视化图表。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `adata_path` | str | — | 含模型结果的 `.h5ad` 路径 |
| `task` | str | — | 已执行的任务 |
| `output_dir` | str \| None | `None` | 可视化文件的输出目录 |
| `generate_umap` | bool | `True` | 是否生成 UMAP 图 |
| `color_by` | list \| None | `None` | 用于 UMAP 着色的 `.obs` 列 |

**计算的指标：**

- 嵌入维度和细胞数
- 轮廓系数（如有细胞类型标签且安装了 sklearn）
- 注释列检测
- 来自 `adata.uns["fm"]` 的溯源元数据

```python
result = ov.fm.interpret_results(
    "pbmc3k_embedded.h5ad",
    task="embed",
    generate_umap=True,
    color_by=["louvain"],
)
for key, info in result["metrics"]["embeddings"].items():
    print(f"{key}: dim={info['dim']}, silhouette={info.get('silhouette', 'N/A')}")
```

---

## 支持的任务

| 任务 | 描述 | 示例模型 |
|------|-------------|----------------|
| `embed` | 生成细胞嵌入用于下游分析 | scGPT, Geneformer, UCE, CellPLM |
| `annotate` | 预测细胞类型标签 | scGPT（微调版）, sccello, ChatCell |
| `integrate` | 跨数据集的批次整合 | scGPT, Geneformer, UCE |
| `perturb` | 扰动响应预测 | scFoundation, Tabula |
| `spatial` | 空间转录组学分析 | Nicheformer |
| `drug_response` | 药物响应建模 | scFoundation |

---

## 模型目录

### Skill-Ready 模型（完整适配器）

这些模型具有完整实现的适配器，可直接通过 `ov.fm.run()` 执行。

| 模型 | 版本 | 任务 | 物种 | 基因 ID | GPU | 最低显存 |
|-------|---------|-------|---------|----------|-----|----------|
| **scGPT** | whole-human-2024 | embed, integrate | human, mouse | symbol | 是 | 8 GB |
| **Geneformer** | v2-106M | embed, integrate | human | ensembl | 否（支持 CPU） | 4 GB |
| **UCE** | 4-layer | embed, integrate | 7 种物种 | symbol | 是 | 16 GB |

### 部分规格模型

这些模型具有部分规格。可用于模型选择和数据分析；执行能力取决于适配器可用性。

| 模型 | 任务 | 模态 | 核心特点 |
|-------|-------|------------|-------------------|
| **scFoundation** | embed, integrate | RNA | 19K 基因词表，扰动预训练 |
| **scBERT** | embed, integrate | RNA | BERT 风格掩码语言建模 |
| **GeneCompass** | embed, integrate | RNA | 1.2 亿细胞预训练语料 |
| **CellPLM** | embed, integrate | RNA | 以细胞为中心（非基因），高吞吐量 |
| **Nicheformer** | embed, integrate, spatial | RNA, Spatial | 感知微环境的空间建模 |
| **scMulan** | embed, integrate | RNA, ATAC, Protein, Multi-omics | 原生多组学 |
| **Tabula** | embed, annotate, integrate, perturb | RNA | 联邦学习 + FlashAttention |
| **tGPT** | embed, integrate | RNA | 自回归下一 token 预测 |
| **CellFM** | embed, integrate | RNA | MLP 架构，1.26 亿细胞 |
| **sccello** | embed, integrate, annotate | RNA | 通过细胞本体论进行零样本注释 |
| **scPRINT** | embed, integrate | RNA | 去噪 + 蛋白质编码基因专注 |
| **ATACformer** | embed, integrate | ATAC | 原生 ATAC-seq（基于 Peak） |
| **scPlantLLM** | embed, integrate | RNA | 植物专用（拟南芥、水稻、玉米） |
| **LangCell** | embed, integrate | RNA | 文本+细胞对齐，自然语言查询 |

!!! tip "模型选择速查表"

    - **默认（RNA，人类）：** scGPT
    - **Ensembl ID / 纯 CPU：** Geneformer
    - **跨物种：** UCE（支持 7 种物种）
    - **多组学（RNA+ATAC+蛋白质）：** scMulan
    - **空间转录组学：** Nicheformer
    - **仅 ATAC-seq：** ATACformer
    - **植物数据：** scPlantLLM
    - **大规模（100 万+ 细胞）：** CellPLM

---

## 数据类型与枚举

```python
from omicverse.fm import TaskType, Modality, GeneIDScheme, SkillReadyStatus
```

=== "TaskType"

    ```python
    TaskType.EMBED          # "embed"
    TaskType.ANNOTATE       # "annotate"
    TaskType.INTEGRATE      # "integrate"
    TaskType.PERTURB        # "perturb"
    TaskType.SPATIAL        # "spatial"
    TaskType.DRUG_RESPONSE  # "drug_response"
    ```

=== "Modality"

    ```python
    Modality.RNA         # "RNA"
    Modality.ATAC        # "ATAC"
    Modality.SPATIAL     # "Spatial"
    Modality.PROTEIN     # "Protein"
    Modality.MULTIOMICS  # "Multi-omics"
    ```

=== "GeneIDScheme"

    ```python
    GeneIDScheme.SYMBOL   # "symbol"  — HGNC 符号（如 TP53）
    GeneIDScheme.ENSEMBL  # "ensembl" — Ensembl ID（如 ENSG00000141510）
    GeneIDScheme.CUSTOM   # "custom"  — 模型特定词表
    ```

=== "SkillReadyStatus"

    ```python
    SkillReadyStatus.READY      # 完整适配器已实现
    SkillReadyStatus.PARTIAL    # 部分规格，需要验证
    SkillReadyStatus.REFERENCE  # 仅参考文档
    ```

---

## 插件系统

您可以通过编写插件来注册自定义基础模型。

### 入口点插件（pip 安装）

在您的 `pyproject.toml` 中：

```toml
[project.entry-points."omicverse.fm"]
my_model = "my_package.fm_plugin:register"
```

### 本地插件（开发用）

在 `~/.omicverse/plugins/fm/my_model.py` 创建文件：

```python
from omicverse.fm import ModelSpec, SkillReadyStatus, TaskType, Modality, GeneIDScheme
from omicverse.fm.adapters import BaseAdapter

MY_SPEC = ModelSpec(
    name="my_model",
    version="v1.0",
    skill_ready=SkillReadyStatus.PARTIAL,
    tasks=[TaskType.EMBED],
    modalities=[Modality.RNA],
    species=["human"],
    gene_id_scheme=GeneIDScheme.SYMBOL,
    zero_shot_embedding=True,
    embedding_dim=256,
)

class MyAdapter(BaseAdapter):
    def run(self, task, adata_path, output_path, **kwargs):
        ...  # 您的实现

    def _load_model(self, device):
        ...

    def _preprocess(self, adata, task):
        ...

    def _postprocess(self, adata, embeddings, task):
        ...

def register():
    """返回 (spec, adapter_class) 元组。"""
    return (MY_SPEC, MyAdapter)
```

!!! note

    插件不能覆盖内置模型。若发生名称冲突，插件将被跳过并发出警告。

---

## 注册表 API

对于高级用法，您可以直接查询模型注册表：

```python
from omicverse.fm import get_registry

registry = get_registry()

# 获取特定模型的规格
spec = registry.get("scgpt")
print(spec.embedding_dim)       # 512
print(spec.supports_task("embed"))  # True

# 查找符合条件的模型
matches = registry.find_models(
    task="embed",
    species="human",
    gene_scheme="symbol",
    zero_shot=True,
    max_vram_gb=16,
)
for m in matches:
    print(m.name, m.version)
```

---

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `OV_FM_CHECKPOINT_DIR` | 模型检查点的基础目录（`<base>/<model_name>/`） |
| `OV_FM_CHECKPOINT_DIR_SCGPT` | 模型专用检查点目录（适用于任何大写模型名） |
| `OV_FM_DISABLE_CONDA_SUBPROCESS` | 禁用 conda 子进程执行，仅使用进程内适配器 |

**检查点解析顺序：**

1. `ov.fm.run()` 中的 `checkpoint_dir` 参数
2. `OV_FM_CHECKPOINT_DIR_<MODEL>` 环境变量
3. `OV_FM_CHECKPOINT_DIR/<model_name>/`
4. 默认缓存：`~/.omicverse/models/<model_name>/`

---

## 错误处理

所有函数均通过结果字典返回错误信息，而非抛出异常：

```python
result = ov.fm.run(task="embed", model_name="scgpt", adata_path="data.h5ad")
if "error" in result:
    print(f"错误：{result['error']}")
    print(f"状态：{result['status']}")  # "not_implemented"、"incompatible" 等
```

常见错误信息：

| 错误 | 原因 |
|-------|-------|
| `Model 'xxx' not found` | 模型名称不在注册表中 |
| `File not found: xxx` | 文件路径无效 |
| `Expected .h5ad file` | 文件格式错误 |
| `No compatible models found` | 没有模型满足任务/数据约束 |
| `No adapter implemented for model 'xxx'` | 模型仅为参考文档，无适配器 |

---

## 动手教程

如需使用真实数据（PBMC 3K + scGPT）的逐步演练，请参阅
[基础模型教程笔记本](t_fm.ipynb)。
