# 架构设计

## 总览

```
                    ┌─────────────────────────────────────────┐
                    │        VerifiableExperiencePipeline      │
                    │                                          │
  Task ──────────▶  │  analyze ──▶ code ──▶ execute ──▶ reflect│
                    │     │            │         │          │   │
                    │     ▼            ▼         ▼          ▼   │
                    │  Thought     Artifact   Evidence   Verdict │
                    └─────────────────────────────────────────┘
                              │                │
                              ▼                ▼
                         Trajectory          Verifiers
                          (回放)          (exit_code/hash/http)
```

## 分层

| 层 | 模块 | 职责 |
|---|---|---|
| 实体层 | `vepforge.core` | Task / Trajectory / Artifact / Evidence / Experience |
| 流水线层 | `vepforge.pipeline` | VEP 主引擎、四阶段、Linker |
| 验证层 | `vepforge.verifier` | 证据验证器（退出码/哈希/HTTP） |
| 智能体层 | `vepforge.agents` | 分析/编码/执行/复盘 + 编排 + 恢复 |
| 工具层 | `vepforge.tools` | shell/python/http/file/search |
| 运行时层 | `vepforge.runtime` | 本地沙箱 / Docker 沙箱 |
| 记忆层 | `vepforge.memory` | 经验持久化 + 向量检索 |
| 模型层 | `vepforge.llm` + `catalog` | LLM 后端适配 + 模型卡 |
| 服务层 | `vepforge.serving` | FastAPI + OpenAI/Anthropic 兼容 |
| 评测层 | `vepforge.benchmarks` | 五类智能体基准 |

## 关键设计决策

1. **四实体连接**：`Experience` 聚合 `Task + Trajectory + Artifacts + Evidences`，
   用 `Linker` 维护步骤 → 产物/证据的映射，实现可追溯。
2. **证据先验证后入库**：工具执行结果先经 `Verifier` 校验，标记 `verified` 再进入
   Experience，杜绝「伪造成功」。
3. **零依赖核心**：核心引擎不依赖 LLM/网络，`MockLLM` + 空工具集即可端到端跑通，
   便于单测与 CI。
4. **兼容多后端**：`OpenAICompatLLM` / `AnthropicCompatLLM` 直连本地 vLLM/Atria API，
   无需改业务代码。
