# 验证器

| 验证器 | 模块 | 证据类型 | 通过条件 |
|---|---|---|---|
| ExitCodeVerifier | `verifier/exit_code.py` | exit_code | `== 0` |
| HashVerifier | `verifier/hash.py` | hash | 64 位 hex / 匹配 expected |
| HttpStatusVerifier | `verifier/http.py` | http_status | `2xx` |
| SchemaVerifier | `verifier/schema.py` | file | 合法 JSON 结构 |
| TestResultVerifier | `verifier/test_result.py` | test_result | `failed == 0` |
| NonEmptyVerifier | `verifier/nonempty.py` | stdout | 非空 |

## 自定义验证器

```python
from vepforge.verifier import Verifier
from vepforge.core.evidence import Evidence

class MyVerifier(Verifier):
    name = "my"
    def verify(self, evidence: Evidence) -> Evidence:
        evidence.verified = True
        return evidence
```
