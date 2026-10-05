# Lotus Stay — mốc 1
Django + PostgreSQL + pgAdmin + Nginx.
Chạy: python3 scripts/setup.py; docker compose up -d --build.
Website http://localhost:8080, pgAdmin http://localhost:5050. Secret nằm trong .env, không commit.

Mốc 2: Prometheus :9090, Grafana :3000, cAdvisor, Nginx exporter và PostgreSQL exporter. Dashboard tự nạp từ monitoring/.
