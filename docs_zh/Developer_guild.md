# 开发者指南

!!! Note
    为了更好地理解以下指南，您可以先阅读我们的 [论文](https://doi.org/10.1101/2023.06.06.543913)，了解总体思路。

以下将介绍框架的主要组件以及如何扩展现有实现。

## 框架结构

omicverse 的代码存放在 GitHub 仓库的 [omicverse 文件夹](https://github.com/Starlitnightly/omicverse/tree/master/omicverse) 中，
`__init__.py` 文件负责处理库函数的导入。

omicverse 框架主要由 5 个组件构成：

- `utils`：通用函数，包括数据处理、绘图等。
- `pp`：预处理，包括质量控制、归一化等。
- `bulk`：用于分析 bulk 组学测序数据，如 RNA-seq 或 Proper-seq。
- `single`：用于分析单细胞组学测序数据，如 scRNA-seq 或 scATAC-seq。
- `space`：用于分析空间 RNA-seq 数据。
- `bulk2single`：用于整合 bulk RNA-seq 与单细胞 RNA-seq。
- `external`：包含更多相关模块，避免安装冲突。

`__init__.py` 文件负责导入各文件夹内的函数入口，所有函数均使用以 `_*.py` 开头的文件进行编写。


## 面向开发者

### external 模块

在大多数情况下，我们意识到编写模块函数是比较困难的。因此，我们引入了 `external` 模块。
我们可以直接从 GitHub 克隆整个包，然后将整个文件夹移动到 `external` 文件夹中。
在此过程中，需要注意许可证是否允许，以及是否与 OmicVerse 的 GPL 许可证存在冲突。
随后，我们需要修改 `import` 内容，将不属于 OmicVerse 依赖的包从顶层导入改为函数级导入。

````shell
.
├── omicverse
├───── external
├──────── STT
├─────────── __init__.py
├─────────── pl
├─────────── tl
````

所有导入都需确保不存在冲突。

以下是一个错误示例，因为该包不在 OmicVerse 默认的 requirements.txt 中：

```python

import dgl

def calculate():
    dgl.run()
    pass

```

正确的导入方式为：

```python

def calculate():
    import dgl
    dgl.run()
    pass

```

我们推荐使用 `try` 捕获导入错误，从而引导用户访问正确的安装页面。


```python

def calculate():
    try:
        import dgl
    except ImportError:
        raise ImportError(
            'Please install the dgl from https://www.dgl.ai/pages/start.html'
        )
    dgl.run()
    pass

```

### 主模块

如果您想为 omicverse 提交 Pull Request，需要明确所开发功能归属于哪个模块。
例如，`TOSICA` 属于单细胞领域的算法，即需要在 `omicverse` 的 `single` 文件夹内添加 `_tosica.py` 文件，
并在 `_init__.py` 中添加 `from . _tosica import pyTOSICA`，使 omicverse 加入新功能。

````shell
.
├── omicverse
├───── single
├──────── __init__.py
├──────── _tosica.py
````

所有函数均需按以下格式提供参数说明：

```python

def preprocess(adata:anndata.AnnData, mode:str='scanpy', target_sum:int=50*1e4, n_HVGs:int=2000,
    organism:str='human', no_cc:bool=False)->anndata.AnnData:
    """
    Preprocesses the AnnData object adata using either a scanpy or a pearson residuals workflow for size normalization
    and highly variable genes (HVGs) selection, and calculates signature scores if necessary.

    Arguments:
        adata: The data matrix.
        mode: The mode for size normalization and HVGs selection. It can be either 'scanpy' or 'pearson'. If 'scanpy', performs size normalization using scanpy's normalize_total() function and selects HVGs
            using pegasus' highly_variable_features() function with batch correction. If 'pearson', selects HVGs
            using scanpy's experimental.pp.highly_variable_genes() function with pearson residuals method and performs
            size normalization using scanpy's experimental.pp.normalize_pearson_residuals() function.
        target_sum: The target total count after normalization.
        n_HVGs: the number of HVGs to select.
        organism: The organism of the data. It can be either 'human' or 'mouse'.
        no_cc: Whether to remove cc-correlated genes from HVGs.

    Returns:
        adata: The preprocessed data matrix.
    """

```

### 为 OmicVerse 智能体注册函数

希望被智能体发现的函数必须使用 `@register_function` 进行装饰。
该装饰器位于 `omicverse.utils.registry` 中，
记录别名、类别和可读描述等关键元数据。
这些元数据会在意图检测和代码生成期间提供给智能体，因此请勿遗漏任何必填字段。

```python
from omicverse.utils.registry import register_function


@register_function(
    aliases=["质控", "qc", "quality_control"],
    category="preprocessing",
    description="Perform standard single-cell quality control filtering",
    examples=["ov.pp.qc(adata, tresh={'mito_perc': 0.15, 'nUMIs': 500, 'detected_genes': 250})"],
)
def qc(adata, tresh=None):
    """Run OmicVerse QC on the provided AnnData."""
    ...
```

请确保至少提供一个别名、非空描述和类别；注册表验证会强制执行这些要求。
提供文档字符串和代表性示例可显著提升智能体建议和自动生成代码的质量。

## Pull Request

1. 首先需要 `fork` omicverse，然后从您的仓库 git clone 您的 fork。
2. 完成相关功能开发后，发起 Pull Request 并等待审核与合并。

