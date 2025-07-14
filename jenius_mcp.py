# Jenius MCP smart device Server 启动入口
import os
import asyncio
import argparse
from typing import Any
from tools.common import mcp
from dotenv import load_dotenv
from utils.logger import logger

# 清除所有环境变量
os.environ.clear()

# 重新加载环境变量
load_dotenv(dotenv_path=".mcp.env")

# 验证环境变量加载
# logger.info("当前所有环境变量：")
# for key, value in os.environ.items():
#     logger.info(f"{key}: {value}")

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='Jenius smart device MCP 服务器')
    parser.add_argument(
        '--port', 
        type=int, 
        default=int(os.getenv("JENIUS_SMART_DEVICE_MCP_SSE_PORT", 8981)),
        help='服务器端口号 (默认: 8981)'
    )
    parser.add_argument(
        '--transport', 
        type=str, 
        default=os.getenv("JENIUS_SMART_DEVICE_MCP_TRANSPORT", "stdio"),
        help='传输方式 (默认: stdio)'
    )
    parser.add_argument(
        '--host', 
        type=str, 
        default=os.getenv("JENIUS_SMART_DEVICE_MCP_HOST", "0.0.0.0"),
        help='服务器地址 (默认: 0.0.0.0)'
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 使用传入的端口号或默认值
    mcp.settings.host = args.host
    mcp.settings.port = args.port
    mcp.settings.log_level = os.getenv("JENIUS_SMART_DEVICE_MCP_LOG_LEVEL", "DEBUG")

    mcp.settings.sse_path = os.getenv("JENIUS_SMART_DEVICE_MCP_SSE_PATH", "/sse")
    mcp.settings.message_path = os.getenv("JENIUS_SMART_DEVICE_MCP_MESSAGE_PATH", "/messages/")

    transport = args.transport
    logger.info("当前启动的MCP Server 配置：")
    logger.info("host: %s" % mcp.settings.host)
    logger.info("port: %s" % mcp.settings.port)
    logger.info("transport: %s" % transport)
    logger.info("sse_path: %s" % mcp.settings.sse_path)
    logger.info("message_path: %s" % mcp.settings.message_path)
    
    asyncio.run(mcp.run(transport=transport))
    # asyncio.run(mcp.run(transport="sse"))
    # asyncio.run(mcp.run(transport="streamable-http"))