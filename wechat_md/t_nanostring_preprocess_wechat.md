<!-- 由 docs_zh/Tutorials-space/t_nanostring_preprocess.ipynb 直接导出，用于公众号排版 -->

# 分析 NanoString 数据

CosMx Spatial Molecular Imager (SMI) 是 NanoString 于 2022 年推出的一种高通量原位空间分子成像平台，面向单细胞乃至亚细胞尺度分析。它把高分辨率成像与多重 RNA、蛋白检测结合起来，使我们能够在组织原位背景下直接观察并定量分子信号。这也是 CosMx 近年越来越多地被用于肿瘤微环境、发育生物学和组织病理研究的原因：它不仅告诉你细胞表达了什么，也告诉你细胞位于哪里，以及相邻细胞可能如何发生相互作用。

本 notebook 以公开的 CosMx NSCLC FFPE 数据集中的 `Lung5_Rep2` 为例，演示 OmicVerse 中一套完整的 NanoString 工作流。这里的主线很明确：先读入原始文件、确认 FOV 级空间结构、检查分割质量，再进入后续空间建模。

整个分析分为四个部分：

1. 配置环境并确认输入文件结构。
2. 读取 NanoString 数据集，检查空间坐标和表达模式。
3. 聚焦单个 FOV，查看底图叠加效果与分割边界。
4. 准备 CAST 输入，生成嵌入，并在空间坐标中比较聚类结果。

这个教程不仅带你跑通流程，也帮助你理解每一步为什么要这样安排，以及关键参数分别控制什么。

## 1. 环境设置

这一部分主要完成三件事：导入 `omicverse`、设置绘图字体，以及启用自动重载。

- `ov.style(font_path='Arial')`：保持绘图风格一致，避免导出图像时出现字体不匹配。
- `%autoreload 2`：在本地开发或调试包代码时很有用，重新运行单元后会自动加载修改过的源码。
- `Path`：后续用于更清晰地构建数据路径。

```python
from pathlib import Path
import omicverse as ov
ov.style(font_path='Arial')

# 启用自动重载，便于开发和调试
%load_ext autoreload
%autoreload 2
```

```text
🔬 Starting plot initialization...
Using already downloaded Arial font from: /tmp/omicverse_arial.ttf
Registered as: Arial
🧬 Detecting GPU devices…
🚫 No GPU devices found (CUDA/MPS/ROCm/XPU)

   ____            _     _    __
  / __ \____ ___  (_)___| |  / /__  _____________
 / / / / __ `__ \/ / ___/ | / / _ \/ ___/ ___/ _ \
/ /_/ / / / / / / / /__ | |/ /  __/ /  (__  )  __/
\____/_/ /_/ /_/_/\___/ |___/\___/_/  /____/\___/

🔖 Version: 2.1.1rc1   📚 Tutorials: https://omicverse.readthedocs.io/
✅ plot_set complete.
```

这一行会初始化 OmicVerse 使用的 CPU/GPU 混合运行环境。

对大多数用户来说，它的实际意义很直接：后续涉及深度学习或图嵌入的步骤可以更稳定地调用硬件资源。如果当前环境没有 GPU，建议把 CAST 配置为在 CPU 上运行。

```python
ov.settings.cpu_gpu_mixed_init()
```

## 2. 检查 NanoString 数据目录

在正式读入数据之前，先打印目录树，确认表达矩阵、metadata、FOV 坐标文件以及图像相关目录都位于预期位置。

本教程使用的是开放的 CosMx NSCLC FFPE 数据集中的 `Lung5_Rep2`。根据数据集说明，这套原型数据包含 8 个 FFPE 非小细胞肺癌样本，使用 960-plex RNA panel 进行检测，典型应用包括细胞分型、组织状态解析以及配体-受体分析。由于 CosMx 数据本身就是“计数矩阵 + metadata + 多个 FOV 图像 + 分割相关文件”的组合体，所以路径问题通常更适合在文件层面提前发现，而不是等到加载或绘图函数报错后再回头排查。

这里用到的计数数据和 HE 图像下载自 https://nanostring.com/products/cosmx-spatial-molecular-imager/ffpe-dataset/

```python
# !mkdir data
# !mkdir data/nanostring_data
# !wget -P data/nanostring_data https://nanostring-public-share.s3.us-west-2.amazonaws.com/SMI-Compressed/Lung5_Rep2/Lung5_Rep2+SMI+Flat+data.tar.gz
# !tar -xzf data/nanostring_data/Lung5_Rep2+SMI+Flat+data.tar.gz -C data/nanostring_data/
```

```python
ov.utils.print_tree(Path("data/nanostring_data/Lung5_Rep2/Lung5_Rep2-Flat_files_and_images"),)
```

```text
Lung5_Rep2-Flat_files_and_images/
│   CellComposite/
│   ├── CellComposite_F001.jpg
│   ├── ...
│   └── CellComposite_F030.jpg
│   CellLabels/
│   ├── CellLabels_F001.tif
│   ├── ...
│   ├── CellLabels_F030.tif
│   └── Thumbs.db
│   CellOverlay/
│   ├── CellOverlay_F001.jpg
│   ├── ...
│   └── CellOverlay_F030.jpg
│   CompartmentLabels/
│   ├── CompartmentLabels_F001.tif
│   ├── ...
│   └── CompartmentLabels_F030.tif
├── Lung5_Rep2_exprMat_file.csv
├── Lung5_Rep2_fov_positions_file.csv
├── Lung5_Rep2_metadata_file.csv
└── Lung5_Rep2_tx_file.csv
```

## 3. 读取 NanoString 数据集

这个单元通过 `ov.io.read_nanostring()` 构建一个 `AnnData` 对象。除了表达矩阵本身，加载器还会把细胞 metadata、FOV 注释、可选的形态学图像、细胞轮廓和空间坐标统一组织到同一个分析对象里。

这一步对 CosMx 类型数据尤其关键：当这些信息都被规整进 `adata` 之后，你就可以比较自然地在整样本拼接视图、单 FOV 图像叠加、分割感知可视化以及后续图学习之间切换，而不用手工对齐多种文件格式。

### 主要参数

- `path`：样本文件所在目录。
- `counts_file`：表达矩阵文件，通常按 cells × genes 组织。
- `meta_file`：包含细胞级注释信息的 metadata 文件。
- `fov_file`：描述不同视野空间位置的文件。

实际使用时，`read_nanostring()` 就是把原始 NanoString 输出转换成可直接用于绘图和下游分析的数据入口。

```python
from pathlib import Path
nanostring_dir = Path().resolve() / "data" / "nanostring_data"
sample_dir = nanostring_dir / "Lung5_Rep2" / "Lung5_Rep2-Flat_files_and_images"

adata = ov.io.read_nanostring(
    path=sample_dir,
    counts_file="Lung5_Rep2_exprMat_file.csv",
    meta_file="Lung5_Rep2_metadata_file.csv",
    fov_file="Lung5_Rep2_fov_positions_file.csv",
)
```

```text
[Nanostring] Reading Nanostring data from: /scratch/users/steorra/analysis/26_omic_protocol/data/nanostring_data/Lung5_Rep2/Lung5_Rep2-Flat_files_and_images
[Nanostring] Matched cells: 106660
[Nanostring] Loading optional FOV images
```

```text
[Nanostring] Extracted cell contours from CellLabels images (geometry WKT generated for 106660 cells)
[Nanostring] Loading FOV metadata: Lung5_Rep2_fov_positions_file.csv
[Nanostring] Done (n_obs=106660, n_vars=980)
```

```python
adata.write('data/Lung5_Rep2_nanostring.h5ad')
```

## 4. 在整张样本尺度检查空间布局

这里使用 `ov.pl.embedding()` 对所有 FOV 做第一次整体预览。

### 主要参数

- `basis='spatial_fov'`：使用跨 FOV 拼接后的空间坐标系。当你想查看多个 FOV 之间的相对位置关系时，这是最合适的视图。
- `color=['Max.PanCK', 'fov']`：一个面板按 marker 强度着色，另一个面板按 FOV 编号着色。
- `vmax='p99.2'`：把颜色上限截断在 99.2 百分位，减少极端值对色阶的影响。
- `cmap='Reds'`：使用连续红色渐变显示表达强度。
- `wspace=0.35`：调整面板间距。

此时的重点不是看局部细节，而是先确认坐标、FOV 拼接和整体信号范围是否合理，再进入局部检查。

```python
ov.pl.embedding(
    adata,
    basis='spatial_fov',
    color=['Max.PanCK','fov'],
    vmax='p99.2',
    cmap='Reds',
    wspace=0.35
)
```

![4. 在整张样本尺度检查空间布局](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_12.png)

打印 `adata` 是一个很轻量的 sanity check，用来确认数据是否正确读入。这里最值得检查的是：

- 观测值和变量的数量，也就是细胞数和特征数；
- `obs` 中有哪些 metadata 列可用；
- `obsm`、`layers` 和 `uns` 里是否已经包含后续分析需要的空间对象。

```python
adata
```

```text
AnnData object with n_obs × n_vars = 106660 × 980
    obs: 'fov', 'Area', 'AspectRatio', 'CenterX_global_px', 'CenterY_global_px', 'Width', 'Height', 'Mean.MembraneStain', 'Max.MembraneStain', 'Mean.PanCK', 'Max.PanCK', 'Mean.CD45', 'Max.CD45', 'Mean.CD3', 'Max.CD3', 'Mean.DAPI', 'Max.DAPI', 'cell_ID', 'geometry'
    uns: 'spatial', 'omicverse_io', 'fov_colors_rgba', 'fov_colors'
    obsm: 'spatial', 'spatial_fov'
```

## 5. 选择单个 FOV 做局部检查

从这里开始，notebook 聚焦于 `fov == '12'`。原因很实际：CosMx 并不是把一大片组织一次性拍成一张巨图，而是把样本拆成多个 FOV 来采集，每个 FOV 都有自己的局部图像区域和坐标系，之后再拼接成更大的空间布局。

也正因为如此，这里必须采用“两级视图”。整样本拼接视图适合做方向判断和跨 FOV 一致性检查，而单个 FOV 更适合观察局部图像配准、分割边界和 marker 分布。

如果你想查看其他视野，只需要把 `'12'` 替换成目标 FOV 编号即可。

```python
vdata=adata[adata.obs['fov']=='12']
```

先在单个 FOV 内查看 `Max.PanCK` 的空间分布。

这里最重要的是区分 `basis='spatial'` 和前面使用的 `spatial_fov`：

- `spatial_fov`：更适合多个 FOV 拼接后的整样本视图。
- `spatial`：更适合单个 FOV 自身的原始局部坐标系。

如果某个 FOV 的方向、长宽比或点位分布看起来不正常，通常这里就是最先需要排查的位置。

```python
ov.pl.embedding(
    vdata,
    basis='spatial',
    color='Max.PanCK',
    vmax='p99.2',
    cmap='Reds'
)
```

![先在单个 FOV 内查看 `Max.PanCK` 的空间分布。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_18.png)

## 6. 结合背景图可视化单个 FOV

`ov.pl.spatial()` 会把信号叠加到空间背景图上。相较于普通散点图，这种方式更接近组织切片的直观观感。

### 主要参数

- `color=[None, 'Max.PanCK']`：第一个面板只显示背景图，第二个面板叠加目标 marker，方便并排比较。
- `size=100`：控制绘制点的大小。
- `library_id='12'`：显式选择当前 FOV 对应的图像。
- `img_key='hires'`：使用该 FOV 存储的高分辨率图像。
- `alpha_img=1`：设置背景图透明度，值为 1 表示完全显示。
- `crop_coord=None`：不裁剪，直接显示整个 FOV。

在整理图件时，这一步很适合用来判断表达模式是否和图像背景一致，再决定是否叠加分割轮廓。

```python
ov.pl.spatial(
    vdata, color=[None,"Max.PanCK"],
    size=100,
    library_id='12',
    legend_fontsize=13, 
    frameon=None,
    vmax=50000,
    cmap='Reds'
)
```

![6. 结合背景图可视化单个 FOV](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_20.png)

对于 NanoString 数据，OmicVerse 也支持把任意视野（FOV）拼接后一起可视化。

```python
ov.pl.nanostring(
    adata, color=["Max.PanCK"],
    size=1,
    fovs=['19','20'],
    legend_fontsize=13, 
    alpha=0.25,
    vmax=50000,
    cmap='Reds'
)
```

```text
<Axes: title={'center': 'Max.PanCK'}, xlabel='global x (px)', ylabel='global y (px)'>
```

![对于 NanoString 数据，OmicVerse 也支持把任意视野（FOV）拼接后一起可视化。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_22.png)

如果设置 `fovs=None`，就会一次显示所有 FOV。

```python
ov.pl.nanostring(
    adata, color=[None,"Max.PanCK"],
    size=1,
    fovs=None,
    legend_fontsize=13, 
    vmax=50000,
    cmap='Reds'
)
```

```text
[<Axes: xlabel='global x (px)', ylabel='global y (px)'>,
 <Axes: title={'center': 'Max.PanCK'}, xlabel='global x (px)', ylabel='global y (px)'>]
```

![如果设置 `fovs=None`，就会一次显示所有 FOV。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_24.png)

## 7. 同时查看分割轮廓与表达信号

接下来切换到 `ov.pl.spatialseg()`。对于带有分割信息的数据，这个函数比普通点图更合适，因为它会把细胞边界直接叠加到背景图上，而不只是画点。

在 CosMx 工作流里，这一步不只是为了让图更好看。官方数据集材料反复强调，稳健的细胞分割是细胞图谱构建、空间邻域分析和配体-受体解释的前提，因为这些分析都依赖于把转录本尽可能准确地分配到对应细胞边界内。

### 主要参数

- `color='Max.PanCK'`：按目标特征给细胞着色。
- `edges_color='white'`, `edges_width=0`：控制分割边界的颜色和线宽。
- `seg_contourpx=15`：设置分割轮廓的像素厚度。
- `library_id='12'`：选择要显示的 FOV。
- `img_key='hires'`：使用高分辨率背景图。
- `crop_coord=None`：显示完整视野，而不是局部裁剪。

因此这一步本质上是一个真正的质控检查点：在相信后续生物学解释之前，你需要先判断当前分割叠加是否足够清晰、边界粗细是否与图幅匹配。

```python
ov.pl.spatialseg(
    vdata,
    color="Max.PanCK",
    edges_color='white',
    edges_width=0,
    #edges_width=0.4,
    figsize=(7, 4),
    library_id='12',
    alpha_img=1,
    seg_contourpx=1,
    alpha=1,
    #crop_coord=(0, 0, 1400, 1400),
    legend_fontsize=13,
)
```

```text
<Axes: title={'center': 'Max.PanCK'}, xlabel='spatial 1', ylabel='spatial 2'>
```

![7. 同时查看分割轮廓与表达信号](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_26.png)

在分割轮廓叠加场景下，OmicVerse 同样支持拼接多个 FOV 一起展示。

```python
ov.pl.nanostringseg(
    adata, color=["Max.PanCK"],
    fovs=['12','13'],
    legend_fontsize=13, 
    alpha=0.8,
    alpha_img=1,
    vmax=50000,
    cmap='Reds',
    edges_color='white',
    edges_width=0.1,
    seg_contourpx=0.3,
    bw=True,
    rasterized=True,
    figsize=(7, 4),
)
```

```text
<Axes: title={'center': 'Max.PanCK'}, xlabel='global x (px)', ylabel='global y (px)'>
```

![在分割轮廓叠加场景下，OmicVerse 同样支持拼接多个 FOV 一起展示。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_28.png)

下一张图和上一张类似，只是没有显式设置 `seg_contourpx`。把这两个版本放在一起看，更容易判断轮廓粗细对可读性的影响。

一个实用经验是：

- 如果你想强调分割结构，可以适当增大 `seg_contourpx`；
- 如果你更想突出连续表达模式，就应把边界画得更细，或者整体弱化边界存在感。

```python
ov.pl.spatialseg(
    vdata,
    color="Max.PanCK",
    edges_color='white',
    edges_width=0,
    #edges_width=0.4,
    figsize=(7, 4),
    library_id='12',
    alpha_img=1,
    #seg_contourpx=1,
    alpha=1,
    #crop_coord=(0, 0, 1400, 1400),
    legend_fontsize=13,
)
```

```text
<Axes: title={'center': 'Max.PanCK'}, xlabel='spatial 1', ylabel='spatial 2'>
```

![下一张图和上一张类似，只是没有显式设置 `seg_contourpx`。把这两个版本放在一起看，更容易判断轮廓粗细对可读性的影响。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_30.png)

## 8. 在局部裁剪前检查坐标范围

在制作放大视图之前，先查看当前 FOV 的 x、y 坐标范围。这样就可以基于真实数值设置 `crop_coord`，而不是反复试错。

这一步很小，但在准备论文图或锁定某个局部区域时非常有帮助。

```python
vdata.obsm['spatial'][:,0].min(),vdata.obsm['spatial'][:,0].max()
```

```text
(array(13), array(5456))
```

这个单元单独打印 y 坐标范围，配合前一个输出，就可以更有针对性地确定局部裁剪窗口。

```python
vdata.obsm['spatial'][:,1].min(),vdata.obsm['spatial'][:,1].max()
```

```text
(array(9), array(3634))
```

## 9. 放大查看选定区域

这个单元使用 `crop_coord=(0, 2000, 400, 2400)` 显示一个局部区域。你可以把它理解为在当前 FOV 中定义一个矩形窗口，以更高分辨率查看细胞边界和表达模式。

### `crop_coord` 的作用

不同绘图函数在内部实现上可能对坐标顺序略有差异，但核心逻辑一致：传入一个矩形范围，只显示该范围内的内容。

对于基于图像的绘图，裁剪尤其适用于以下场景：

- 感兴趣区域只占整张 FOV 的一小部分；
- 需要局部评估分割质量；
- 图版排版需要比整张图更紧凑的构图。

```python
ov.pl.spatialseg(
    vdata,
    color="Max.PanCK",
    edges_color='white',
    edges_width=0,
    #edges_width=0.4,
    figsize=(7, 4),
    library_id='12',
    alpha_img=1,
    seg_contourpx=0.5,
    alpha=1,
    crop_coord=(0, 2000, 400, 2400),
    legend_fontsize=13,
)
```

```text
<Axes: title={'center': 'Max.PanCK'}, xlabel='spatial 1', ylabel='spatial 2'>
```

![9. 放大查看选定区域](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_36.png)

在进入建模部分之前，再打印一次 `adata` 作为轻量级 sanity check，确认前面的可视化步骤没有对对象状态引入意料之外的变化。

```python
adata
```

```text
AnnData object with n_obs × n_vars = 106660 × 980
    obs: 'fov', 'Area', 'AspectRatio', 'CenterX_global_px', 'CenterY_global_px', 'Width', 'Height', 'Mean.MembraneStain', 'Max.MembraneStain', 'Mean.PanCK', 'Max.PanCK', 'Mean.CD45', 'Max.CD45', 'Mean.CD3', 'Max.CD3', 'Mean.DAPI', 'Max.DAPI', 'cell_ID', 'geometry'
    uns: 'spatial', 'omicverse_io'
    obsm: 'spatial', 'spatial_fov'
```

## 10. 为 CAST 准备空间坐标

CAST 需要显式的坐标输入，因此这里把整样本坐标系 `spatial_fov` 中的坐标写入 `adata.obs['x']` 和 `adata.obs['y']`。

原始注释里已经提示，这个赋值有时需要重新执行，并检查是否出现 `NA`。实际排查时通常对应两类问题：

- 前面的对象状态没有完全刷新；
- 索引对齐方式和预期不一致。

这个单元的目的，是让后续构建 CAST 所需的按 FOV 分组字典时，能更方便地读取坐标。

```python
# 这一单元有时需要运行两次
# 并确认 adata.obs['x'] 没有被写成 NA
adata.obs['x'] = adata.obsm['spatial_fov'][:,0]
adata.obs['y'] = adata.obsm['spatial_fov'][:,1]
adata.obs['x'][0]
```

```text
8156.0
```

## 11. 构建归一化表达层

这里通过 `ov.pp.normalize_total()` 把每个细胞的总计数归一化到 `1e4`，并把结果保存到 `adata.layers['norm_1e4']`。

### 主要参数

- `target_sum=1e4`：归一化后每个细胞的目标总计数。
- `inplace=False`：返回归一化矩阵，而不是直接覆盖原始数据。

单独保留一个归一化层很有价值，因为这样既能保存原始矩阵，又能为后续嵌入方法提供标准化输入。

```python
adata.layers['norm_1e4'] = ov.pp.normalize_total(
    adata,
    target_sum=1e4,
    inplace=False,
)['X'].toarray()  # 使用每个细胞的归一化计数作为输入表达矩阵
```

```text
🔍 Count Normalization:
   Target sum: 10000.0
   Exclude highly expressed: False
   ⚠️ Warning: 5,508 cells have zero counts

✅ Count Normalization Completed Successfully!
   ✓ Processed: 106,660 cells × 980 genes
   ✓ Runtime: 0.21s
```

## 12. 按 FOV 组织 CAST 输入

CAST 需要两个字典：

- `coords_raw`：每个 FOV 的二维坐标；
- `exp_dict`：每个 FOV 的归一化表达矩阵。

核心思路是把一个大的 `AnnData` 对象拆成多个 FOV 级别子集，再传给 CAST 做跨样本图表示学习。这里使用 `samples = np.unique(adata.obs['fov'])`，以稳定一致的顺序遍历所有 FOV。

```python
import numpy as np

# 获取每个样本的坐标和表达数据
samples = np.unique(adata.obs['fov'])  # adata 中使用到的样本
coords_raw = {
    sample_t: np.array(adata.obs[['x', 'y']])[adata.obs['fov'] == sample_t] for sample_t in samples
}
exp_dict = {
    sample_t: adata[adata.obs['fov'] == sample_t].layers['norm_1e4'] for sample_t in samples
}
```

## 13. 运行 CAST_MARK 生成图嵌入

这是整个 notebook 的核心建模步骤：基于每个 FOV 的空间坐标和表达矩阵学习图嵌入。

### 主要参数

- `coords_raw`：各 FOV 的空间坐标字典。
- `exp_dict`：各 FOV 的表达矩阵字典。
- `output_path`：中间结果或输出文件的保存目录。
- `graph_strategy='delaunay'`：使用 Delaunay 三角剖分构建空间图。
- `device='cuda:0'`：在第一张 GPU 上运行；如果需要 CPU 或其他设备，应在这里修改。
- `args = Args(...)`：封装 CAST 使用的一组训练超参数。

更具体的优化细节属于 CAST 模型本身；从这个 notebook 的角度看，这一步就是把原始空间表达转换为可用于后续分析的学习型嵌入空间。

```python
### 运行模型生成图嵌入
# 设置输出目录
import os
output_path = 'result/CAST_Mark/output'
os.makedirs(output_path, exist_ok=True)

from omicverse.external.CAST import CAST_MARK
embed_dict = CAST_MARK(
    coords_raw, exp_dict, output_path,
    gpu_t=0, device='cuda:0'
)
```

## 14. 用 K-means 初步查看嵌入结构

CAST 得到嵌入后，使用 `kmeans_plot_multiple()` 做一次快速的无监督总结。这里的目标不是立即给出生物学解释，而是先判断嵌入空间是否已经能分开有意义的空间区域。

### 主要参数

- `embed_dict`：CAST 输出的嵌入结果。
- `samples`：参与分析的 FOV 列表。
- `task_name_t='Lung5_Rep2'`：可视化中使用的任务标签。
- `output_path_t`：输出保存目录。
- `k=20`：K-means 聚类数。
- `plot_strategy='sep'`：各样本分别绘图，而不是全部合并到一个面板。

可以把它视为一个探索性检查点：如果嵌入质量足够好，即便是简单的聚类方法，也应该开始显露结构。

```python
### 使用 K-means 可视化嵌入结果
from omicverse.external.CAST.visualize import kmeans_plot_multiple

clusters_kmeans = kmeans_plot_multiple(
    embed_dict, samples, coords_raw, 'demo1', output_path,
    k=30, dot_size=10, minibatch=False
)
```

## 15. 把 CAST 的 K-means 标签写回 `adata.obs`

这个循环会按照 FOV 顺序，把 `clusters_kmeans` 映射回原始细胞表，并最终写入 `adata.obs['cast_clusters']`。

之所以手动维护 `front_idx` 和 `back_idx`，是因为 `clusters_kmeans` 本质上是按 FOV 顺序拼接后的结果。要正确还原标签，就必须把每一段重新对齐到对应的细胞子集。

```python
adata.obs['cast_clusters']='-1'
for idx,key in enumerate(embed_dict.keys()):
    if idx==0:
        front_idx=0
        back_idx=adata.obs.loc[adata.obs['fov']==key].shape[0]
        adata.obs.loc[adata.obs['fov']==key,'cast_clusters']=clusters_kmeans[front_idx:front_idx+back_idx]
        front_idx+=back_idx
    else:
        back_idx=adata.obs.loc[adata.obs['fov']==key].shape[0]
        adata.obs.loc[adata.obs['fov']==key,'cast_clusters']=clusters_kmeans[front_idx:front_idx+back_idx]
        front_idx+=back_idx
```

## 16. 把 CAST 嵌入保存到 `adata.obsm`

除了聚类标签外，512 维的 CAST 嵌入本身也应该保存下来，供后续构图和 Leiden 聚类使用。

代码先创建一个空矩阵，再按 FOV 逐块填充。保存到 `obsm['X_cast']` 之后，这个表示就可以像 `X_pca`、`X_umap` 一样被下游流程直接调用。

```python
import pandas as pd
adata.obsm['X_cast']=np.zeros((adata.shape[0],512))
adata.obsm['X_cast']=pd.DataFrame(adata.obsm['X_cast'],index=adata.obs.index)
from tqdm import tqdm
for key in tqdm(embed_dict.keys()):
    adata.obsm['X_cast'].loc[adata.obs['fov']==key]+=embed_dict[key].cpu().numpy()
```

把 `cast_clusters` 转成字符串，这样绘图函数会把它当作离散类别，而不是连续数值变量。这个小步骤通常是分类着色正常工作的前提。

```python
adata.obs['cast_clusters']=adata.obs['cast_clusters'].astype(str)
```

## 17. 在整样本空间中可视化 CAST 聚类

这里再次使用 `basis='spatial_fov'`，把 CAST 聚类标签投影回整张样本拼接后的空间布局。这样可以直观看出聚类是否具有空间连续性，以及它们在不同 FOV 之间是否呈现出可解释的组织结构。

`palette=ov.pl.palette_112[:]` 提供了足够多的离散颜色，适合类别较多的场景。

```python
ov.pl.embedding(
    adata,
    basis='spatial_fov',
    color=['cast_clusters'],
    vmax='p99.2',
    cmap='Reds',
    palette=ov.pl.palette_112[:],
    legend_fontsize=13,
)
```

![17. 在整样本空间中可视化 CAST 聚类](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_56.png)

前面为了方便按索引赋值，`X_cast` 曾临时存成 `DataFrame`。在计算邻接图之前，这里把它转回 `numpy` 数组，确保后续函数可以直接使用。

```python
adata.obsm['X_cast']=adata.obsm['X_cast'].values
```

## 18. 基于 CAST 嵌入构建邻接图

从这一步开始，不再使用 PCA，而是直接把 `X_cast` 作为近邻图构建的表示空间。

### 主要参数

- `n_neighbors=15`：每个细胞连接 15 个最近邻。
- `n_pcs=512`：这里与嵌入维度一致，因为 `X_cast` 本身就是 512 维。
- `use_rep='X_cast'`：显式指定使用 CAST 嵌入，而不是默认表示。

这一步会把学习到的嵌入转换为图结构，从而支持社区发现和其他下游分析。

```python
ov.pp.neighbors(
    adata,n_neighbors=15,
    n_pcs=512, use_rep='X_cast',
)
```

## 19. 运行 Leiden 聚类

接着在 CAST 嵌入构建出的邻接图上执行 Leiden 聚类。

- `resolution=0.1`：控制聚类粒度。值越大通常簇越多，值越小则结果更粗。

和前面的 K-means 相比，Leiden 更直接依赖近邻图结构，因此两者结果不需要完全一致。

```python
ov.pp.leiden(adata,resolution=0.1)
```

```text
⚙️ Using torch CPU/GPU mixed mode to calculate Leiden...
NVIDIA CUDA GPUs detected:
📊 [CUDA 0] NVIDIA A100-SXM4-40GB
    |----------------------------- 2443/40960 MiB (6.0%)
Using batch size `n_batches` calculated from sqrt(n_obs): 326
Running GPU Leiden (batched)
Device: cpu
```

```text
done: 25 clusters (0:00:24)

╭─ SUMMARY: leiden ──────────────────────────────────────────────────╮
│  Duration: 24.0545s                                                │
│  Shape:    106,660 x 980 (Unchanged)                               │
│                                                                    │
│  CHANGES DETECTED                                                  │
│  ────────────────                                                  │
╰────────────────────────────────────────────────────────────────────╯
```

这里把 Leiden 标签重新投影到 `spatial_fov` 坐标中，方便与前面 CAST K-means 的结果直接比较。

```python
ov.pl.embedding(
    adata,
    basis='spatial_fov',
    color=['leiden'],
    vmax='p99.2',
    cmap='Reds',
    palette=ov.pl.palette_112,
    legend_fontsize=13,
)
```

![这里把 Leiden 标签重新投影到 `spatial_fov` 坐标中，方便与前面 CAST K-means 的结果直接比较。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_64.png)

## 20. 在单个 FOV 内比较聚类结果

最后回到 `fov == '12'`，把 `leiden` 和 `cast_clusters` 都叠加到分割图像上。

这是回答两个常见问题的直接方法：

1. 聚类边界是否贴合组织结构？
2. K-means 和 Leiden 在局部分区上是否大体一致？

如果两种结果在某些区域差异很大，通常值得回头检查嵌入质量、邻接图构建参数，或者分割上下文本身。

```python
vdata=adata[adata.obs['fov']=='12']
```

这个面板展示的是 Leiden 聚类在分割叠加图上的空间分布。由于边界线画得较细，更容易观察相邻细胞群之间的过渡关系。

```python
ov.pl.spatialseg(
    vdata,
    color="leiden",
    edges_color='white',
    edges_width=0.1,
    #edges_width=0.4,
    figsize=(7, 4),
    library_id='12',
    alpha_img=1,
    #seg_contourpx=1,
    alpha=1,
    #crop_coord=(0, 0, 1400, 1400),
    legend_fontsize=13,
)
```

```text
<Axes: title={'center': 'leiden'}, xlabel='spatial 1', ylabel='spatial 2'>
```

![这个面板展示的是 Leiden 聚类在分割叠加图上的空间分布。由于边界线画得较细，更容易观察相邻细胞群之间的过渡关系。](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_68.png)

这个面板展示的是 CAST K-means 聚类结果。和 Leiden 图并排观察时，可以更清楚地判断：

- CAST 嵌入是否抓住了主要空间结构；
- 图聚类与直接聚类之间的局部差异主要出现在什么位置。

```python
ov.pl.spatialseg(
    vdata,
    color="cast_clusters",
    edges_color='white',
    edges_width=0.1,
    #edges_width=0.4,
    figsize=(7, 4),
    library_id='12',
    alpha_img=1,
    #seg_contourpx=1,
    alpha=1,
    #crop_coord=(0, 0, 1400, 1400),
    legend_fontsize=13,
)
```

```text
<Axes: title={'center': 'cast_clusters'}, xlabel='spatial 1', ylabel='spatial 2'>
```

![这个面板展示的是 CAST K-means 聚类结果。和 Leiden 图并排观察时，可以更清楚地判断：](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/20260407_nanostring_cell_70.png)

## 总结

到这里，完整流程已经走通：

- 将 NanoString 原始文件读入 `AnnData` 对象；
- 在整样本和单 FOV 两个尺度上检查空间表达与分割结果；
- 准备 CAST 输入并学习图嵌入；
- 在嵌入空间中执行 K-means 与 Leiden 聚类，再把结果映射回空间坐标。

放在更广的 CosMx 应用场景里，这些步骤也是细胞图谱构建、空间 niche 分析、配体-受体程序解析以及 FFPE 组织生物标志物解释的基础。

后续可以继续做的方向包括：

- 用 marker genes 为 CAST 聚类结果做注释；
- 比较不同 FOV 或不同生物学重复之间的聚类一致性；
- 结合 CAST 嵌入开展更正式的下游分析，例如 neighborhood enrichment、差异表达或区域级注释。
