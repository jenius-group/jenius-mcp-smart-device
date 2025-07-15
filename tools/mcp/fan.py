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

import os
import json
import requests
from typing import Literal
from pydantic import Field

from tools.common import mcp
from utils.logger import logger
from utils.error import error_json_msg


"""

    本MCP服务器用于控制连接智能插座的风扇开关，核心是对于智能插座的控制，包含以下功能：

        1. switch_fan()  # 控制电扇开关

"""


####################
# Global vairables #
####################
FAN_BASE_URL = os.getenv('FAN_BASE_URL')
FAN_HEADERS = json.loads(os.getenv('FAN_HEADERS'))


###############
# MCP servers #
###############
@mcp.tool()
async def switch_fan(
    action: Literal["open", "close"] = Field(description="要执行的操作类型: 打开电扇或者关闭电扇。必须从两个选项中选择一个"), 
) -> str:
    """
    控制电扇开关的流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if action not in ['open', 'close']:
            return error_json_msg('不支持的开关操作类型。仅支持 open, close。请核对后重新输入。')
        logger.info(f"Current action: {action}")
        # Request body formation
        data = {"ctrl_cmd": {f"{action}_relay_cmd": {}}}
        # HTTP request
        response = requests.post(FAN_BASE_URL, headers=FAN_HEADERS, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            response_json['message'] = f"操作成功！"
            response_json['status_code'] = 200

        # response_json = response.json()

    except requests.exceptions.RequestException as e:
        response_json['message'] = f"操作运行失败！错误内容：HTTP请求失败，原因：{str(e)}"
        response_json['status_code'] = 299
    except Exception as e:
        response_json['message'] = f"操作运行失败！错误内容: {str(e)}"
        response_json['status_code'] = 299

    logger.info(response_json)
    return response_json