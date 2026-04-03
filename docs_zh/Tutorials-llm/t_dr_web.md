---
title: 领域研究 (dr) — 实时网络搜索
---

本指南介绍如何使用 `omicverse.llm.domain_research` 配合实时网络搜索检索器，生成一份来源于互联网的、含引用的综合性报告。

前提条件：
- 可选但推荐：设置 `TAVILY_API_KEY` 以使用 Tavily 后端。
- 对于 DuckDuckGo 后端，安装 `duckduckgo_search` 和 `beautifulsoup4` 以获得更佳效果。

快速开始（自动选择后端）：

```python
from omicverse.llm.domain_research import ResearchManager

# 最简方式：`vector_store="web"` 会在设置了 TAVILY_API_KEY 时自动选择 Tavily，
# 否则回退到 DuckDuckGo。
rm = ResearchManager(vector_store="web")
report = rm.run("State-of-the-art methods for single-cell integration in 2024")
print(report)
```

强制指定后端或调整检索参数：
- 使用 `vector_store="web:tavily"` 或 `vector_store="web:duckduckgo"` 强制指定后端。
- 如需手动控制（例如 `max_results`、`fetch_content`），可直接导入并实例化 `WebRetrieverStore`。

使用技巧：
- `fetch_content=True` 会从结果 URL 中抓取并提取正文文本。设置为 `False` 则仅依赖摘要片段。
- 结合 LLM 合成器可生成更高质量的执行摘要：

```python
import os
from omicverse.llm.domain_research.write.synthesizer import PromptSynthesizer

synth = PromptSynthesizer(
    model="gpt-4o-mini",
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY", ""),
)
rm = ResearchManager(vector_store="web", synthesizer=synth)
print(rm.run("Multi-omics integration benchmarks 2023–2025"))
```

故障排查：
- Tavily：请确认 `TAVILY_API_KEY` 已正确设置且有效。
- DuckDuckGo：建议使用 `duckduckgo_search` 包以获得最佳稳定性；否则 HTML 回退方式可能受到频率限制或因网站变更而失效。
- 若页面不是 HTML 格式或位于付费墙后，抓取器将返回原始响应文本（截断）作为文档正文。
