# FAQ

**Q: 不接 LLM 能跑吗？**
A: 能。核心引擎零依赖，`MockLLM` + 空工具集即可端到端闭环，适合 CI 与单测。

**Q: 如何接本地 vLLM / Atria？**
A: 用 `LLMRegistry.build({"provider": "openai-compat", "base_url": "...", "model": "..."})`。

**Q: 证据 verified 是什么意思？**
A: 证据经过验证器校验（如退出码为 0、哈希匹配），标记为可信，避免「伪造成功」。

**Q: 如何扩展工具/验证器？**
A: 继承 `Tool` / `Verifier`，在对应 registry 注册即可，见 docs/tools.md、docs/verifiers.md。
