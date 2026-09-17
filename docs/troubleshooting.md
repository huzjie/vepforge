# 故障排查

| 现象 | 原因 | 解法 |
|---|---|---|
| smoke 返回 failed | 阶段枚举值不匹配 | 确认 TaskStatus 含 analyze/code/execute/reflect |
| evidence 不 verified | 验证器未注册 | 检查 VerifierRegistry |
| 工具报 command not allowed | 超出 allowlist | 调整 SandboxPolicy / ShellTool allowlist |
| LLM 调用超时 | base_url 不可达 | 检查 vLLM 服务 / 降级 MockLLM |
| 模型卡加载 0 张 | 缺 PyYAML | `pip install PyYAML` |
