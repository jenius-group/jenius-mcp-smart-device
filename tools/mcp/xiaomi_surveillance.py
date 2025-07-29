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

    本MCP服务器用于控制小米智能摄像机的开关机和夜视模式切换，包含以下两个功能：

        1. switch_xiaomi_smart_surveillance()            # 开关机
        2. night_vision_mode_xiaomi_smart_surveillance() # 夜视模式切换

"""


####################
# Global vairables #
####################
CONTROL_CENTER_BASE_URL = os.getenv('CONTROL_CENTER_BASE_URL')
CONTROL_CENTER_HEADERS = json.loads(os.getenv('CONTROL_CENTER_HEADERS'))
SWITCH_ENTITY_ID = os.getenv('XIAOMI_SMART_SURVEILLANCE_SWITCH_ENTITY_ID')
MODE_SELECT_ENTITY_ID = os.getenv('XIAOMI_SMART_SURVEILLANCE_NIGHT_VISION_MODE_SELECT_ENTITY_ID')


###############
# MCP servers #
###############
@mcp.tool()
async def switch_xiaomi_smart_surveillace(
    action: Literal["turn_on", "turn_off"] = Field(description="要执行的操作类型: 打开或者关闭。必须从两个选项中选择一个"), 
) -> str:
    """
    控制小米智能摄像机的开关机流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if action not in ['turn_on', 'turn_off']:
            return error_json_msg('不支持的开关操作类型。仅支持 turn_on, turn_off。请核对后重新输入。')
        logger.info(f"Current action: {action}")
        # Request body formation
        domain = SWITCH_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/{action}"
        data = {
            "entity_id": SWITCH_ENTITY_ID
        }
        # HTTP request
        response = requests.post(request_url, headers=CONTROL_CENTER_HEADERS, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            response_json['message'] = f"操作成功！"
            response_json['status_code'] = 200

    except requests.exceptions.RequestException as e:
        response_json['message'] = f"操作运行失败！错误内容：HTTP请求失败，原因：{str(e)}"
        response_json['status_code'] = 299
    except Exception as e:
        response_json['message'] = f"操作运行失败！错误内容: {str(e)}"
        response_json['status_code'] = 299

    logger.info(f"{response_json}")
    return response_json


@mcp.tool()
async def mode_xiaomi_smart_surveillance(
    mode: Literal["Off", "Auto", "On"] = Field(description="智能摄像机的运行模式，从三个模式:Off、Auto、On当中选择一个")
) -> str:
    """
    控制小米智能摄像机夜视模式的流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()
    ACTION = "select_option" # not an option so we initialize it manually

    try:

        # Sanity check
        if mode not in ['Off', 'Auto', 'On']:
            return error_json_msg('不支持的运行模式。仅支持 Off, Auto, On。请核对后重新输入。')
        logger.info(f"Current mode: {mode}")
        # Request body formation
        domain = MODE_SELECT_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/{ACTION}"
        data = {
            "entity_id": MODE_SELECT_ENTITY_ID,
            "option": mode
        }
        # HTTP request
        response = requests.post(request_url, headers=CONTROL_CENTER_HEADERS, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            response_json['message'] = f"操作成功！"
            response_json['status_code'] = 200

    except requests.exceptions.RequestException as e:
        response_json['message'] = f"操作运行失败！错误内容：HTTP请求失败，原因：{str(e)}"
        response_json['status_code'] = 299
    except Exception as e:
        response_json['message'] = f"操作运行失败！错误内容: {str(e)}"
        response_json['status_code'] = 299

    logger.info(f"{response_json}")
    return response_json