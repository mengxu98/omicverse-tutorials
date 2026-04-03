# GenePT

⚠️ **状态：** 部分支持 | **版本：** v1.0

---

## 概述

基于 API 调用的 GPT-3.5 基因嵌入（1536 维），无需本地 GPU，以基因为单位（而非细胞）

!!! tip "何时选择 GenePT"

    适用于需要基因级嵌入（而非细胞级）、没有本地 GPU，或希望使用基于 API 的 OpenAI 嵌入的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | GenePT |
| **版本** | v1.0 |
| **任务** | `embed` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | symbol |
| **嵌入维度** | 1536 |
| **需要 GPU** | 否 |
| **最低显存** | 0 GB |
| **推荐显存** | 0 GB |
| **CPU 回退** | 是 |
| **适配器状态** | ⚠️ 部分支持 |

---

## 快速开始

```python
import omicverse as ov

# 1. 查看模型规格
info = ov.fm.describe_model("genept")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "genept", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="genept",
    adata_path="your_data.h5ad",
    output_path="output_genept.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_genept.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 无需本地预处理。生成嵌入需要 OpenAI API 密钥。 |
| **数据格式** | AnnData (`.h5ad`) |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_genept` | `adata.obsm` | 细胞嵌入向量（1536 维） |

```python
import scanpy as sc

adata = sc.read_h5ad("output_genept.h5ad")
embeddings = adata.obsm["X_genept"]  # shape: (n_cells, 1536)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_genept")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/yiqunchen/GenePT](https://github.com/yiqunchen/GenePT)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [GenePT 教程笔记本](t_fm_genept.ipynb)。
