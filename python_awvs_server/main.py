# -*- coding: utf-8 -*-
import httpx
import asyncio
from typing import Any, Dict, Coroutine
from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Acunetix API 配置
ACUNETIX_API_URL = "https://localhost:3443/api/v1"
ACUNETIX_API_KEY = "your_api_key_here"
headers = {"X-Auth": ACUNETIX_API_KEY, "Content-type": "application/json;charset=utf8"}

# 初始化 MCP Server
mcp = FastMCP("Acunetix-MCP-Server")
request_session = httpx.AsyncClient(headers=headers, verify=False)

# 通用的异步请求函数
async def _make_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any] | None:
    url = f"{ACUNETIX_API_URL}{endpoint}"
    try:
        if method == "GET":
            response = await request_session.get(url, params=data)
        elif method == "POST":
            response = await request_session.post(url, json=data)
        elif method == "PUT":
            response = await request_session.put(url, json=data)
        elif method == "DELETE":
            response = await request_session.delete(url, json=data)
        else:
            raise ValueError("Unsupported HTTP method")
        
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return None

# 获取所有目标信息
@mcp.tool()
async def get_all_targets() -> Dict[str, Any] | None:
    return await _make_request("GET", "/targets")

# 添加扫描目标
@mcp.tool()
async def add_target(address: str, description: str = "", criticality: int = 10) -> Dict[str, Any] | None:
    data = {
        "address": address,
        "description": description,
        "criticality": criticality
    }
    return await _make_request("POST", "/targets", data)

# 启动扫描任务
@mcp.tool()
async def start_scan(target_id: str, profile_id: str = "11111111-1111-1111-1111-111111111112") -> Dict[str, Any] | None:
    data = {
        "target_id": target_id,
        "profile_id": profile_id,
        "schedule": {
            "disable": False,
            "start_date": None,
            "time_sensitive": False
        }
    }
    return await _make_request("POST", "/scans", data)

# 获取最新扫描任务的扫描 ID
@mcp.tool()
async def get_latest_scan_id() -> str | None:
    response = await _make_request("GET", "/scans")
    if response and "scans" in response:
        return response["scans"][0].get("scan_id")
    return None

# 生成扫描报告
@mcp.tool()
async def generate_report(scan_id: str, template_id: str = "11111111-1111-1111-1111-111111111115") -> Dict[str, Any] | None:
    data = {
        "template_id": template_id,
        "source": {
            "list_type": "scans",
            "id_list": [scan_id]
        }
    }
    return await _make_request("POST", "/reports", data)

# 下载扫描报告
@mcp.tool()
async def download_report(report_id: str, report_type: str = "html") -> None:
    response = await _make_request("GET", f"/reports/{report_id}")
    if response and "download" in response:
        report_url = response["download"][0 if report_type == "html" else 1]
        report_url_full = f"{ACUNETIX_API_URL}{report_url}"
        report_response = await _make_request("GET", report_url_full)
        if report_response:
            time_now = datetime.now().strftime('%Y-%m-%d %H%M%S')
            with open(f"report-{time_now}.{report_type}", "wb") as file:
                file.write(report_response.content)

# 获取扫描结果
@mcp.tool()
async def get_scan_results(scan_id: str) -> Dict[str, Any] | None:
    return await _make_request("GET", f"/scans/{scan_id}/results")

# 获取扫描结果中的漏洞信息
@mcp.tool()
async def get_scan_vulnerabilities(scan_id: str, result_id: str) -> Dict[str, Any] | None:
    return await _make_request("GET", f"/scans/{scan_id}/results/{result_id}/vulnerabilities")

# 获取扫描结果中的技术信息
@mcp.tool()
async def get_scan_technologies(scan_id: str, result_id: str) -> Dict[str, Any] | None:
    return await _make_request("GET", f"/scans/{scan_id}/results/{result_id}/technologies")

# 获取扫描结果中的爬取数据
@mcp.tool()
async def get_scan_crawldata(scan_id: str, result_id: str) -> Dict[str, Any] | None:
    return await _make_request("GET", f"/scans/{scan_id}/results/{result_id}/crawldata")

# 获取扫描结果中的统计信息
@mcp.tool()
async def get_scan_statistics(scan_id: str, result_id: str) -> Dict[str, Any] | None:
    return await _make_request("GET", f"/scans/{scan_id}/results/{result_id}/statistics")

# 主程序入口
if __name__ == "__main__":
    mcp.run(transport='sse')
