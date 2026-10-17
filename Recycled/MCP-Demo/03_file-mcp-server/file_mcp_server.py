import os
from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp import FastMCP
import tools

# 1️⃣ 创建 MCP 服务器实例
mcp = FastMCP(
    "FileMCPServer",
    port=16681
)

# 2️⃣ 加载环境变量
_ = load_dotenv(find_dotenv())

# 3️⃣ 定义MCP工具
@mcp.tool()
def list_files(directory: str = ".", base_dir: str = "") -> list[str]:
    """列出指定目录下的所有文件
    
    Args:
        directory: 要列出文件的目录路径，默认为当前目录
        base_dir: 可选，基础目录，如果提供则相对于此目录查找
    """
    result = tools.list_files(directory, base_dir if base_dir else None)
    if isinstance(result, str):
        return [result]  # 错误信息转换为列表
    return result


@mcp.tool()
def read_file(filepath: str, base_dir: str = "") -> str:
    """读取指定文件的内容
    
    Args:
        filepath: 文件路径
        base_dir: 可选，基础目录，如果提供则在此目录下查找文件
    """
    return tools.read_file(filepath, base_dir if base_dir else None)


@mcp.tool()
def rename_file(old_path: str, new_name: str, base_dir: str = "") -> str:
    """重命名文件（保持在同一目录）
    
    专门用于处理用户场景：在同一目录下重命名文件
    
    Args:
        old_path: 原文件路径（可以是相对于base_dir的相对路径）
        new_name: 新的文件名（只需提供文件名，不要包含路径）
        base_dir: 可选，基础目录，如果提供则在此目录下操作
    """
    return tools.rename_file(old_path, new_name, base_dir if base_dir else None)


@mcp.tool()
def restore_original_names(directory: str = "") -> str:
    """恢复文件到原始名称
    
    Args:
        directory: 可选，只恢复此目录下的文件
    """
    return tools.restore_original_names(directory if directory else None)


@mcp.tool()
def view_rename_history(filter_dir: str = "") -> str:
    """查看重命名历史
    
    Args:
:
        filter_dir: 可选，只查看此目录下的历史记录
    """
    return tools.view_rename_history(filter_dir if filter_dir else None)


@mcp.tool()
def get_file_info(filepath: str, base_dir: str = "") -> str:
    """获取文件详细信息（大小、修改时间等）
    
    Args:
        filepath: 文件路径
        base_dir: 可选，基础目录
    """
    return tools.get_file_info(filepath, base_dir if base_dir else None)


# 4️⃣ 启动 MCP 服务器
if __name__ == "__main__":
    mcp.run(transport="streamable-http")


# 注册示例
"""
{
    "mcpServers": {
        "FileMCPServer": {
            "name": "FileMCPServer",
            "description": "支持中文城市名的天气查询",
            "url": "http://120.79.252.32:16681/mcp",
            "command": "",
            "args": [],
            "env": {},
            "isActive": true,
            "type": "streamableHttp"
        }
    }
}
"""



# 调用示例

"""
/workspace/ai-showcase/3.4大模型-Agent/02_MCP/files/   列出这个目录下所有文件，读取文件内容，根据文件内容修改文件名字，修改文件静默执行修改，不要调用TERMINAL
"""
"""
E:\test  列出这个目录下所有文件，读取文件内容，根据文件内容修改文件名字，静默执行修改
"""