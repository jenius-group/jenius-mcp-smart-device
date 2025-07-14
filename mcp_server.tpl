# This is an MCP server template
# You can build up your own MCP servers with respect to this file
# The MCP servers run on Python 3.12
# All MCP servers must be put under ./tools/mcp to be properly loaded

"""

    MCP服务器描述

"""


####################
# Global vairables #
####################
BASE_URL = ...
HEADERS = ...
FIRST_ENTITY_ID = ...
SECOND_ENTITY_ID = ...


###############
# MCP servers #
###############
@mcp.tool()
async def sample_funtion_one(
    **params, 
) -> str:
    """
    该函数功能的描述信息，大模型以此为参考并调用。
    """

    try:

        # 功能实现

    except Exception as e:
        
        # 错误抓取

    # 返回结果


@mcp.tool()
async def sample_funtion_two(
    **params, 
) -> str:
    """
    该函数功能的描述信息，大模型以此为参考并调用。
    """

    try:

        # 功能实现

    except Exception as e:
        
        # 错误抓取

    # 返回结果