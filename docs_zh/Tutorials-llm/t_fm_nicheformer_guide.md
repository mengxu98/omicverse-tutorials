# Nicheformer

⚠️ **状态：** 部分支持 | **版本：** v1.0

---

## 概述

感知微环境的空间 Transformer，联合建模空间坐标与基因表达

!!! tip "何时选择 Nicheformer"

    适用于拥有空间转录组学数据（Visium、MERFISH、Slide-seq）并希望获得微环境感知或空间上下文嵌入的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | Nicheformer |
| **版本** | v1.0 |
| **任务** | `embed`, `integrate`, `spatial` |
| **模态** | RNA, Spatial |
| **物种** | human, mouse |
| **基因 ID** | symbol |
| **嵌入维度** | 512 |
| **需要 GPU** | 是 |
| **最低显存** | 16 GB |
| **推荐显存** | 32 GB |
| **CPU 回退** | 否 |
| **适配器状态** | ⚠️ 部分支持 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("nicheformer")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "nicheformer", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="nicheformer",
    adata_path="your_data.h5ad",
    output_path="output_nicheformer.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_nicheformer.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 标准预处理。对于空间任务，请在 `adata.obsm['spatial']` 中包含空间坐标。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_nicheformer` | `adata.obsm` | 细胞嵌入向量（512 维） |

```python
import scanpy as sc

adata = sc.read_h5ad("output_nicheformer.h5ad")
embeddings = adata.obsm["X_nicheformer"]  # shape: (n_cells, 512)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_nicheformer")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/theislab/nicheformer](https://github.com/theislab/nicheformer)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [Nicheformer 教程笔记本](t_fm_nicheformer.ipynb)。
