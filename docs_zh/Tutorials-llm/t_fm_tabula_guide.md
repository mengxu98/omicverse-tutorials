# Tabula

⚠️ **状态：** 部分支持 | **版本：** federated-v1

---

## 概述

保护隐私的联邦学习 + 表格 Transformer，60697 基因词表，分位数分箱表达，支持 FlashAttention

!!! tip "何时选择 Tabula"

    适用于需要隐私保护分析、联邦训练嵌入，或使用表格建模方法进行扰动预测的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | Tabula |
| **版本** | federated-v1 |
| **任务** | `embed`, `annotate`, `integrate`, `perturb` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | custom (60,697 gene vocabulary) |
| **嵌入维度** | 192 |
| **需要 GPU** | 是 |
| **最低显存** | 8 GB |
| **推荐显存** | 16 GB |
| **CPU 回退** | 否 |
| **适配器状态** | ⚠️ 部分支持 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("tabula")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "tabula", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="tabula",
    adata_path="your_data.h5ad",
    output_path="output_tabula.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_tabula.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | custom (60,697 gene vocabulary) |
| **预处理** | 基因表达进行分位数分箱处理。模型使用其自有的 60,697 基因词表进行 tokenization。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |
| **标签键** | 用于细胞类型标签的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_tabula` | `adata.obsm` | 细胞嵌入向量（192 维） |
| `tabula_pred` | `adata.obs` | 预测的细胞类型标签 |

```python
import scanpy as sc

adata = sc.read_h5ad("output_tabula.h5ad")
embeddings = adata.obsm["X_tabula"]  # shape: (n_cells, 192)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_tabula")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/aristoteleo/tabula](https://github.com/aristoteleo/tabula)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [Tabula 教程笔记本](t_fm_tabula.ipynb)。
