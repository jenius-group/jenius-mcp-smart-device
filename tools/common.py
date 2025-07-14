"""
Jenius 工具包 - 通用模块

该模块包含了扩展工具包的通用功能：
- 环境变量加载
- MCP服务初始化
"""

from mcp.server.fastmcp import FastMCP
from utils.logger import logger

# 初始化 MCP
mcp = FastMCP("jenius-mcp-smart-device")
logger.info("MCP server is started!")