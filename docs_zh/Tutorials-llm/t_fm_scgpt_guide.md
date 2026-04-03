# scGPT

✅ **状态：** 就绪 | **版本：** whole-human-2024

---

## 概述

多模态 Transformer（RNA+ATAC+空间），基于注意力机制的基因交互建模

!!! tip "何时选择 scGPT"

    适用于需要多模态分析（RNA+ATAC 或空间）或显式注意力机制基因交互图的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | scGPT |
| **版本** | whole-human-2024 |
| **任务** | `embed`, `integrate` |
| **模态** | RNA, ATAC, Spatial |
| **物种** | human, mouse |
| **基因 ID** | symbol (HGNC) |
| **嵌入维度** | 512 |
| **需要 GPU** | 是 |
| **最低显存** | 8 GB |
| **推荐显存** | 16 GB |
| **CPU 回退** | 是 |
| **适配器状态** | ✅ 就绪 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("scgpt")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "scgpt", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="scgpt",
    adata_path="your_data.h5ad",
    output_path="output_scgpt.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_scgpt.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol (HGNC) |
| **预处理** | 使用 `sc.pp.normalize_total` 归一化至 1e4，然后分箱为 51 个表达箱。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_scGPT` | `adata.obsm` | 细胞嵌入向量（512 维） |
| `scgpt_pred` | `adata.obs` | 预测的细胞类型标签 |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scgpt.h5ad")
embeddings = adata.obsm["X_scGPT"]  # shape: (n_cells, 512)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_scGPT")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/bowang-lab/scGPT#pretrained-scgpt-model-zoo](https://github.com/bowang-lab/scGPT#pretrained-scgpt-model-zoo)
- **论文：** [https://www.nature.com/articles/s41592-024-02201-0](https://www.nature.com/articles/s41592-024-02201-0)
- **文档：** [https://scgpt.readthedocs.io/](https://scgpt.readthedocs.io/)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [scGPT 教程笔记本](t_scgpt.ipynb)。
