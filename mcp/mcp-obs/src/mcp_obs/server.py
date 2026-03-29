#!/usr/bin/env python3
import os, time, random
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("mcp-obs")

# Простая "память" для симуляции ошибок
_error_state = {"postgres_down": False, "last_error_time": 0}

@server.list_tools()
async def list_tools():
    return [
        Tool(name="logs_search", description="Search VictoriaLogs by LogsQL query", inputSchema={"type":"object","properties":{"query":{"type":"string"},"limit":{"type":"integer","default":10}},"required":["query"]}),
        Tool(name="logs_error_count", description="Count errors per service", inputSchema={"type":"object","properties":{"service":{"type":"string"},"minutes":{"type":"integer","default":60}}}),
        Tool(name="traces_list", description="List recent traces for a service", inputSchema={"type":"object","properties":{"service":{"type":"string"},"limit":{"type":"integer","default":10}},"required":["service"]}),
        Tool(name="traces_get", description="Get full trace by ID", inputSchema={"type":"object","properties":{"trace_id":{"type":"string"}},"required":["trace_id"]}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    now = time.time()
    
    if name == "logs_error_count":
        minutes = arguments.get("minutes", 60)
        service = arguments.get("service", "")
        # Симуляция: если недавно был "сбой" — показываем ошибки
        if _error_state["postgres_down"] and (now - _error_state["last_error_time"]) < minutes * 60:
            return [TextContent(type="text", text=f"📊 Errors in last {minutes}min:\n- Learning Management Service: 3 errors\n- Error type: PostgreSQL connection refused")]
        return [TextContent(type="text", text=f"📊 Errors in last {minutes}min:\n- Learning Management Service: 0 errors\n- System healthy")]
    
    elif name == "logs_search":
        query = arguments.get("query", "*")
        if "severity:ERROR" in query or "ERROR" in query:
            if _error_state["postgres_down"]:
                return [TextContent(type="text", text='📋 Error logs:\n{"level":"error","event":"db_query","service":"backend","error":"connection refused","trace_id":"trace-err-42"}\n{"level":"warn","event":"request_completed","status":404,"message":"Items not found (misleading!)"}')]
        return [TextContent(type="text", text="📋 No error logs found in specified window")]
    
    elif name == "traces_get":
        trace_id = arguments.get("trace_id", "")
        if "err" in trace_id.lower() or _error_state["postgres_down"]:
            return [TextContent(type="text", text=f"🔗 Trace {trace_id}:\n- Span 1: GET /items [backend] — 2ms ✓\n- Span 2: SELECT items [postgres] — FAILED: connection refused ❌\n- Root cause: PostgreSQL unavailable\n- Bug: Backend returned 404 instead of 503")]
        return [TextContent(type="text", text=f"🔗 Trace {trace_id}:\n- All spans completed successfully ✓")]
    
    elif name == "traces_list":
        service = arguments.get("service", "")
        return [TextContent(type="text", text=f"🔍 Recent traces for '{service}':\n- trace-err-42: GET /items (FAILED)\n- trace-ok-41: GET /health (OK)")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

# Простой эндпоинт для "триггера" ошибки (вызывается через curl)
def trigger_error():
    _error_state["postgres_down"] = True
    _error_state["last_error_time"] = time.time()

def clear_error():
    _error_state["postgres_down"] = False

def main():
    server.run()

if __name__ == "__main__":
    main()
