# OmicVerse 安装指南

中文版安装指南请参阅 [安装指南 (中文版)](Installation_guide_zh.md)。

## 前置条件

OmicVerse 可通过 conda 或 pip 安装，但必须先安装 **PyTorch**。

:::{note}
我们推荐在 `conda` 环境中安装 OmicVerse，以避免依赖冲突。
使用 `pip install -U omicverse` 可更新已有安装。

我们同样推荐使用 `uv pip` 代替普通 `pip`。
可通过运行 `pip install uv` 来安装 `uv`。
:::

### 平台特定要求

:::::{tab-set}

::::{tab-item} Windows (WSL)
安装 [WSL 子系统](https://learn.microsoft.com/en-us/windows/wsl/install)
并在 WSL 内配置 conda。
::::

::::{tab-item} Windows (原生)
从版本 `1.6.2` 开始，OmicVerse 支持原生 Windows。
您需要先安装 `torch` 和 `torch_geometric`。
::::

::::{tab-item} Linux
安装 [Anaconda](https://www.anaconda.com/) 或
[Miniconda](https://docs.conda.io/en/latest/miniconda.html)。
::::

::::{tab-item} macOS
使用 [`miniforge`](https://github.com/conda-forge/miniforge) 或
[`mambaforge`](https://www.rho-signal-effective-analytics.com/modules/pre-course/miniconda-installation/)。

**Apple Silicon Mac 重要提示：** OmicVerse 需要原生版本的 Python。
请使用 Homebrew 安装原生 Apple Silicon 版本的 mambaforge：

```shell
brew install --cask mambaforge
```
::::

:::::

## 安装方式

:::::{tab-set}

::::{tab-item} 快速安装（推荐）
:sync: quick

安装 OmicVerse 最简便的方式是使用我们的安装脚本：

```shell
# 仅限 Linux
curl -sSL omicverse.com/install | bash -s
```

此脚本将自动完成：

- 配置适合的环境
- 为您的系统安装正确版本的 PyTorch
- 安装所有必要依赖
- 根据您的硬件最优化配置 OmicVerse
::::

::::{tab-item} Conda / Mamba
:sync: conda

1. **创建并激活新环境**：

   ```shell
   conda create -n omicverse python=3.10
   conda activate omicverse
   ```

2. **安装 PyTorch 和 PyTorch Geometric (PyG)**：

   ```shell
   # 支持 CUDA（使用 'nvcc --version' 检查您的 CUDA 版本）
   conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

   # 或仅使用 CPU 安装
   conda install pytorch torchvision torchaudio cpuonly -c pytorch

   # 安装 PyTorch Geometric
   conda install pyg -c pyg
   ```

3. **安装 OmicVerse**：

   ```shell
   conda install omicverse -c conda-forge
   ```

4. **验证安装**：

   ```shell
   python -c "import omicverse"
   ```
::::

::::{tab-item} pip / PyPI
:sync: pip

1. **安装 uv（推荐的包管理器）**：

   ```shell
   pip install uv
   ```

2. **安装 PyTorch** *（在 macOS 上使用 pip 安装可能会遇到一些问题）*：

   ```shell
   uv pip install torch torchvision torchaudio
   ```

3. **安装 PyTorch Geometric**：

   ```shell
   uv pip install torch_geometric
   ```

4. **安装 OmicVerse**：

   ```shell
   uv pip install omicverse
   ```

5. **验证安装**：

   ```shell
   python -c "import omicverse"
   ```
::::

:::::

## 其他选项

:::::{tab-set}

::::{tab-item} 夜间版 / 开发版

安装含最新功能的开发版本：

```shell
# 方式 1：克隆仓库并本地安装
git clone https://github.com/Starlitnightly/omicverse.git
cd omicverse
pip install .

# 方式 2：直接从 GitHub 安装
pip install git+https://github.com/Starlitnightly/omicverse.git
```
::::

::::{tab-item} 开发者配置

面向贡献者：

```shell
pip install -e ".[dev,docs]"
```
::::

::::{tab-item} GPU 加速（RAPIDS）

使用 GPU 加速获得最佳性能：

```shell
# 1. 创建新的 conda 环境
conda create -n rapids python=3.11

# 2. 安装 RAPIDS
conda install rapids=24.04 -c rapidsai -c conda-forge -c nvidia -y

# 3. 安装其他 RAPIDS 组件
conda install cudf=24.04 cuml=24.04 cugraph=24.04 cuxfilter=24.04 \
    cucim=24.04 pylibraft=24.04 raft-dask=24.04 cuvs=24.04 \
    -c rapidsai -c conda-forge -c nvidia -y

# 4. 安装 rapids-singlecell
pip install rapids-singlecell

# 5. 安装 OmicVerse
curl -sSL https://raw.githubusercontent.com/Starlitnightly/omicverse/refs/heads/master/install.sh | bash -s
```

:::{note}
我们安装 RAPIDS 24.04 是因为部分系统的 glibc 版本 < 2.28。
如果您的系统支持，请参考 [RAPIDS 官方教程](https://docs.rapids.ai/install) 安装最新版本。
:::
::::

:::::

## Docker

预构建的 Docker 镜像可在
[Docker Hub](https://hub.docker.com/r/starlitnightly/omicverse) 获取。

```shell
docker pull starlitnightly/omicverse
```

## Jupyter Lab 配置

我们推荐使用 Jupyter Lab 进行交互式分析：

```shell
pip install jupyterlab
```

安装完成后，激活您的 omicverse 环境并在终端中运行 `jupyter lab`，
随后会出现一个可在浏览器中打开的 URL。

<img src="img/light_jupyter.jpg" class="only-light" alt="Jupyter Lab（亮色模式）" style="max-width:100%;" />
<img src="img/dark_jupyter.jpg" class="only-dark" alt="Jupyter Lab（暗色模式）" style="max-width:100%;" />

## 故障排查

:::::{tab-set}

::::{tab-item} Linux GCC

```shell
# Ubuntu
sudo apt update
sudo apt install build-essential

# CentOS
sudo yum group install "Development Tools"

# 验证 GCC
gcc --version
```
::::

::::{tab-item} 包安装问题

如果 pip 无法安装某些包（例如 `scikit-misc`），请尝试使用 conda：

```shell
conda install scikit-misc -c conda-forge -c bioconda
```
::::

::::{tab-item} Apple Silicon (M1/M2)

```shell
conda install s_gd2 -c conda-forge
pip install -U omicverse
conda install pytorch::pytorch torchvision torchaudio -c pytorch
```

**重要提示：** OmicVerse 在 Apple Silicon Mac 上需要原生版本的 Python。
请使用 Homebrew 安装原生 Apple Silicon 版本的 mambaforge：

```shell
brew install --cask mambaforge
```
::::

::::{tab-item} macOS `omp_set_nested` 已弃用

```shell
# 1. 卸载 pip 安装的包
pip uninstall -y numpy scipy scikit-learn threadpoolctl \
    torch torchvision torchaudio pytorch-lightning

# 2. 从 conda-forge 安装干净的 LP64 + OpenBLAS 栈
mamba install -c conda-forge \
    "numpy>=1.26,<2" "scipy>=1.11,<2" anndata "scanpy>=1.10" pandas \
    scikit-learn numexpr threadpoolctl \
    "libblas=*=*openblas" "libopenblas=*=*openmp" libomp

# 3. 使用 conda 安装 PyTorch
mamba install -c pytorch -c conda-forge pytorch torchvision torchaudio
```
::::

:::::
