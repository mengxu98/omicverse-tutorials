# scPlantLLM

⚠️ **状态：** 部分支持 | **版本：** v1.0

---

## 概述

植物专用单细胞模型，处理多倍性和植物基因命名体系

!!! tip "何时选择 scPlantLLM"

    适用于拥有植物单细胞数据（拟南芥、水稻、玉米等）或涉及多倍性问题的场景

---

## 规格参数

| 属性 | 值 |
|----------|-------|
| **模型** | scPlantLLM |
| **版本** | v1.0 |
| **任务** | `embed`, `integrate` |
| **模态** | RNA |
| **物种** | plant (Arabidopsis, rice, maize, etc.) |
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
info = ov.fm.describe_model("scplantllm")

# 2. 分析您的数据
profile = ov.fm.profile_data("your_data.h5ad")

# 3. 验证兼容性
check = ov.fm.preprocess_validate("your_data.h5ad", "scplantllm", "embed")

# 4. 运行推理
result = ov.fm.run(
    task="embed",
    model_name="scplantllm",
    adata_path="your_data.h5ad",
    output_path="output_scplantllm.h5ad",
    device="auto",
)

# 5. 解读结果
metrics = ov.fm.interpret_results("output_scplantllm.h5ad", task="embed")
```

---

## 输入要求

| 要求 | 详情 |
|-------------|--------|
| **基因 ID 方案** | symbol |
| **预处理** | 使用植物基因命名体系进行标准预处理。模型处理多倍性特有的挑战。 |
| **数据格式** | AnnData (`.h5ad`) |
| **批次键** | 用于批次整合的 `.obs` 列（可选） |

---

## 输出键

运行 `ov.fm.run()` 后，结果存储在 AnnData 对象中：

| 键 | 位置 | 描述 |
|-----|----------|-------------|
| `X_scplantllm` | `adata.obsm` | 细胞嵌入向量（512 维） |

```python
import scanpy as sc

adata = sc.read_h5ad("output_scplantllm.h5ad")
embeddings = adata.obsm["X_scplantllm"]  # shape: (n_cells, 512)

# 下游分析
sc.pp.neighbors(adata, use_rep="X_scplantllm")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)
sc.pl.umap(adata, color=["leiden"])
```

---

## 参考资源

- **仓库 / 检查点：** [https://github.com/scPlantLLM/scPlantLLM](https://github.com/scPlantLLM/scPlantLLM)
- **许可证：** 请查阅上游 LICENSE

---

## 动手教程

如需包含代码的逐步演练，请参阅 [scPlantLLM 教程笔记本](t_fm_scplantllm.ipynb)。
