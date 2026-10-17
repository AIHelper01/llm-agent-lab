import json
import time
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("TimeServer")


# 使用装饰器定义获取当前时间的工具函数
@mcp.tool()
def get_current_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {"current_time": current_time}


# 运行 MCP 服务器,stdio方式运行
if __name__ == "__main__":
    # stdio方式运行
    mcp.run(transport="stdio")


# 在cline里注册,注意检查路径是否与实际路径相符
"""
{
  "mcpServers": {
    "TimeServer": {
      "command": "/opt/miniconda3/envs/env_agent/bin/python",
      "args": [
        "/workspace/learn-llm-agent-easily/03_MCP实操/02_file-agent-mcp/time_agent_mcp_server.py"
      ],
      "autoApprove": [
        "get_current_time"
      ],
      "disabled": false
    }
  }
}
"""


# # 运行 MCP 服务器,sse方式运行
# if __name__ == "__main__":
#     # sse方式运行
#     mcp.run(transport="sse")

# # 在cline里注册,注意baseUrl是否与实际相符
# # 这种方式在cheery studio可以,在 cline 等客户端不支持
# """
# {
#   "mcpServers": {
#     "TimeServer": {
#       "name": "TimeServer",
#       "description": "",
#       "baseUrl": "http://127.0.0.1:8000/sse",
#       "command": "",
#       "args": [],
#       "env": {},
#       "isActive": true,
#       "type": "sse"
#     }
#   }
# }
# """

# # 运行 MCP 服务器,streamable-http方式运行
# if __name__ == "__main__":
#     # streamable-http方式运行
#     mcp.run(transport="streamable-http")

# # 在cline里注册,注意url是否与实际相符
# """
# {
#   "mcpServers": {
#     "TimeServer": {
#       "name": "TimeServer",
#       "description": "",
#       "url": "http://127.0.0.1:8000/mcp",
#       "command": "",
#       "args": [],
#       "env": {},
#       "isActive": true,
#       "type": "streamableHttp"
#     }
#   }
# }
# """
