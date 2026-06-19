# STORIES.md

## Guardrail – API Resilience & Abuse Prevention Platform

**Goal** – Deliver a cloud‑agnostic, API‑first platform that automatically detects abuse patterns, enforces rate limits, and protects downstream services from denial‑of‑service or data exfiltration attacks.  
**MVP** – Core detection, mitigation, and reporting pipeline that works out‑of‑the‑box on any cloud provider (AWS, GCP, Azure, or on‑prem).  

---

## Epics

| Epic | Description |
|------|-------------|
| **E1: Abuse Detection Engine** | Detect anomalous traffic patterns and known abuse signatures. |
| **E2: Mitigation & Policy Engine** | Enforce rate limits, circuit breakers, and custom policies. |
| **E3: Observability & Analytics** | Provide dashboards, alerts, and audit logs. |
| **E4: Integration & Deployment** | SDKs, API gateway plugins, and CI/CD templates. |
| **E5: Security & Compliance** | Authentication, encryption, and compliance reporting. |

---

## User Story Backlog

### Epic E1 – Abuse Detection Engine

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **E1‑S1** | **As a security engineer, I want the system to automatically detect traffic spikes that exceed 5× the 95th percentile of historical rates, so that I can pre‑emptively block potential DDoS attacks.** | • Engine calculates 95th percentile per endpoint over the last 24 h.<br>• Spike detection triggers when current rate > 5× percentile.<br>• Alert is logged and a mitigation rule is auto‑generated. |
| **E1‑S2** | **As a product manager, I want the platform to flag repeated failed authentication attempts per IP, so that I can enforce temporary bans.** | • Tracks failed auth per IP over 10‑minute windows.<br>• Threshold of 10 failures triggers a 30‑minute ban.<br>• Ban is stored in a distributed cache (Redis/Memory). |
| **E1‑S3** | **As a data scientist, I want the engine to learn new abuse patterns from labeled data, so that detection accuracy improves over time.** | • Supports ingestion of labeled abuse logs (CSV/JSON).<br>• Trains a lightweight ML model (e.g., Isolation Forest) nightly.<br>• Model updates are versioned and deployed without downtime. |
| **E1‑S4** | **As a DevOps engineer, I want the detection engine to run in a containerized microservice, so that it can scale horizontally.** | • Dockerfile builds a stateless service.<br>• Exposes `/health` and `/metrics` endpoints.<br>• Supports Kubernetes Horizontal Pod Autoscaler. |

### Epic E2 – Mitigation & Policy Engine

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **E2‑S1** | **As an API consumer, I want to be rate‑limited to 100 requests per minute per API key, so that my usage stays within fair‑use limits.** | • Policy engine enforces 100 req/min per key.<br>• Excess requests receive HTTP 429 with `Retry-After` header.<br>• Policy is configurable via JSON/YAML. |
| **E2‑S2** | **As a system admin, I want to define custom circuit‑breaker thresholds per service, so that downstream failures are isolated.** | • Admin UI allows setting threshold (e.g., 5 % error rate over 1 min).<br>• When exceeded, circuit opens for 30 s.<br>• State transitions are logged. |
| **E2‑S3** | **As a compliance officer, I want to enforce IP whitelisting for sensitive endpoints, so that only approved clients can access them.** | • Whitelist is stored in a secure KV store.<br>• Requests from non‑whitelisted IPs receive HTTP 403.<br>• Whitelist changes trigger a live reload. |
| **E2‑S4** | **As a developer, I want to plug the mitigation engine into my existing API gateway (e.g., Kong, Envoy), so that I can deploy without rewriting code.** | • Provides a sidecar plugin for Kong (Lua) and Envoy (Lua).<br>• Plugin fetches policies from central config service.<br>• Plugin passes through or blocks requests accordingly. |

### Epic E3 – Observability & Analytics

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **E3‑S1** | **As a product owner, I want a real‑time dashboard showing abuse incidents per endpoint, so that I can spot trends.** | • Grafana dashboard pulls data from Prometheus.<br>• Widgets: incidents per endpoint, top offending IPs, mitigation actions.<br>• Dashboard refreshes every 30 s. |
| **E3‑S2** | **As a security analyst, I want audit logs of all mitigation actions, so that I can review post‑incident.** | • Logs stored in Elasticsearch with fields: timestamp, endpoint, action, reason.<br>• Logs are searchable via Kibana.<br>• Export to CSV is available. |
| **E3‑S3** | **As a DevOps engineer, I want the system to expose Prometheus metrics for health, throughput, and error rates.** | • `/metrics` endpoint provides `guardrail_requests_total`, `guardrail_blocked_total`, `guardrail_errors_total`. |
| **E3‑S4** | **As a customer, I want email alerts when my API key is blocked, so that I can investigate.** | • Configurable email template.<br>• Uses SendGrid API.<br>• Alerts include key ID, IP, reason, timestamp. |

### Epic E4 – Integration & Deployment

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **E4‑S1** | **As a developer, I want a Go SDK that wraps the Guardrail API, so that I can integrate easily.** | • SDK provides `NewClient`, `BlockIP`, `GetPolicy` methods.<br>• Handles authentication via API key.<br>• Unit tests cover all public methods. |
| **E4‑S2** | **As a platform engineer, I want Helm charts for Kubernetes deployment, so that I can roll out Guardrail in production.** | • Helm chart includes deployment, service, configmap, and RBAC.<br>• Supports `--set image.tag` for versioning.<br>• Includes tests with `helm lint`. |
| **E4‑S3** | **As a CI engineer, I want automated integration tests that spin up a local Docker Compose stack, so that every PR is verified.** | • `docker-compose.yml` spins up Guardrail, Redis, Prometheus, Grafana.<br>• Tests run against the stack and assert policy enforcement. |
| **E4‑S4** | **As a customer, I want a Terraform module for AWS, so that I can provision Guardrail with IaC.** | • Module provisions ECS Fargate task, ALB, IAM roles.<br>• Supports `var.enable_logging` flag. |

### Epic E5 – Security & Compliance

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **E5‑S1** | **As a security officer, I want all API traffic to be encrypted with TLS 1.3, so that data in transit is protected.** | • API gateway enforces TLS 1.3.<br>• Self‑signed certificates are rejected. |
| **E5‑S2** | **As a compliance lead, I want role‑based access control for the admin console, so that only authorized users can modify policies.** | • Admin console uses OAuth2 with scopes `guardrail:admin`.<br>• RBAC rules stored in PostgreSQL. |
| **E5‑S3** | **As a data privacy officer, I want the system to automatically purge logs older than 90 days, so that we meet retention policies.** | • Log retention job runs nightly.<br>• Deletes entries older than 90 days from Elasticsearch. |
| **E5‑S4** | **As a developer, I want the platform to support GDPR “right to be forgotten”, so that user data can be deleted on request.** | • API endpoint `/v1/users/{id}/delete` triggers deletion.<br>• All references in policies and logs are anonymized. |

---

## MVP Release Plan

| Sprint | Epic | Key Stories |
|--------|------|-------------|
| **Sprint 1** | E1 | E1‑S1, E1‑S2 |
| **Sprint 2** | E1, E2 | E1‑S3, E2‑S1 |
| **Sprint 3** | E2, E3 | E2‑S2, E3‑S1 |
| **Sprint 4** | E3, E4 | E3‑S2, E4‑S1 |
| **Sprint 5** | E4, E5 | E4‑S2, E5‑S1 |
| **Sprint 6** | E5 | E5‑S2, E5‑S3, E5‑S4 |

---

## Definition of Done (DoD)

- Unit tests ≥ 90 % coverage.  
- Integration tests pass in Docker Compose.  
- Documentation updated (README, API docs, Helm/Terraform docs).  
- Security review completed (OWASP Top 10).  
- Performance benchmark: ≤ 200 ms latency under 1,000 req/s.  

---

## Dependencies & Risks

- **Dependencies**: Redis, PostgreSQL, Prometheus, Grafana, SendGrid, Kubernetes.  
- **Risks**:  
  - False positives in detection may block legitimate traffic.  
  - ML model drift requires retraining schedule.  
  - Multi‑cloud deployment may face networking differences.  

---

*Prepared by the Guardrail Product & Engineering Lead*
