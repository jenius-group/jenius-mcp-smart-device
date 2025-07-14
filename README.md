# Jenius MCP Smart Device

Jenius 支持的智能家居控制工具

[Jenius](https://www.jenius.cn/) 是由 **天聚地合（苏州）科技股份有限公司** 自主研发的 **通用多智能体 AI Agent**，通过深度融合多智能体协作架构与实时数据服务能力，致力于实现从 “需求理解” 到 “精准执行” 的全链路闭环。Jenius 独创 “**数据+智能体+RPA**” 三角引擎，依托天聚地合旗下聚合数据平台的海量资源与自研RPA技术，专注于解决复杂场景的深度服务需求，尤其在旅游行程规划、营销活动生成、报表分析等垂直领域展现惊艳的执行力。

# 项目结构

```bash
.
├── README.md                # 项目说明文档
├── Home Assistant Guide.md  # 小米 Home Assistant 搭建指南
├── jenius_mcp.py            # MCP服务主入口
├── tools/                   # MCP工具集
│   ├── __init__.py
│   ├── common.py            # 通用工具函数
│   └── mcp/                 # MCP具体实现
├── utils/                   # 工具函数
├── img/                     # 项目图片
├── .mcp.env                 # MCP环境配置
├── mcp_server.tpl           # MCP服务器模板
├── pyproject.toml           # Python项目配置
└── uv.lock                  # UV依赖锁定文件
```

# 使用流程

## 搭建 Home Assistant 控制中心

 我们建议使用 Home Assistant 作为连接MCP服务器和智能家居终端的桥梁。通过把智能家居设备接入 Home Assistant，并配置智能家居控制中心 URL 和密钥，即可快速实现 MCP 服务器对智能家居设备的远程控制。具体操作请参考以下文档
 
 [Home Assistant 搭建指南](Home%20Assistant%20Guide.md)

## 配置环境

MCP 服务器环境配置：
```bash
# SERVER HOST (支持Arg参数传递)
JENIUS_SMART_DEVICE_MCP_HOST = 127.0.0.1

# Jenius MCP TRANSPORT协议配置（支持Arg参数传递）
JENIUS_SMART_DEVICE_MCP_TRANSPORT = stdio

# 如果使用SSE方式，则配置下面这些
JENIUS_SMART_DEVICE_MCP_SSE_PORT = 8981
JENIUS_SMART_DEVICE_MCP_SSE_PATH = "/sse"
JENIUS_SMART_DEVICE_MCP_MESSAGE_PATH = "/messages/"
```
Home Assistant 控制中心环境配置：
```bash
# 智能家居控制中心URL配置
CONTROL_CENTER_BASE_URL = YOUR_HOME_ASSISTANT_BASE_URL

# 智能家居控制中心请求头配置，需要填入账户相对应的密钥
CONTROL_CENTER__HEADERS = {"Authorization": YOUR_HOME_ASSISTANT_API_KEY, "Content-Type": "application/json"}
```
智能终端环境配置：
```bash
# 小米空气净化器控制
XIAOMI_AIR_PURIFIER_SWITCH_ENTITY_ID = "switch.zhimi_cn_495307311_rma1_on_p_2_1"
XIAOMI_AIR_PURIFIER_MODE_SELECT_ENTITY_ID = "select.zhimi_cn_495307311_rma1_mode_p_2_4"
...

# 小米智能音箱控制
XIAOMI_SPEAKER_SLEEPMODE_SWITCH_ENTITY_ID = "switch.xiaomi_cn_58102534_s12_sleep_mode_p_5_3"
XIAOMI_SPEAKER_MUTE_SWITCH_ENTITY_ID = "switch.xiaomi_cn_58102534_s12_mute_p_2_2"
...
```
控制中心的URL `YOUR_HOME_ASSISTANT_BASE_URL` 和密钥 `YOUR_HOME_ASSISTANT_API_KEY` 可以参考 [Home Assistant 搭建指南](Home%20Assistant%20Guide.md) 的 **第三** 和 **第四** 部分获取。


## 安装UV
`uv`是一个 Python 环境管理工具，是 MCP 官方推荐的 Python 项目管理工具，安装方式见 
> https://docs.astral.sh/uv/getting-started/installation/

## 启动MCP服务器

如果没有安装依赖包，可进入项目根目录执行命令进行同步。

```sh
uv sync
```

STDIO协议启动（默认）：

```sh
uv run jenius_mcp.py
```
可自由配置启动参数，例如：
```sh
uv run jenius_mcp.py --host 0.0.0.0 --port 8981 --transport sse
```

## 客户端配置
可以使用例如 `Cline`, `Claude Desktop` 等客户端方便地进行 MCP 服务器配置，配置案例如下：
```yaml
# STDIO 模式
"juhe-mcp-smart_device": { 
    "command": "uv",
    "args": [
        "run",
        "jenius_mcp.py"
    ]
}

# SSE 模式
"smart_home_server": {
    "url": "http://127.0.0.1:8981/sse",
    "transport": "sse"
}
```

# 已支持的终端

- 米家空气净化器4 Lite
- 小米AI音箱

**米家空气净化器4 Lite** 和 **小米AI音箱** 可通过在环境配置文件中简单替换您的设备实体标识符进行快速接入。设备实体标识符的获取请参考 [Home Assistant 搭建指南](Home%20Assistant%20Guide.md) 的 **第四** 部分。

- 智能插座 SmartHW MF287

**智能插座** 的配置可参考您设备的使用说明书。智能插座有其独立的IP地址和端口，可通过在环境配置文件中添加您的设备IP、端口等信息进行接入，同时根据您插座连接的家具类型修改MCP服务器的提示词内容和函数命名规则，以便大模型更好地理解并调用。