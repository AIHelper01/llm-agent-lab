# -------------------------------
# 工具函数：查询天气（使用OpenWeather API）
# -------------------------------

import json
import os
import requests
from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp import FastMCP

# 加载环境变量
_ = load_dotenv(find_dotenv())

# 创建 MCP 服务器实例
mcp = FastMCP("WeatherMCPServer",port="16681")

@mcp.tool()
def get_weather(location: str):
    """
    查询指定城市实时天气，根据输入的城市名称，查询对应城市的实时天气，返回结果将遵循固定的JSON格式，包含城市、温度、天气状况、湿度、风速和更新时间等字段。
    中国城市名称需用英文，如 Beijing。
    """
    open_weather_key = os.environ["API_KEY_OPENWEATHER"]
    open_weather_url = os.environ["BASE_URL_OPENWEATHER"]

    params = {
        "q": location,
        "appid": open_weather_key,
        "units": "metric",
        "lang": "zh_cn"
    }

    response = requests.get(open_weather_url, params=params)
    data = response.json()

    # 直接返回 JSON（MCP 会自动序列化)
    return data


# -------------------------------
# 启动 MCP Server
# -------------------------------
if __name__ == "__main__":
    # 支持 streamable-http（Claude Desktop、浏览器触发）模式
    mcp.run(transport="streamable-http")


# 在cline里注册
"""
{
    "mcpServers": {
        "WeatherMCPServer": {
            "name": "WeatherMCPServer",
            "description": "支持中文城市名的天气查询",
            "url": "http://8.159.144.108:16681/mcp",
            "command": "",
            "args": [],
            "env": {},
            "isActive": true,
            "type": "streamableHttp"
        }
    }
}
"""



# # -------------------------------
# # 和风天气开发服务：https://dev.qweather.com/
# # -------------------------------

# import signal
# import sys
# import json
# import os
# import requests
# from dotenv import load_dotenv, find_dotenv
# from mcp.server.fastmcp import FastMCP

# # 加载环境变量
# _ = load_dotenv(find_dotenv())

# # 创建 MCP 服务器实例
# mcp = FastMCP("WeatherServer", port="19981")

# # 工具函数：查询天气（使用和风天气API）
# @mcp.tool()
# def get_weather(location: str):
#     """
#     查询指定城市实时天气，支持中文城市名（如北京、上海）和英文城市名。
#     返回结果包含城市、温度、天气状况、湿度、风速和更新时间等字段。
#     """
#     hefeng_key = os.environ["HEFENG_API_KEY"]
    
#     # 第一步：获取城市LocationID
#     city_search_url = f"https://geoapi.qweather.com/v2/city/lookup?location={location}&key={hefeng_key}"
    
#     try:
#         # 获取城市信息
#         city_response = requests.get(city_search_url)
#         city_data = city_response.json()
        
#         if city_data.get("code") != "200":
#             return {"error": f"找不到城市: {location}", "details": city_data}
        
#         location_id = city_data["location"][0]["id"]
#         city_name = city_data["location"][0]["name"]
        
#         # 第二步：查询实时天气
#         weather_url = f"https://devapi.qweather.com/v7/weather/now?location={location_id}&key={hefeng_key}"
#         weather_response = requests.get(weather_url)
#         weather_data = weather_response.json()
        
#         if weather_data.get("code") != "200":
#             return {"error": "获取天气数据失败", "details": weather_data}
        
#         # 格式化返回数据
#         result = {
#             "city": city_name,
#             "temperature": weather_data["now"]["temp"],
#             "weather": weather_data["now"]["text"],
#             "humidity": weather_data["now"]["humidity"],
#             "windSpeed": weather_data["now"]["windSpeed"],
#             "windDir": weather_data["now"]["windDir"],
#             "updateTime": weather_data["updateTime"]
#         }
        
#         return result
        
#     except Exception as e:
#         return {"error": str(e)}

# # 信号处理函数
# def signal_handler(sig, frame):
#     print("\n收到停止信号，正在优雅退出...")
#     if hasattr(mcp, 'shutdown'):
#         mcp.shutdown()
#     sys.exit(0)


# # 启动 MCP Server
# if __name__ == "__main__":
#     # 注册信号处理器
#     signal.signal(signal.SIGINT, signal_handler)
    
#     try:
#         # 支持 streamable-http 模式
#         mcp.run(transport="streamable-http")
#     except KeyboardInterrupt:
#         print("\n程序被用户中断")
#     finally:
#         print("服务器已停止")
        
