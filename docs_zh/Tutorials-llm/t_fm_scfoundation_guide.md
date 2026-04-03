# scFoundation

✅ **状态：** 就绪 | **版本：** xTrimoGene

---

## 概述

大规模非对称 Transformer（xTrimoGene），自定义 19264 基因词表，针对扰动/药物响应任务进行预训练

!!! tip "何时选择 scFoundation"

    适用于需要扰动预测、药物响应建模，或使用 xTrimoGene 基因词表的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | scFoundation |
| **版本** | xTrimoGene |
| **任务** | `embed`, `integrate` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | custom (19,264 gene set) |
| **嵌入维度** | 512 |
| **需要 GPU** | 是 |
| **最低显存** | 16 GB |
| **推荐显存** | 32 GB |
| **CPU 回退** | 否 |
| **适配器状态** | ✅ 就绪 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("scfoundation")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "scfoundation", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="scfoundation",
    adata_path="your_data.h5ad",
    output_path="output_scfoundation.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_scfoundation.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | custom (19,264 gene set) |
| **预处理** | 将基因与模型词表对齐。遵循 xTrimoGene 预处理流程。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_scfoundation` | `adata.obsm` | 细胞嵌入向量（512 维） |
| `scfoundation_pred` | `adata.obs` | 预测的细胞类型标签 |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scfoundation.h5ad")
embeddings = adata.obsm["X_scfoundation"]  # shape: (n_cells, 512)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_scfoundation")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/biomap-research/scFoundation](https://github.com/biomap-research/scFoundation)
- **论文：** [https://www.nature.com/articles/s41592-024-02305-7](https://www.nature.com/articles/s41592-024-02305-7)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [scFoundation 教程笔记本](t_scfoundation.ipynb)。
