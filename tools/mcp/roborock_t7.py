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

    本MCP服务器用于控制 Roborock T7 扫地机器人的充电，模式切换和启动、停止、定位，包含以下三个功能：

        1. start_charge_roborock_t7() # 开始充电
        2. switch_mode_roborock_t7()  # 模式切换
        3. control_roborock_t7()      # 启动、停止、定位

"""


####################
# Global vairables #
####################
CONTROL_CENTER_BASE_URL = os.getenv('CONTROL_CENTER_BASE_URL')
CONTROL_CENTER_HEADERS = json.loads(os.getenv('CONTROL_CENTER_HEADERS'))
START_CHARGE_ENTITY_ID = os.getenv('ROBOROCK_T7_START_CHARGE_ENTITY_ID')
MODE_SELECT_ENTITY_ID = os.getenv('ROBOROCK_T7_MODE_SELECT_ENTITY_ID')
CONTROL_ENTITY_ID = os.getenv('ROBOROCK_T7_CONTROL_ENTITY_ID')


###############
# MCP servers #
###############
@mcp.tool()
async def start_charge_roborock_t7() -> str:
    """
    Roborock T7 扫地机器人开始充电的触发按钮，启动后扫地机器人会归位并开始充电。
    """

    response_json = dict()

    try:

        domain = START_CHARGE_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/press"
        data = {
            "entity_id": START_CHARGE_ENTITY_ID
        }
        #HTTP request
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
async def switch_mode_roborock_t7(
    mode: Literal["安静", "标准", "强力", "全速"] = Field(description="扫地机器人的运行模式，从四个模式:安静、标准、强力、全速当中选择一个")
)-> str:
    """
    控制 Roborock T7 扫地机器人的运行模式的流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if mode not in ['安静', '标准', '强力', '全速']:
            return error_json_msg('不支持的运行模式。仅支持 安静, 标准，强力, 全速。请核对后重新输入。')
        logger.info(f"Current mode: {mode}")
        # Request body formation
        domain = MODE_SELECT_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/select_option"
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


@mcp.tool()
async def control_roborock_t7(
    action: Literal["start", "stop", "locate"] = Field(description="控制 Roborock T7 扫地机器人的指令, 从开始start，停止stop，定位locate当中选择一个")
) -> str:
    """
    控制 Roborock T7 扫地机器人的流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if action not in ['start', 'stop', 'locate']:
            return error_json_msg('不支持的运行模式。仅支持 开始, 停止, 定位。请核对后重新输入。')
        logger.info(f"Current action: {action}")
        # Request
        domain = CONTROL_ENTITY_ID.split(".")[0]
        requests_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/{action}"
        data = {
            "entity_id": CONTROL_ENTITY_ID
        }
        # HTTP request
        response = requests.post(requests_url, headers=CONTROL_CENTER_HEADERS, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            response_json['message'] = f"操作成功!"
            response_json['status_code'] = 200

    except requests.exceptions.RequestException as e:
        response_json['message'] = f"操作运行失败！错误内容：HTTP请求失败"
        response_json['status_code'] = 299
    except Exception as e:
        response_json['message'] = f"操作运行失败！错误内容: {str(e)}"
        response_json['status_code'] = 299

    logger.info(f"{response_json}")
    return response_json