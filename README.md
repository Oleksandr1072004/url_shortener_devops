## Розгортання в Kubernetes (Lab 3)

### Передумови
- minikube ≥ 1.30
- kubectl
- Docker Desktop

### Запуск кластера
```bash
minikube start --driver=docker --cpus=2 --memory=4g
minikube addons enable ingress
minikube addons enable metrics-server
```

### Збірка образів всередині minikube
```bash
minikube docker-env | Invoke-Expression   # PowerShell
docker build -t api-gateway:1.0.0 ./api-gateway
docker build -t api-gateway:1.1.0 ./api-gateway
```

### Розгортання
```bash
kubectl apply -f k8s/
kubectl get pods -n url-shortener
```

### Параметри ConfigMap

| Ключ | Опис | Значення |
|------|------|----------|
| `BASE_URL` | Базовий URL застосунку | `http://url-shortener.local` |
| `CODE_LENGTH` | Довжина короткого коду | `6` |

### Параметри Secret

| Ключ | Опис |
|------|------|
| `DATABASE_URL` | Рядок підключення до PostgreSQL (base64) |

> **Увага:** реальні паролі в Secret не зберігаються — лише тестові значення.

### Доступ до застосунку
```bash
minikube service api-gateway-service -n url-shortener --url
# або через Ingress
echo "$(minikube ip) url-shortener.local" | sudo tee -a /etc/hosts
```
