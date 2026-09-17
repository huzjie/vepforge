# 核心概念

## 可验证经验流水线（VEP）

一句话：**不让智能体「声称」做了什么，而要它「证明」做了什么。**

- 每个动作都进入 `Trajectory`（可回放）；
- 每次工具真实执行都产生 `Evidence`（退出码/哈希/状态码）；
- 每个产物都有 `sha256`（可寻址、防篡改）；
- 复盘阶段对照 `acceptance_criteria` 打分。

## 四大实体

### Task

`goal`（目标）+ `constraints`（约束）+ `acceptance_criteria`（验收标准）。

### Trajectory

步骤序列，角色含 `thought/action/observation/artifact/evidence/reflection/error`。

### Artifact

`name + kind + content + sha256`，内容可寻址。

### Evidence

`kind + value + tool + verified`，`verified=True` 表示已被验证器校验通过。

## 验证器

| 验证器 | 证据类型 | 通过条件 |
|---|---|---|
| ExitCodeVerifier | exit_code | `== 0` |
| HashVerifier | hash | 与 expected 一致 / 64 位 hex |
| HttpStatusVerifier | http_status | `2xx` |
