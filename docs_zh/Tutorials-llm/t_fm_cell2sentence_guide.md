# Cell2Sentence

⚠️ **状态：** 部分支持 | **版本：** v1.0

---

## 概述

将细胞转换为文本句子，用于 LLM 微调，生成 768 维 LLM 嵌入向量

!!! tip "何时选择 Cell2Sentence"

    适用于希望利用通用 LLM、将细胞转换为文本，或使用 LLM 微调工作流程的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | Cell2Sentence |
| **版本** | v1.0 |
| **任务** | `embed` |
| **模态** | RNA |
| **物种** | human |
| **基因 ID** | symbol |
| **嵌入维度** | 768 |
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
info = ov.fm.describe_model("cell2sentence")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "cell2sentence", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="cell2sentence",
    adata_path="your_data.h5ad",
    output_path="output_cell2sentence.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_cell2sentence.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 需要在参考数据上进行微调。基因表达会被转换为排序基因句子。 |
| **数据格式** | AnnData (`.h5ad`) |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_cell2sentence` | `adata.obsm` | 细胞嵌入向量（768 维） |

```python
import scanpy as sc

adata = sc.read_h5ad("output_cell2sentence.h5ad")
embeddings = adata.obsm["X_cell2sentence"]  # shape: (n_cells, 768)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_cell2sentence")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/vandijklab/cell2sentence](https://github.com/vandijklab/cell2sentence)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [Cell2Sentence 教程笔记本](t_fm_cell2sentence.ipynb)。
