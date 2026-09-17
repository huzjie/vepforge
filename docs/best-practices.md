# 最佳实践

1. **验收标准要可判定**：acceptance_criteria 尽量写成「产物已生成 / 退出码 0」等可验证判据；
2. **工具要真实执行**：绑定 PythonExecTool / ShellTool / DockerRuntime，别用 mock 结果冒充；
3. **证据先验证后入库**：所有工具输出走 Verifier；
4. **凭证走环境变量**：禁止硬编码 API key；
5. **生产用 Docker 沙箱**：隔离代码执行，限制网络与文件权限。
