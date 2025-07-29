# Jenius MCP Smart Device

A smart home control tool supported by **Jenius**.

[Jenius](https://www.jenius.cn/) is a **universal multi-agent AI system** independently developed by **Tianju Dihe (Suzhou) Technology Co., Ltd.**. By deeply integrating multi-agent collaboration architecture with real-time data services, Jenius aims to realize a full closed-loop process from *intention recognition* to *precise execution*. Its unique "**Data + Agent + RPA**" triangular engine, empowered by massive data resources from its aggregation platform and proprietary RPA technologies, is designed to meet the deep service needs of complex scenarios — particularly excelling in vertical fields such as travel itinerary planning, marketing content generation, and report analysis.

# Project Structure

```bash
.
├── README.md                # Project documentation
├── Home Assistant Guide.md  # Guide for setting up Home Assistant
├── jenius_mcp.py            # Main entry point of the MCP server
├── tools/                   # MCP toolkit
│   ├── __init__.py          # MCP toolkit initialization
│   ├── common.py            # Common utility functions
│   └── mcp/                 # MCP core implementation
├── utils/                   # Utility functions
├── img/                     # Project images
├── .mcp.env                 # MCP environment configuration
├── Dockerfile               # Docker build configuration
├── mcp_server.tpl           # MCP server template
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependency requirements
└── uv.lock                  # UV dependency lock file
```

# Usage Guide

## Set Up the Home Assistant Control Center

We recommend using **Home Assistant** as a bridge between the MCP server and smart home devices. By integrating your smart devices into Home Assistant and configuring the control center URL and API keys, you can enable remote control of devices via the MCP server.

Refer to the setup instructions in:
[Home Assistant Setup Guide](Home%20Assistant%20Guide.md)

## Environment Configuration

MCP Server Configuration:

```bash
# MCP host address (supports Arguments input)
JENIUS_SMART_DEVICE_MCP_HOST = 127.0.0.1

# Jenius MCP transport protocol configuration (supports Arguments input)
JENIUS_SMART_DEVICE_MCP_TRANSPORT = stdio

# If using SSE protocol, configure the following:
JENIUS_SMART_DEVICE_MCP_SSE_PORT = YOUR_SSE_PORT
JENIUS_SMART_DEVICE_MCP_SSE_PATH = "/sse"
JENIUS_SMART_DEVICE_MCP_MESSAGE_PATH = "/messages/"
```

**Home Assistant** Control Center Configuration:

```bash
# Base URL of the control center
CONTROL_CENTER_BASE_URL = YOUR_HOME_ASSISTANT_BASE_URL

# Request headers for the control center, with your own API key
CONTROL_CENTER__HEADERS = {"Authorization": YOUR_HOME_ASSISTANT_API_KEY, "Content-Type": "application/json"}
```

Smart Device Configuration:

```bash
# Mi Air Purifier control
XIAOMI_AIR_PURIFIER_SWITCH_ENTITY_ID = "switch.zhimi_cn_495307311_rma1_on_p_2_1"
XIAOMI_AIR_PURIFIER_MODE_SELECT_ENTITY_ID = "select.zhimi_cn_495307311_rma1_mode_p_2_4"

# Mi Smart Speaker control
XIAOMI_SPEAKER_SLEEPMODE_SWITCH_ENTITY_ID = "switch.xiaomi_cn_58102534_s12_sleep_mode_p_5_3"
XIAOMI_SPEAKER_MUTE_SWITCH_ENTITY_ID = "switch.xiaomi_cn_58102534_s12_mute_p_2_2"

# Mi Roborock T7 Robot Vacuum
...

# Xiaomi smart camera
...
```

You can obtain the values for `YOUR_HOME_ASSISTANT_BASE_URL` and `YOUR_HOME_ASSISTANT_API_KEY` from **Sections 3 and 4** of the [Home Assistant Setup Guide](Home%20Assistant%20Guide.md).

## Installing UV

`uv` is a Python environment management tool recommended by the MCP project. Installation instructions can be found at:

> [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

## Start the MCP Server

If dependencies are not yet installed, sync by running the following command from the project root:

```bash
uv sync
```

To start the server using the default STDIO protocol:

```bash
uv run jenius_mcp.py
```

You may also specify startup parameters, for example:

```bash
uv run jenius_mcp.py --host 0.0.0.0 --port 8981 --transport sse
```

## Client Configuration

You can configure MCP server connections using clients like `Cline` or `Claude Desktop`. Example configurations:

```yaml
# STDIO mode
"juhe-mcp-smart_device": { 
    "command": "uv",
    "args": [
        "run",
        "jenius_mcp.py"
    ]
}

# SSE mode
"smart_home_server": {
    "url": "http://0.0.0.0:8981/sse",
    "transport": "sse"
}
```

# Supported Devices

* Mi Air Purifier 4 Lite
* Mi AI Speaker
* Mi Roborock T7 Robot Vacuum
* Xiaomi Smart Camera

All devices from **Mi** or **Xiaomi** can be integrated simply by replacing the *entity IDs* in the environment configuration file. Refer to **Section 4** of the [Home Assistant Setup Guide](Home%20Assistant%20Guide.md) for instructions on obtaining these IDs.

* Smart Socket: SmartHW MF287

For **Smart Sockets**, refer to your device’s user manual for setup. Since smart sockets have unique IP addresses and ports, you can add these details to the environment configuration file. You may also want to adjust prompt content and function naming in the MCP server to better match the type of appliance being controlled, helping the LLM (Large Language Model) understand and behave accordingly.

# License

This project is licensed under the [Apache License 2.0](LICENSE).
