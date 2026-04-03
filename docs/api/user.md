# User API

Import OmicVerse as:

```python
import omicverse as ov
```

```{eval-rst}
.. currentmodule:: omicverse
```

## Data IO

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

## Preprocessing (pp)

_Quality control & filtering_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.qc
   pp.filter_cells
   pp.filter_genes
   pp.scrublet
```

_Normalisation & feature selection_

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

_Dimensionality reduction & graph_

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

_Clustering_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pp.leiden
   pp.louvain
```

_Batch correction & scaling_

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

## Single-cell (single)

_Annotation_

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

_Trajectory & cell fate_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.TrajInfer
   single.Velo
   single.Fate
   single.cytotrace2
```

_Cell structure_

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

_Batch correction & integration_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.Batch
   single.pySIMBA
   single.Integration
```

_Multi-omics_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   single.pyMOFA
   single.pyMOFAART
   single.GLUE_pair
   single.pyTOSICA
```

_Topic modelling_

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

## Spatial transcriptomics (space)

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

## Bulk-to-Single (bulk2single)

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   bulk2single.BulkTrajBlend
   bulk2single.Bulk2Single
   bulk2single.Single2Spatial
```

## Foundation Models (fm)

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

## Plotting (pl)

_Embedding & dimensionality_

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

_Differential expression_

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

_Cell proportion & composition_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.cellproportion
   pl.cellstackarea
   pl.venn
   pl.bardotplot
```

_Distribution_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.violin
   pl.violin_box
   pl.boxplot
   pl.plot_boxplots
```

_Spatial_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.spatial
   pl.plot_spatial
   pl.highlight_spatial_region
```

_Cell communication_

```{eval-rst}
.. autosummary::
   :toctree: reference/
   :nosignatures:

   pl.cpdb_heatmap
   pl.cpdb_network
   pl.cpdb_chord
   pl.CellChatViz
```

_Colours & palettes_

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

## Datasets

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
