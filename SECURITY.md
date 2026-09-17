# Security Policy

## 沙箱隔离

代码执行默认走子进程（`LocalRuntime`）或 Docker（`DockerRuntime`）。
生产环境请使用 Docker 沙箱，并限制网络与文件系统权限。

## 凭证

LLM API key 通过环境变量注入，**禁止硬编码**。见 `.env.example`。

## 报告漏洞

请通过 GitHub Security Advisory 报告，勿公开披露。
