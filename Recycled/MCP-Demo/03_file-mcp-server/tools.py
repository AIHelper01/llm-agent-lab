from pathlib import Path
import os
import json
import shutil
from typing import Optional, List, Union


def _silent_rename(old_path: Path, new_path: Path) -> bool:
    """静默重命名文件，确保不会调用终端"""
    try:
        # 使用最低级别的文件操作
        # 方法1: 使用 os.rename
        os.rename(str(old_path), str(new_path))
        return True
    except OSError:
        try:
            # 方法2: 如果os.rename失败，尝试shutil.move
            shutil.move(str(old_path), str(new_path))
            return True
        except Exception:
            # 方法3: 终极方案 - 复制内容后删除原文件
            try:
                with open(old_path, 'rb') as src, open(new_path, 'wb') as dst:
                    dst.write(src.read())
                os.remove(old_path)
                return True
            except Exception:
                return False


def _record_rename_history(old_path_str: str, new_path_str: str):
    """记录重命名历史"""
    try:
        history_file = Path.home() / ".file_rename_history.json"
        
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = {}
        else:
            history = {}
        
        # 使用列表记录多次重命名
        if new_path_str not in history:
            history[new_path_str] = [old_path_str]
        else:
            if old_path_str not in history[new_path_str]:
                history[new_path_str].append(old_path_str)
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # 静默失败，不记录历史


def rename_file(old_path: str, new_filename: str, base_dir: Optional[str] = None) -> str:
    """静默重命名文件，确保不调用终端
    
    Args:
        old_path: 原文件路径
        new_filename: 新文件名
        base_dir: 可选的基础目录
        
    Returns:
        操作结果（纯文本，不调用终端）
    """
    try:
        # 禁用任何可能调用终端的操作
        import warnings
        warnings.filterwarnings('ignore')
        
        # 构建路径
        if base_dir:
            old_full_path = Path(base_dir) / old_path
        else:
            old_full_path = Path(old_path)
        
        # 检查文件是否存在
        if not old_full_path.exists():
            return f"文件不存在: {old_path}"
        
        # 检查是否是文件
        if not old_full_path.is_file():
            return f"不是文件: {old_path}"
        
        # 清理新文件名
        new_filename = new_filename.strip()
        if '/' in new_filename or '\\' in new_filename:
            new_filename = Path(new_filename).name
        
        # 检查新文件名是否为空
        if not new_filename:
            return f"新文件名不能为空"
        
        # 构建新路径
        new_full_path = old_full_path.parent / new_filename
        
        # 如果新旧相同
        if old_full_path == new_full_path:
            return f"文件已经是这个名字: {old_full_path.name}"
        
        # 如果目标文件已存在
        if new_full_path.exists():
            return f"目标文件已存在: {new_filename}"
        
        # 静默重命名
        if _silent_rename(old_full_path, new_full_path):
            # 记录历史
            _record_rename_history(str(old_full_path), str(new_full_path))
            return f"✓ 重命名成功: {old_full_path.name} -> {new_filename}"
        else:
            return f"✗ 重命名失败: 未知错误"
            
    except Exception as e:
        return f"错误: {str(e)}"


def read_file(filepath: str, base_dir: Optional[str] = None) -> str:
    """静默读取文件内容"""
    try:
        if base_dir:
            full_path = Path(base_dir) / filepath
        else:
            full_path = Path(filepath)
        
        if not full_path.exists():
            return f"文件不存在: {filepath}"
        
        if not full_path.is_file():
            return f"不是文件: {filepath}"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"文件内容 ({len(content)} 字符):\n{content}"
    except UnicodeDecodeError:
        return f"无法读取文件（可能是二进制文件）: {filepath}"
    except Exception as e:
        return f"读取失败: {str(e)}"


# def list_files(directory: str = ".", base_dir: Optional[str] = None) -> Union[List[str], str]:
#     """静默列出文件"""
#     try:
#         if base_dir:
#             target_dir = Path(base_dir) / directory
#         else:
#             target_dir = Path(directory)
        
#         if not target_dir.exists():
#             return f"目录不存在: {directory}"
        
#         if not target_dir.is_dir():
#             return f"不是目录: {directory}"
        
#         files = []
#         for item in target_dir.iterdir():
#             if item.is_file():
#                 files.append(item.name)
        
#         if files:
#             return sorted(files)
#         else:
#             return "目录为空"
#     except Exception as e:
#         return f"列出文件失败: {str(e)}"
def list_files(directory: str = ".", base_dir: Optional[str] = None) -> Union[List[str], str]:
    """静默列出文件"""
    try:
        # 规范化路径，处理反斜杠
        directory = directory.replace("\\", "/")
        
        if base_dir:
            base_dir = str(base_dir).replace("\\", "/")
            target_dir = Path(base_dir) / directory
        else:
            target_dir = Path(directory)
        
        # 修复：如果是绝对路径，确保正确解析
        if ":" in str(target_dir):
            target_dir = Path(str(target_dir).replace("/", "\\"))
        
        if not target_dir.exists():
            return f"目录不存在: {target_dir}"
        
        if not target_dir.is_dir():
            return f"不是目录: {target_dir}"
        
        files = []
        for item in target_dir.iterdir():
            if item.is_file():
                files.append(item.name)
        
        if files:
            return sorted(files)
        else:
            return "目录为空"
    except Exception as e:
        return f"列出文件失败: {str(e)}"


def restore_original_names(directory: Optional[str] = None) -> str:
    """恢复文件到原始名称
    
    Args:
        directory: 可选，只恢复此目录下的文件
    """
    try:
        history_file = Path.home() / ".file_rename_history.json"
        
        if not history_file.exists():
            return "没有重命名历史记录"
        
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                return "历史记录文件损坏"
        
        restored = 0
        failed = 0
        
        for new_path_str, old_paths in history.items():
            # 如果历史记录是旧格式（字符串而不是列表）
            if isinstance(old_paths, str):
                old_paths = [old_paths]
            
            if not old_paths:
                continue
            
            new_path = Path(new_path_str)
            
            # 如果指定了目录，只处理该目录下的文件
            if directory and not str(new_path.parent).startswith(directory):
                continue
            
            # 获取最早的原始名称
            original_path = Path(old_paths[0])
            
            # 如果新文件不存在，跳过
            if not new_path.exists():
                continue
            
            # 如果原始位置已经有文件，跳过
            if original_path.exists():
                failed += 1
                continue
            
            # 恢复文件
            if _silent_rename(new_path, original_path):
                # 从历史记录中移除
                del history[new_path_str]
                restored += 1
            else:
                failed += 1
        
        # 保存更新后的历史记录
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        if restored == 0 and failed == 0:
            return "没有需要恢复的文件"
        
        return f"恢复完成: {restored} 个文件已恢复，{failed} 个文件恢复失败"
    
    except Exception as e:
        return f"恢复失败: {str(e)}"


def view_rename_history(filter_dir: Optional[str] = None) -> str:
    """查看重命名历史
    
    Args:
        filter_dir: 可选，只查看此目录下的历史记录
    """
    try:
        history_file = Path.home() / ".file_rename_history.json"
        
        if not history_file.exists():
            return "没有重命名历史记录"
        
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                return "历史记录文件损坏"
        
        if not history:
            return "重命名历史为空"
        
        result = []
        for new_path_str, old_paths in history.items():
            new_path = Path(new_path_str)
            
            # 如果指定了目录，只显示该目录下的历史
            if filter_dir and not str(new_path.parent).startswith(filter_dir):
                continue
            
            if isinstance(old_paths, str):
                # 旧格式：单个字符串
                result.append(f"{old_paths} -> {new_path_str}")
            elif isinstance(old_paths, list) and old_paths:
                # 新格式：列表
                result.append(f"{old_paths[0]} -> {new_path_str}")
                if len(old_paths) > 1:
                    for i, old_path in enumerate(old_paths[1:], 1):
                        result.append(f"  (之前: {old_path})")
            result.append("")  # 空行分隔
        
        if not result:
            return f"在目录 {filter_dir} 中没有找到历史记录"
        
        return "重命名历史:\n" + "\n".join(result)
    
    except Exception as e:
        return f"查看历史失败: {str(e)}"


def get_file_info(filepath: str, base_dir: Optional[str] = None) -> str:
    """获取文件信息（大小、修改时间等）"""
    try:
        if base_dir:
            full_path = Path(base_dir) / filepath
        else:
            full_path = Path(filepath)
        
        if not full_path.exists():
            return f"文件不存在: {filepath}"
        
        stats = full_path.stat()
        size_kb = stats.st_size / 1024
        from datetime import datetime
        mtime = datetime.fromtimestamp(stats.st_mtime)
        
        info = [
            f"文件: {full_path.name}",
            f"路径: {full_path}",
            f"大小: {stats.st_size} 字节 ({size_kb:.2f} KB)",
            f"修改时间: {mtime}",
            f"创建时间: {datetime.fromtimestamp(stats.st_ctime)}",
            f"访问时间: {datetime.fromtimestamp(stats.st_atime)}",
        ]
        
        return "\n".join(info)
    except Exception as e:
        return f"获取文件信息失败: {str(e)}"