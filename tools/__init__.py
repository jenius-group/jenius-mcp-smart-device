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
Jenius Smart Device 工具包

该模块包含了扩展工具包的通用功能：
- MCP服务初始化
- 智能插座控制
- 米家智能扫地机器人控制
- 米家空气净化器控制
- 米家智能音箱控制
- 米家智能摄像头控制
"""


from tools.common import mcp
from tools.mcp import fan 
from tools.mcp import roborock_t7 
from tools.mcp import xiaomi_air_purifier 
from tools.mcp import xiaomi_speaker 
from tools.mcp import xiaomi_surveillance 


__all__ = [
    'mcp',
    'fan',
    'roborock_t7',
    'xiaomi_air_purifier',
    'xiaomi_speaker',
    'xiaomi_surveillance',
]