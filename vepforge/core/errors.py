# -*- coding: utf-8 -*-
"""vepforge 自定义异常体系。"""


class VepforgeError(Exception):
    """基础异常。"""


class TaskError(VepforgeError):
    """任务定义/执行错误。"""


class VerificationError(VepforgeError):
    """验证失败。"""


class ToolExecutionError(VepforgeError):
    """工具执行失败（带退出码与 stderr）。"""

    def __init__(self, message: str, exit_code: int = -1, stderr: str = ""):
        super().__init__(message)
        self.exit_code = exit_code
        self.stderr = stderr


class ModelUnavailableError(VepforgeError):
    """LLM 后端不可用。"""


class RegistryError(VepforgeError):
    """注册表错误（重复注册/未注册）。"""


class SandboxError(VepforgeError):
    """沙箱运行时错误。"""
