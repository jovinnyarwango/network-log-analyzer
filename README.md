# Network Log Analyzer

Python tool that parses raw network logs, isolates ERROR-level events,
identifies high-frequency error-generating IPs, and exports a CSV
report. Containerized with Docker and deployed to AWS ECS Fargate
through a GitHub Actions CI/CD pipeline.

## What it does

- Parses timestamped logs (INFO / WARNING / ERROR) with regex
- Extracts source IPs from error messages and ranks top offenders
- Prints a summary and exports detailed errors to CSV
- Pure Python standard library — no dependencies

## Run locally

    python log_analyzer.py [input.log] [report.csv]

Arguments are optional; defaults are `network_traffic.log` and
`critical_errors_report.csv`.

## Run with Docker

    docker build -t log-analyzer .
    docker run --rm -v "$(pwd):/data" log-analyzer \
      /data/network_traffic.log /data/report.csv

The image contains code only; input data is mounted at runtime, so
the same image runs against any log file.

## Cloud deployment (AWS)

- **ECR** — images are stored in a private registry
- **ECS Fargate** — the task definition in `task-definition.json`
  runs the analyzer serverlessly (0.25 vCPU / 512MB, awslogs driver)
- **CloudWatch Logs** — container output streams to
  `/ecs/log-analyzer`

## CI/CD

Every push to `main` triggers `.github/workflows/deploy.yml`, which
builds the image on GitHub-hosted runners and pushes it to ECR with
two tags: `latest` and the commit SHA (for traceable rollbacks).
Authentication uses a dedicated least-privilege IAM user via
encrypted repository secrets.

## Roadmap

- Pull input logs from S3 via a task role instead of baking the
  sample log into the image
- Scheduled runs via EventBridge
