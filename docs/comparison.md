# 与同类框架对比

| 维度 | vepforge | 通用 Agent 框架 | 传统脚本编排 |
|---|---|---|---|
| 证据可验证 | 一等公民（Evidence + Verifier） | 弱 | 无 |
| 轨迹可回放 | Trajectory 逐步记录 | 部分 | 无 |
| 产物可寻址 | sha256 | 无 | 无 |
| 长程闭环 | analyze→code→execute→reflect | 部分 | 无 |
| 零依赖核心 | 是 | 否 | 是 |

vepforge 的差异化：**把「可信执行」做成基础设施**，而非事后审计。
