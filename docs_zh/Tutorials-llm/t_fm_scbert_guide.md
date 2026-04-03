# scBERT

⚠️ **状态：** 部分支持 | **版本：** v1.0

---

## 概述

紧凑型 200 维嵌入，BERT 风格掩码基因预训练，轻量级模型

!!! tip "何时选择 scBERT"

    适用于需要紧凑型 200 维嵌入、BERT 风格预训练，或在资源受限硬件上使用轻量级模型的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | scBERT |
| **版本** | v1.0 |
| **任务** | `embed`, `integrate` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | symbol |
| **嵌入维度** | 200 |
| **需要 GPU** | 是 |
| **最低显存** | 8 GB |
| **推荐显存** | 16 GB |
| **CPU 回退** | 是 |
| **适配器状态** | ⚠️ 部分支持 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("scbert")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "scbert", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="scbert",
    adata_path="your_data.h5ad",
    output_path="output_scbert.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_scbert.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 标准对数归一化和基因筛选。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_scBERT` | `adata.obsm` | 细胞嵌入向量（200 维） |
| `scbert_pred` | `adata.obs` | 预测的细胞类型标签 |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scbert.h5ad")
embeddings = adata.obsm["X_scBERT"]  # shape: (n_cells, 200)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_scBERT")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/TencentAILabHealthcare/scBERT](https://github.com/TencentAILabHealthcare/scBERT)
- **论文：** [https://www.nature.com/articles/s42256-022-00534-z](https://www.nature.com/articles/s42256-022-00534-z)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [scBERT 教程笔记本](t_fm_scbert.ipynb)。
