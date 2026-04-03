# UCE

✅ **状态：** 就绪 | **版本：** 4-layer

---

## 概述

最广泛的物种支持（7 种物种），1280 维嵌入，通过蛋白质结构实现通用细胞嵌入

!!! tip "何时选择 UCE"

    适用于非人类/非小鼠物种（斑马鱼、蛙、猪、猕猴、狐猴），或需要跨物种比较的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | UCE |
| **版本** | 4-layer |
| **任务** | `embed`, `integrate` |
| **模态** | RNA |
| **物种** | human, mouse, zebrafish, mouse_lemur, macaque, frog, pig |
| **基因 ID** | symbol |
| **嵌入维度** | 1280 |
| **需要 GPU** | 是 |
| **最低显存** | 16 GB |
| **推荐显存** | 16 GB |
| **CPU 回退** | 否 |
| **适配器状态** | ✅ 就绪 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("uce")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "uce", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="uce",
    adata_path="your_data.h5ad",
    output_path="output_uce.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_uce.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 标准对数归一化。模型内部处理 tokenization。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_uce` | `adata.obsm` | 细胞嵌入向量（1280 维） |

```python
import scanpy as sc

adata = sc.read_h5ad("output_uce.h5ad")
embeddings = adata.obsm["X_uce"]  # shape: (n_cells, 1280)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_uce")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/snap-stanford/UCE](https://github.com/snap-stanford/UCE)
- **论文：** [https://www.nature.com/articles/s41592-024-02201-0](https://www.nature.com/articles/s41592-024-02201-0)
- **文档：** [https://github.com/snap-stanford/UCE](https://github.com/snap-stanford/UCE)
- **许可证：** MIT License

---

## 动手教程

如需包含代码的逐步演练，请参阅 [UCE 教程笔记本](t_uce.ipynb)。
