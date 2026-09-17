# 部署

## Docker

```bash
docker build -t vepforge .
docker run -p 8000:8000 vepforge
```

## Kubernetes

```bash
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
```

## 生产建议

- 接真实 LLM：设置 `LLM_PROVIDER` / `LLM_BASE_URL` / `LLM_MODEL` / `LLM_API_KEY`；
- 用 Docker 沙箱隔离代码执行（`vepforge.runtime.DockerRuntime`）；
- 经验落库用 SQLite 后端（`MemoryStore(use_sqlite=True)`）。
