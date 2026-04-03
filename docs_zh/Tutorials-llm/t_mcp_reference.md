---
title: OmicVerse MCP 参考文档
---

# OmicVerse MCP 参考文档

本页面是服务器标志、工具计数、返回信封和常见错误模式的简洁技术参考。

## CLI 标志

| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--phase` | `P0+P0.5` | 要暴露的部署阶段 |
| `--transport` | `stdio` | `stdio` 或 `streamable-http` |
| `--session-id` | `default` | 会话标识符 |
| `--persist-dir` | tempdir | `ov.persist_adata` 的持久化目录 |
| `--max-adata` | `50` | AnnData 句柄的最大数量 |
| `--max-artifacts` | `200` | artifact 句柄的最大数量 |
| `--host` | `127.0.0.1` | HTTP 绑定主机 |
| `--port` | `8765` | HTTP 绑定端口 |
| `--http-path` | `/mcp` | HTTP 路由路径 |
| `--version` | — | 显示版本 |

## 当前工具计数

来自当前服务器的实际计数：

| 阶段选择 | 工具总数 |
|----------------|-------------|
| `P0` | 40 |
| `P0+P0.5` | 53 |
| `P0+P0.5+P2` | 58 |

细分：

- `P0`：15 个分析工具
- `P0.5`：13 个额外分析工具
- `P2`：5 个高级分析工具
- 元工具：25 个

## 响应信封

大多数工具调用返回如下结构：

```json
{
  "ok": true,
  "tool_name": "ov.utils.read",
  "summary": "Loaded AnnData",
  "outputs": [],
  "state_updates": {},
  "warnings": []
}
```

失败时使用：

```json
{
  "ok": false,
  "error_code": "missing_data_requirements",
  "message": "Missing required data",
  "details": {},
  "suggested_next_tools": []
}
```

## JSON-RPC 示例

### `tools/list`

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### `tools/call`

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "ov.utils.read",
    "arguments": {
      "path": "pbmc3k.h5ad"
    }
  }
}
```

使用 Claude Code 或 Claude Desktop 时，通常不需要手动发送原始 JSON-RPC。

## 常见输出类型

- `object_ref`：通常是 `adata_id` 或 `instance_id`
- `json`：结构化表格或元数据
- `image`：绘图结果

## 典型错误码

| 错误码 | 含义 |
|-----------|---------|
| `missing_session_object` | 未找到 `adata_id` 或其他句柄 |
| `missing_data_requirements` | 缺少前提数据，如 `scaled` 或 `X_pca` |
| `tool_unavailable` | 工具存在但因依赖或部署状态而无法执行 |
| `execution_failed` | 底层工具抛出错误 |

## 通用 stdio 客户端示例

```python
import subprocess
import json

proc = subprocess.Popen(
    ["python", "-m", "omicverse.mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
proc.stdin.write(json.dumps(request) + "\n")
proc.stdin.flush()
response = json.loads(proc.stdout.readline())
print(f"Available tools: {len(response['result']['tools'])}")

call_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "ov.utils.read",
        "arguments": {"path": "pbmc3k.h5ad"},
    },
}
proc.stdin.write(json.dumps(call_request) + "\n")
proc.stdin.flush()
print(json.loads(proc.stdout.readline()))
```

## 常用元工具

- `ov.list_tools`
- `ov.describe_tool`
- `ov.get_session`
- `ov.list_handles`
- `ov.get_trace`
- `ov.list_traces`
- `ov.get_health`

## 相关页面

- 概述：[指南](t_mcp_guide.md)
- 快速配置：[快速开始](t_mcp_quickstart.md)
- 客户端：[客户端与部署](t_mcp_clients.md)
- 运行时详情：[运行时与故障排查](t_mcp_runtime.md)
