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

    本MCP服务器用于控制小米智能音箱的睡眠模式，静音开关，音量调整以及一系列操作，包含以下功能：

        1. switch_xiaomi_sleep()  # 睡眠模式开关
        2. switch_xiaomi_mute()   # 扬声器静音开关
        3. switch_xiaomi_volume() # 音量调整
        4. button_xiaomi()        # 按键操作

"""


####################
# Global vairables #
####################
CONTROL_CENTER_BASE_URL = os.getenv('CONTROL_CENTER_BASE_URL')
CONTROL_CENTER_HEADERS = json.loads(os.getenv('CONTROL_CENTER_HEADERS'))
SLEEPMODE_SWITCH_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_SLEEPMODE_SWITCH_ENTITY_ID')
MUTE_SWITCH_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_MUTE_SWITCH_ENTITY_ID')
VOLUME_ADJUST_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_VOLUME_ADJUST_ENTITY_ID')
BUTTON_PLAY_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_BUTTON_PLAY_ENTITY_ID')
BUTTON_PREVIOUS_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_BUTTON_PREVIOUS_ENTITY_ID')
BUTTON_NEXT_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_BUTTON_NEXT_ENTITY_ID')
BUTTON_PAUSE_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_BUTTON_PAUSE_ENTITY_ID')
BUTTON_MUSIC_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_BUTTON_MUSIC_ENTITY_ID')
BUTTON_BROADCAST_ENTITY_ID = os.getenv('XIAOMI_SPEAKER_BUTTON_BROADCAST_ENTITY_ID')


###############
# MCP servers #
###############
@mcp.tool()
async def switch_sleep_mode(
    action: Literal["turn_on", "turn_off"] = Field(description="要执行的操作类型: 打开或者关闭。必须从两个选项中选择一个"), 
) -> str:
    """
    控制小米AI音箱睡眠模式的开关流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if action not in ['turn_on', 'turn_off']:
            return error_json_msg('不支持的开关操作类型。仅支持 turn_on, turn_off。请核对后重新输入。')
        logger.info(f"Current action: {action}")
        # Request body formation
        domain = SLEEPMODE_SWITCH_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/{action}"
        data = {
            "entity_id": SLEEPMODE_SWITCH_ENTITY_ID
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
async def mute(
    action: Literal["turn_on", "turn_off"] = Field(description="要执行的操作类型: 打开或者关闭。必须从两个选项中选择一个"), 
) -> str:
    """
    控制小米AI音箱扬声器的静音开关的流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if action not in ['turn_on', 'turn_off']:
            return error_json_msg('不支持的开关操作类型。仅支持 turn_on, turn_off。请核对后重新输入。')
        logger.info(f"Current action: {action}")
        # Request body formation
        domain = MUTE_SWITCH_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/{action}"
        data = {
            "entity_id": MUTE_SWITCH_ENTITY_ID
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
async def adjust_volume(
    volume: int = Field(ge=1, le=100, description="音箱的音量设定，从1-100之间选择一个值"), 
) -> str:
    """
    控制小米AI音箱的音量的流程。请根据用户的需求抽取参数，控制设备。
    """

    response_json = dict()

    try:

        # Sanity check
        if volume < 1 or volume > 100:
            return error_json_msg('音量值必须是 1-100 间的整数。请核对后重新输入。')
        logger.info(f"Current sound: {volume}")
        # Request body formation
        domain = VOLUME_ADJUST_ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/set_value"
        data = {
            "entity_id": VOLUME_ADJUST_ENTITY_ID,
            "value": volume
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
async def speaker_button(
    action: Literal["play", "previous", "next", "pause", "music", "broadcast"] = Field(
        description="要执行的功能类型: play 播放、previous 上一首、next 下一首、pause 暂停、music 播放音乐、broadcast 播放电台broadcast"
    ), 
) -> str:
    """
    控制小米AI音箱功能的流程。请根据用户的需求抽取功能对应的参数，控制设备。
    """

    ACTION = {
        "play": BUTTON_PLAY_ENTITY_ID,
        "previous": BUTTON_PREVIOUS_ENTITY_ID,
        "next": BUTTON_NEXT_ENTITY_ID,
        "pause": BUTTON_PAUSE_ENTITY_ID,
        "music": BUTTON_MUSIC_ENTITY_ID,
        "broadcast": BUTTON_BROADCAST_ENTITY_ID
    }

    response_json = dict()

    try:

        # Sanity check
        if action not in ["play", "previous", "next", "pause","music","broadcast"]:
            return error_json_msg('不支持的操作类型。请核对后重新输入。')
        logger.info(f"Current action: {action}")

        ENTITY_ID = ACTION[action]
        # if music_state==state:
        #     return error_json_msg('当前状态与所需状态一致，无需重复操作')
        # state=music_state
        # Request body formation
        domain = ENTITY_ID.split(".")[0]
        request_url = f"{CONTROL_CENTER_BASE_URL}/api/services/{domain}/press"
        data = {
            "entity_id": ENTITY_ID
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