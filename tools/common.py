#    Copyright 2025 jenius-group

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


"""
Jenius Smart Device 工具包 - 通用模块

该模块包含了扩展工具包的通用功能：
- MCP服务初始化
"""


from mcp.server.fastmcp import FastMCP
from utils.logger import logger


# 初始化 MCP
mcp = FastMCP("jenius-mcp-smart-device")
logger.info("MCP server is started!")