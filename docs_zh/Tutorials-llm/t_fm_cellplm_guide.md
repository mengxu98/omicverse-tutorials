# CellPLM

✅ **状态：** 就绪 | **版本：** v1.0

---

## 概述

以细胞为中心（而非基因为中心）的架构，批次吞吐量最高（batch_size=128），推理速度快

!!! tip "何时选择 CellPLM"

    适用于需要快速推理、高吞吐量、百万级细胞处理，或细胞级（而非基因级）建模的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | CellPLM |
| **版本** | v1.0 |
| **任务** | `embed`, `integrate` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | symbol |
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
info = ov.fm.describe_model("cellplm")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "cellplm", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="cellplm",
    adata_path="your_data.h5ad",
    output_path="output_cellplm.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_cellplm.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 标准预处理。模型内部处理 tokenization。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_cellplm` | `adata.obsm` | 细胞嵌入向量（512 维） |

```python
import scanpy as sc

adata = sc.read_h5ad("output_cellplm.h5ad")
embeddings = adata.obsm["X_cellplm"]  # shape: (n_cells, 512)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_cellplm")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/OmicsML/CellPLM](https://github.com/OmicsML/CellPLM)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [CellPLM 教程笔记本](t_cellplm.ipynb)。
