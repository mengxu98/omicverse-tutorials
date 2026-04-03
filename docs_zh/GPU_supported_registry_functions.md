# 已注册函数 — GPU 支持概览

## 图例说明
- [x] 支持：GPU 加速可用（原生、参数启用或由环境自动启用）。
- [ ] 不支持：仅 CPU 实现。
- 如需启用 GPU，请先初始化环境（如有需要）：`ov.settings.gpu_init()`（RAPIDS）或 `ov.settings.cpu_gpu_mixed_init()`（混合模式）。实际 GPU 使用情况还取决于相关依赖是否以 GPU 支持方式安装。

## 设置
- [x] `ov.settings.gpu_init`：初始化 RAPIDS/GPU 模式。
- [x] `ov.settings.cpu_gpu_mixed_init`：初始化 CPU–GPU 混合模式。

## 预处理 (ov.pp)
- [x] `ov.pp.anndata_to_GPU`：将 AnnData 移至 GPU（RAPIDS）。
- [ ] `ov.pp.anndata_to_CPU`：将数据移回 CPU。
- [x] `ov.pp.preprocess`：端到端预处理（gpu <span class="tag tag-rapids">rapids</span>）。
    - `mode='shiftlog|pearson'`
        - [x] normalize_total/log1p（gpu <span class="tag tag-rapids">rapids</span>）。
        - [x] HVGs = pearson_residuals（gpu <span class="tag tag-rapids">rapids</span>）。
    - `mode='pearson|pearson'`
        - [x] normalize_pearson_residuals（gpu <span class="tag tag-rapids">rapids</span>）。
        - [x] HVGs = pearson_residuals（gpu <span class="tag tag-rapids">rapids</span>）。
- [x] `ov.pp.scale`：数据缩放（gpu <span class="tag tag-rapids">rapids</span>）。
- [x] `ov.pp.pca`：PCA（gpu <span class="tag tag-rapids">rapids</span> | <span class="tag tag-mixed">cpu-gpu-mixed</span>[<span class="tag tag-torch">torch</span>|<span class="tag tag-mlx">mlx</span>]）。
- [ ] `ov.pp.neighbors`：KNN 图（按 `method` 参数区分）。
    - [ ] `method='umap'`（基于 UMAP 的邻域估计，CPU）。
    - [ ] `method='gauss'`（高斯核，CPU）。
    - [x] `method='rapids'`（gpu <span class="tag tag-rapids">rapids</span>）。
- [ ] `ov.pp.umap`：UMAP（按实现区分）。
    - [ ] Scanpy UMAP（`settings.mode='cpu'`）。
    - [x] RAPIDS UMAP（`settings.mode='gpu'`，gpu <span class="tag tag-rapids">rapids</span>）。
    - [x] PyMDE/torch 路径（`settings.mode='cpu-gpu-mixed'`，<span class="tag tag-mixed">cpu-gpu-mixed</span>[<span class="tag tag-torch">torch</span>]）。
- [x] `ov.pp.qc`：质量控制（gpu <span class="tag tag-rapids">rapids</span> | <span class="tag tag-mixed">cpu-gpu-mixed</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.pp.score_genes_cell_cycle`：细胞周期评分。
- [x] `ov.pp.sude`：SUDE 降维（<span class="tag tag-mixed">cpu-gpu-mixed</span>[<span class="tag tag-torch">torch</span>]）。

## 工具函数 (ov.utils)
- [x] `ov.utils.mde`：最小失真嵌入（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.utils.cluster`：多算法聚类（按算法区分如下）。
    - [x] Leiden（<span class="tag tag-mixed">cpu</span>[<span class="tag tag-torch">igraph</span>]<span class="tag tag-mixed">cpu-gpu-mixed</span>[<span class="tag tag-torch">pyg</span>]）。
    - [ ] Louvain（Scanpy，CPU）。
    - [ ] KMeans（scikit-learn，CPU）。
    - [ ] GMM/mclust（scikit-learn，CPU）。
    - [ ] mclust_R（R 包 mclust，CPU）。
    - [ ] schist（schist 库，CPU）。
    - [ ] scICE（当前以 `use_gpu=False` 调用）。
- [ ] `ov.utils.refine_label`：邻域投票标签细化。
- [ ] `ov.utils.weighted_knn_trainer`：训练加权 KNN。
- [ ] `ov.utils.weighted_knn_transfer`：加权 KNN 标签转移。

## 单细胞 (ov.single)
- [ ] `ov.single.batch_correction`：批次校正（按方法区分如下）。
    - [ ] harmony（Harmony，CPU）。
    - [ ] combat（Scanpy Combat，CPU）。
    - [ ] scanorama（Scanorama，CPU）。
    - [x] scVI（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
    - [ ] CellANOVA（CPU）。
- [x] `ov.single.MetaCell`：SEACells（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.single.TrajInfer`：轨迹推断（按方法区分如下）。
    - [ ] palantir（CPU）。
    - [ ] diffusion_map（CPU）。
    - [ ] slingshot（CPU）。
- [x] `ov.single.Fate`：TimeFateKernel（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [x] `ov.single.pyCEFCON`：CEFCON 驱动因子发现（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [x] `ov.single.gptcelltype_local`：本地 LLM 注释（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [x] `ov.single.cNMF`：cNMF（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.single.CellVote`：多方法投票。
  * [ ] `scsa_anno`（SCSA，CPU）。
  * [ ] `gpt_anno`（在线 GPT，CPU/网络）。
  * [ ] `gbi_anno`（GPTBioInsightor，CPU/网络）。
  * [ ] `popv_anno`（PopV，CPU）。
- [ ] `ov.single.gptcelltype`：在线 GPT 注释。
- [ ] `ov.single.mouse_hsc_nestorowa16`：加载数据集。
- [ ] `ov.single.load_human_prior_interaction_network`：加载先验网络。
- [ ] `ov.single.convert_human_to_mouse_network`：跨物种基因符号转换。

## 空间转录组 (ov.space)
- [x] `ov.space.pySTAGATE`：STAGATE 空间聚类（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.space.clusters`：多方法空间聚类（按方法区分如下）。
    - [x] STAGATE（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
    - [x] GraphST（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
    - [x] CAST（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
    - [x] BINARY（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.space.merge_cluster`：合并聚类。
- [ ] `ov.space.Cal_Spatial_Net`：构建空间邻域图。
- [x] `ov.space.pySTAligner`：STAligner 整合（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [x] `ov.space.pySpaceFlow`：SpaceFlow 空间嵌入（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.space.Tangram`：Tangram 去卷积（按模式区分如下）。
    - [x] `mode='clusters'`（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
    - [x] `mode='cells'`（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.space.svg`：空间可变基因（基于统计，无明确 GPU）。
- [x] `ov.space.CAST`：CAST 整合（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
- [ ] `ov.space.crop_space_visium`：裁剪空间图像/坐标。
- [ ] `ov.space.rotate_space_visium`：旋转空间图像/坐标。
- [ ] `ov.space.map_spatial_auto`：自动映射（按方法区分如下）。
    - [x] `method='torch'`（<span class="tag tag-all">all</span>[<span class="tag tag-torch">torch</span>]）。
    - [ ] `method='phase'`（NumPy，CPU）。
    - [ ] `method='feature'`（基于特征的匹配，CPU）。
    - [ ] `method='hybrid'`（混合流程，CPU）。
- [ ] `ov.space.map_spatial_manual`：手动偏移映射。
- [ ] `ov.space.read_visium_10x`：读取 Visium 数据。
- [x] `ov.space.visium_10x_hd_cellpose_he`：H&E 分割（`gpu=True`）。
- [ ] `ov.space.visium_10x_hd_cellpose_expand`：标签扩展。
- [x] `ov.space.visium_10x_hd_cellpose_gex`：GEX 分割/映射（`gpu=True`）。
- [ ] `ov.space.salvage_secondary_labels`：合并标签。
- [ ] `ov.space.bin2cell`：Bin 转细胞。

## 外部模块 (ov.external)
- [x] `ov.external.GraphST.GraphST`：GraphST（`device` 支持 GPU）。
- [ ] `ov.bulk.pyWGCNA`：WGCNA（CPU 实现）。

## 绘图 (ov.pl)
- [ ] `ov.pl.*`（`_single/_bulk/_density/_dotplot/_violin/_general/_palette`）：绘图 API。

## Bulk (ov.bulk)
- [ ] `ov.bulk.*`（`_Deseq2/_Enrichment/_combat/_network/_tcga`）：统计、富集和网络分析。
