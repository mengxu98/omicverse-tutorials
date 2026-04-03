# Geneformer

✅ **状态：** 就绪 | **版本：** v2-106M

---

## 概述

基于秩值编码的 Transformer，使用 Ensembl 基因 ID，支持 CPU 推理，融合网络生物学预训练

!!! tip "何时选择 Geneformer"

    适用于拥有 Ensembl 基因 ID、需要纯 CPU 推理，或希望获得基因网络感知嵌入的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | Geneformer |
| **版本** | v2-106M |
| **任务** | `embed`, `integrate` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | ensembl (ENSG...) |
| **嵌入维度** | 512 |
| **需要 GPU** | 否 |
| **最低显存** | 4 GB |
| **推荐显存** | 16 GB |
| **CPU 回退** | 是 |
| **适配器状态** | ✅ 就绪 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("geneformer")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "geneformer", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="geneformer",
    adata_path="your_data.h5ad",
    output_path="output_geneformer.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_geneformer.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | ensembl (ENSG...) |
| **预处理** | 秩值编码。使用 `geneformer.preprocess()` 进行正确的 tokenization。如存在 Ensembl 版本后缀（如 `.15`），请将其去除。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

!!! warning "基因 ID 转换"

    Geneformer 需要 Ensembl ID（如 `ENSG00000141510`）。若您的数据使用基因符号，请通过以下方式转换：
    ```python
    # ov.fm.preprocess_validate() 会自动检测并给出修复建议
    check = ov.fm.preprocess_validate("data.h5ad", "geneformer", "embed")
    print(check["auto_fixes"])  # 显示转换建议
    ```

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_geneformer` | `adata.obsm` | 细胞嵌入向量（512 维） |
| `geneformer_pred` | `adata.obs` | 预测的细胞类型标签 |

```python
import scanpy as sc

adata = sc.read_h5ad("output_geneformer.h5ad")
embeddings = adata.obsm["X_geneformer"]  # shape: (n_cells, 512)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_geneformer")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://huggingface.co/ctheodoris/Geneformer](https://huggingface.co/ctheodoris/Geneformer)
- **论文：** [https://www.nature.com/articles/s41586-023-06139-9](https://www.nature.com/articles/s41586-023-06139-9)
- **文档：** [https://geneformer.readthedocs.io/](https://geneformer.readthedocs.io/)
- **许可证：** Apache 2.0（代码部分）

---

## 动手教程

如需包含代码的逐步演练，请参阅 [Geneformer 教程笔记本](t_geneformer.ipynb)。
