---
name: bilibili-history-mcp
description: Use when an AI client needs to read BilibiliHistoryFetcher data through its read-only LAN MCP server without loading the full project context.
---

# Bilibili History MCP

Use the project's MCP server instead of reading files directly when the user asks for local Bilibili history, yearly reports, viewing analytics, interaction records, video details, scheduler status, or data health.

## Start Here

1. Read `bili://project/overview`.
2. Read `bili://project/data-status`.
3. Read `bili://project/tool-guide` only when choosing a tool is unclear.

## Tool Rules

- Prefer summary tools before record tools.
- Always paginate record tools; keep `size` small unless the user asks for bulk analysis.
- Use `query_history_records` for browsing and `search_history_records` for keyword lookup.
- Use `get_annual_summary`, `get_viewing_analytics`, and `get_title_analytics` for analysis.
- Use `query_interaction_records` only after `get_interaction_summary` when details are needed.
- Do not ask for write operations; this MCP intentionally does not expose sync, fetch, download, delete, login, reset, or config update.

## Privacy

The MCP is LAN HTTP with Bearer Token auth. Treat returned watch history as private user data. Do not request secrets such as SESSDATA, bili_jct, email passwords, or config tokens.
