# 用户 API

导入 OmicVerse：

```python
import omicverse as ov
```

```{eval-rst}
.. currentmodule:: omicverse
```

## 数据输入/输出

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   read
   io.read_h5ad
   io.read_h5ad
   io.read_10x_h5
   io.read_10x_mtx
   io.read_nanostring
   io.read_visium_hd
```

## 预处理 (pp)

_质量控制与过滤_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.qc
   pp.filter_cells
   pp.filter_genes
   pp.scrublet
```

_归一化与特征选择_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.normalize_total
   pp.log1p
   pp.highly_variable_genes
   pp.highly_variable_features
   pp.normalize_pearson_residuals
   pp.recover_counts
```

_降维与图构建_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.pca
   pp.neighbors
   pp.umap
   pp.tsne
   pp.mde
```

_聚类_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.leiden
   pp.louvain
```

_批次校正与缩放_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.scale
   pp.regress
   pp.regress_and_scale
   pp.remove_cc_genes
   pp.score_genes_cell_cycle
```

## 单细胞 (single)

_注释_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.pySCSA
   single.MetaTiME
   single.CellVote
   single.gptcelltype
   single.gptcelltype_local
   single.CellOntologyMapper
   single.Annotation
   single.AnnotationRef
```

_轨迹与细胞命运_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.TrajInfer
   single.Velo
   single.Fate
   single.cytotrace2
```

_细胞结构_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.MetaCell
   single.DEG
   single.SCENIC
   single.aucell
   single.geneset_aucell
   single.cellphonedb_v5
   single.Drug_Response
```

_批次校正与整合_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.Batch
   single.pySIMBA
   single.Integration
```

_多组学_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.pyMOFA
   single.pyMOFAART
   single.GLUE_pair
   single.pyTOSICA
```

_主题建模_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.cNMF
```

## Bulk RNA-seq (bulk)

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   bulk.pyDEG
   bulk.pyGSEA
   bulk.pyPPI
   bulk.pyWGCNA
   bulk.pyTCGA
   bulk.Deconvolution
   bulk.Matrix_ID_mapping
   bulk.batch_correction
   bulk.geneset_enrichment
```

## 空间转录组学 (space)

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   space.clusters
   space.Deconvolution
   space.pySTAGATE
   space.pySTAligner
   space.pySpaceFlow
   space.Tangram
   space.STT
   space.GASTON
   space.Cal_Spatial_Net
   space.spatial_neighbors
   space.moranI
```

## Bulk 转单细胞 (bulk2single)

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   bulk2single.BulkTrajBlend
   bulk2single.Bulk2Single
   bulk2single.Single2Spatial
```

## 基础模型 (fm)

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   fm.run
   fm.list_models
   fm.get_registry
   fm.describe_model
   fm.select_model
   fm.preprocess_validate
   fm.profile_data
   fm.interpret_results
   fm.ModelSpec
   fm.ModelRegistry
```

## 绘图 (pl)

_嵌入与降维_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.embedding
   pl.embedding_celltype
   pl.embedding_density
   pl.embedding_multi
   pl.embedding_atlas
   pl.pca
   pl.umap
   pl.tsne
```

_差异表达_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.volcano
   pl.marker_heatmap
   pl.rank_genes_groups_dotplot
   pl.dotplot
   pl.markers_dotplot
```

_细胞比例与组成_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.cellproportion
   pl.cellstackarea
   pl.venn
   pl.bardotplot
```

_分布_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.violin
   pl.violin_box
   pl.boxplot
   pl.plot_boxplots
```

_空间_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.spatial
   pl.plot_spatial
   pl.highlight_spatial_region
```

_细胞通信_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.cpdb_heatmap
   pl.cpdb_network
   pl.cpdb_chord
   pl.CellChatViz
```

_颜色与调色板_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.palette_112
   pl.palette_28
   pl.sc_color
   pl.ForbiddenCity
   pl.optim_palette
   pl.colormaps_palette
```

## 数据集

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   datasets.pbmc3k
   datasets.zebrafish
   datasets.pancreatic_endocrinogenesis
   datasets.dentate_gyrus
   datasets.create_mock_dataset
   datasets.predefined_signatures
```

[anndata]: https://anndata.readthedocs.io/en/stable/
[scanpy]: https://scanpy.readthedocs.io/en/stable/index.html
