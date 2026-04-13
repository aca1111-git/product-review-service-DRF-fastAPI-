#!/bin/bash
# product-review-service K8s 배포 스크립트

set -e

echo "=== 1. Docker 이미지 빌드 ==="
eval $(minikube docker-env)
docker build -t product-review-backend:latest ./backend
docker build -t product-review-ai:latest -f ./ai-server/Dockerfile.deploy ./ai-server

echo "=== 2. K8s 리소스 적용 ==="
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/redis.yaml
kubectl apply -f kubernetes/django.yaml
kubectl apply -f kubernetes/celery.yaml
kubectl apply -f kubernetes/fastapi.yaml
kubectl apply -f kubernetes/nginx.yaml
kubectl apply -f kubernetes/prometheus.yaml
kubectl apply -f kubernetes/grafana.yaml
kubectl apply -f kubernetes/alertmanager.yaml

echo "=== 3. 상태 확인 ==="
kubectl get all -n product-review

echo "=== 4. 접속 주소 ==="
echo "Django (Nginx):  http://$(minikube ip):30080"
echo "Grafana:         http://$(minikube ip):30300"
