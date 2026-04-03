# OmicVerse 以注册表为中心的 Agent 架构

```text
OmicVerse registry-centered agent architecture
==============================================

[Source code layer]
    |
    |  Public API definitions in OmicVerse modules
    |  ------------------------------------------------------------
    |  A. Explicitly registered entry points
    |     - @register_function on functions
    |     - @register_function on classes
    |
    |  B. Latent capabilities hidden inside registered objects
    |     - public class methods
    |     - string-dispatch branches
    |       e.g. method='dynamo'
    |            backend='scvelo'
    |            method='bayesprism'
    |            method='regdiffusion'
    |
    |  C. Backend evidence inside branch bodies
    |     - import dynamo
    |     - import regdiffusion
    |     - import celltypist
    |     - from ... import Prism
    v

[Registry build layer: FunctionRegistry.register]
    |
    |  1. Build canonical runtime entry
    |     ------------------------------------------------------------
    |     fields:
    |     - function
    |     - full_name
    |     - short_name
    |     - module
    |     - aliases
    |     - category
    |     - description
    |     - examples
    |     - related
    |     - signature
    |     - parameters
    |     - docstring
    |     - prerequisites / requires / produces
    |     - source = runtime
    |     - virtual_entry = False
    |
    |  2. Derive method-level virtual entries from registered classes
    |     ------------------------------------------------------------
    |     e.g.
    |     - omicverse.single._velo.Velo.moments
    |     - omicverse.single._scenic.SCENIC.cal_grn
    |
    |  3. Derive branch-level virtual entries from selector branches
    |     ------------------------------------------------------------
    |     e.g.
    |     - ...Velo.moments[backend=dynamo]
    |     - ...Deconvolution.deconvolution[method=bayesprism]
    |     - ...SCENIC.cal_grn[method=regdiffusion]
    |
    |  4. Attach branch metadata
    |     ------------------------------------------------------------
    |     - source = runtime_derived_method / runtime_derived_branch
    |     - virtual_entry = True
    |     - parent_full_name
    |     - branch_parameter
    |     - branch_value
    |     - imports
    |
    |  5. Store all entries into _global_registry
    v

[_global_registry]
    |
    |  Searchable memory structure
    |  ------------------------------------------------------------
    |  contains:
    |  - canonical registered entries
    |  - virtual method entries
    |  - virtual branch entries
    |
    |  searchable over:
    |  - full_name
    |  - short_name
    |  - aliases
    |  - category
    |  - description
    |  - docstring
    |  - examples
    |  - related
    |  - imports
    v

[Hydration layer: ensure_registry_populated()]
    |
    |  Problem:
    |  OmicVerse uses lazy imports, so decorators do not fire until modules load.
    |
    |  Hydration procedure:
    |  ------------------------------------------------------------
    |  1. Read PHASE_WHITELIST from MCP overrides
    |  2. Convert whitelisted full_names -> module paths
    |  3. Try importlib.import_module(module)
    |  4. If package import fails for any reason:
    |     - attempt direct leaf-module loading
    |     - bypass fragile package __init__ chains
    |  5. Decorators execute
    |  6. _global_registry becomes populated
    v

[Export layer]
    |
    |  export_registry(filepath)
    |  ------------------------------------------------------------
    |  serializes unique entries from _global_registry
    |  output fields include:
    |  - full_name / short_name / module
    |  - aliases / category / description / examples
    |  - signature / docstring
    |  - source
    |  - virtual_entry
    |  - parent_full_name
    |  - branch_parameter
    |  - branch_value
    |  - imports
    v

[MCP manifest layer]
    |
    |  build_registry_manifest(...)
    |  ------------------------------------------------------------
    |  uses _global_registry as source of truth
    |  BUT filters out virtual_entry == True
    |
    |  rationale:
    |  - searchable branch variants should aid retrieval
    |  - they should not be exposed as independently executable tools
    v

[Agent initialization: OmicVerseAgent.__init__]
    |
    |  1. initialize skill registry
    |  2. hydrate / access registry context
    |  3. build system prompt
    |  4. create tool runtime + turn controller
    |
    |  system prompt contents
    |  ------------------------------------------------------------
    |  - OmicVerse task instructions
    |  - workflow rules
    |  - code quality rules
    |  - full registry summary text
    |  - skill catalog overview
    v

[Reasoning-time tool use]
    |
    |  Jarvis / Claw agentic loop
    |  ------------------------------------------------------------
    |  inspect_data()     -> understand current dataset state
    |  search_functions() -> query _global_registry
    |  search_skills()    -> retrieve workflow guidance
    |  execute_code()     -> final OmicVerse code action
    |  finish()           -> terminate turn
    |
    |  retrieval examples
    |  ------------------------------------------------------------
    |  query = "dynamo"
    |  -> Velo.moments[backend=dynamo]
    |  -> Velo.dynamics[backend=dynamo]
    |  -> Velo.cal_velocity[method=dynamo]
    |
    |  query = "bayesprism"
    |  -> Deconvolution.deconvolution[method=bayesprism]
    |
    |  query = "regdiffusion"
    |  -> SCENIC.cal_grn[method=regdiffusion]
    v

[Interface split]
    |
    |  Jarvis
    |  ------------------------------------------------------------
    |  - same agent
    |  - same registry
    |  - same skills
    |  - same search_functions / search_skills logic
    |  - execute_code really runs
    |
    |  Claw
    |  ------------------------------------------------------------
    |  - same agent
    |  - same registry
    |  - same skills
    |  - same search_functions / search_skills logic
    |  - execute_code is intercepted
    |  - final code is captured and returned without execution
    v

[Outcome]
    |
    |  Registry serves three roles simultaneously:
    |  ------------------------------------------------------------
    |  1. capability index for discovery
    |  2. prompt-grounding substrate for the agent
    |  3. exportable machine-readable API/capability snapshot
```

我们在 OmicVerse 中实现了以注册表为中心的 agent 架构，旨在使分析能力可被机器读取、可检索，并通过统一接口可执行。在该设计中，运行时注册表（而非全仓库源码搜索）被视为可用功能的主要表示形式。OmicVerse 的公共功能通过 `@register_function` 进行声明，该装饰器记录符号和语义元数据，包括别名、类别标签、自然语言描述、示例、相关条目、函数签名以及状态注释（如前提条件、所需数据结构和预期输出）。每个被装饰的对象在 `_global_registry` 中生成一个规范的运行时条目，建立起 OmicVerse 公共抽象与 agent 可消费表示之间的显式映射。

仅靠装饰器注册对 OmicVerse 而言是不够的，因为大量具有生物学意义的功能并非作为独立的顶层函数暴露。许多工作流程以类的形式实现，真正的分析操作位于公共方法中；许多特定后端的行为则通过字符串分发分支进行选择，如 `method='dynamo'`、`backend='scvelo'`、`method='bayesprism'` 或 `method='regdiffusion'`。为了恢复这些隐藏的功能，注册表在运行时使用抽象语法树分析对每个注册对象进行展开。注册类被转换为方法级虚拟条目，包含选择器分支的方法或函数进一步展开为分支特定的虚拟条目。这些派生条目保留了父可调用对象的语义上下文，同时添加了分支特定的元数据，包括选择器参数、选择器值和分支内的导入证据。这使注册表能够表示如 `Velo.cal_velocity[method=dynamo]`、`Deconvolution.deconvolution[method=bayesprism]` 和 `SCENIC.cal_grn[method=regdiffusion]` 等功能变体，即使这些变体并非独立的顶层 API。

由此产生的 `_global_registry` 是一个可搜索的功能图谱，而非简单的名称映射。条目可以通过全名、短名、别名、类别、描述、文档字符串、示例、相关函数注释和后端导入 token 进行匹配。这对自然语言 agent 使用尤为重要，因为用户通常引用后端包名或工作流程名，而非确切的 OmicVerse 封装符号。通过将导入证据和选择器值作为可搜索字段保留，注册表可以将以后端为导向的请求解析为对应的 OmicVerse 封装分支。该设计大幅提升了工作流程的检索精度，特别是那些科学标识由内部后端选择而非唯一顶层函数名承载的工作流程。

由于 OmicVerse 使用惰性导入，因此不能在解释器启动时假设注册表已完整填充。为此，我们使用显式的注水过程 `ensure_registry_populated()`，在检索或 agent 推理开始前加载精选的模块白名单。注水过程首先尝试标准模块导入，当包初始化失败时，回退到直接的叶模块加载，以绕过脆弱的包 `__init__` 链。这种行为是必要的，因为某些包级导入会传递激活重型或环境敏感的依赖。回退加载器允许装饰器执行并构建注册表条目，即使更广泛的包导入图并不完全稳定。在当前实现中，这对于保证公共类工作流程（如 `SCENIC`）的稳定注册至关重要，从而允许下游分支展开将 `regdiffusion`、`grnboost2` 和 `genie3` 作为可检索的变体暴露出来。

相同的运行时注册表被用于两个相关但不同的下游产品。首先，它通过 `export_registry(...)` 导出为机器可读的 JSON 快照，同时保留规范条目和派生的虚拟条目，以及 `source`、`virtual_entry`、`parent_full_name`、`branch_parameter`、`branch_value` 和 `imports` 等元数据。这一丰富的导出旨在用于调试、接口检查和外部集成。其次，注册表被转换为用于工具执行的 MCP 清单。在这第二条路径中，虚拟条目被有意过滤掉。理由是分支派生条目是面向检索的抽象，而非可独立执行的工具。将表达性强的功能表示与可执行清单分离，使 OmicVerse 能够在不将合成的分支变体呈现为独立工具调用的情况下保持高发现召回率。

`OmicVerseAgent` 同时将此注册表用作初始化上下文和运行时检索基础。在初始化期间，agent 构建一个包含工作流规则、代码质量约束、注册表派生的 OmicVerse 可用函数摘要以及精选 skill 概述的系统提示。然而在交互式推理期间，功能基础并不仅依赖初始提示。agent 可以调用 `search_functions()` 查询 `_global_registry`，调用 `search_skills()` 检索工作流指导，调用 `inspect_data()` 表征当前数据集，以及调用 `execute_code()` 执行或生成最终的 OmicVerse 分析代码。这样，注册表充当可在规划过程中重新查阅的可更新本地记忆，而非静态的提示附录。包含后端名称（如 `dynamo`、`bayesprism` 或 `regdiffusion`）的查询，因此可以通过与普通函数发现相同的机制检索到对应的 OmicVerse 封装。

这一以注册表为中心的推理路径在 Jarvis 和 Claw 之间共享。Jarvis 使用完整的 agent 循环来检查数据、搜索注册表、检索 skill，并对实时对象执行代码。Claw 复用相同的 OmicVerse agent、相同的运行时注册表、相同的 skill 系统以及相同的工具级检索逻辑，但拦截了最终的 `execute_code()` 操作，使得最终 Python 程序被捕获而非运行。Jarvis 与 Claw 之间的差异因此仅限于执行语义，而非功能发现或规划。因此，注册表表达能力的任何提升都将直接惠及两个接口。一旦工作流对象或特定后端分支在 `_global_registry` 中有所表示，它就同时可用于 Jarvis 的交互式执行和 Claw 的纯代码合成。

该设计解决了生物信息学 agent 中的一个常见失败模式，即功能发现滞后于包的真实操作界面。仅靠装饰器的注册表会遗漏隐藏的分支特定方法，而不受约束的源码搜索则会将内部实现细节与用户可见功能混淆。通过结合显式注册、运行时方法和分支展开、鲁棒的注水机制以及面向检索的搜索语义，OmicVerse 维护了一个更忠实地表示其分析功能的注册表。该注册表因此同时作为功能索引、提示基础基底，以及面向下游 agent 系统的可导出接口描述。
