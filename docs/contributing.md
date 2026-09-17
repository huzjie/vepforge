# 贡献指南

1. Fork 并 clone；
2. `pip install -e .` 后运行 `vepforge doctor` 确认基线通过；
3. 新增验证器继承 `Verifier`，新增工具继承 `Tool`，并在对应 registry 注册；
4. 提交前 `python -m compileall vepforge` 零错。

欢迎提交 PR。
