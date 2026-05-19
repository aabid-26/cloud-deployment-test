# Zero-to-Cloud Automated API

A professional-grade DevOps pipeline that takes a Python FastAPI application from local development to a live, auto-deploying cloud service. Every `git push` to `main` automatically builds, containerises, and deploys the latest version to AWS — no manual steps required.

---

## What This Project Does

This project demonstrates a complete, production-style DevOps workflow:

- A **Python FastAPI** application with a root endpoint and a `/health` monitoring endpoint
- **Dockerised** for consistent, portable execution across any environment
- **Hosted on AWS EC2** (Ubuntu Linux) and accessible publicly via the internet
- **Fully automated** via a GitHub Actions CI/CD pipeline — push code, and the server updates itself

---

## Architecture Overview

```
Your Laptop
    │
    │  git push
    ▼
GitHub Repository
    │
    ├── Triggers GitHub Actions (deploy.yml)
    │       │
    │       ├── Builds Docker image
    │       ├── Pushes image → Docker Hub
    │       └── SSHs into AWS EC2
    │               │
    │               ├── Stops old container
    │               └── Runs new container on :8000
    │
    └── Live API accessible at http://<SERVER_IP>:8000
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Python, FastAPI, Uvicorn |
| Containerisation | Docker, Docker Hub |
| Cloud Infrastructure | AWS EC2 (Ubuntu, t2.micro) |
| CI/CD Automation | GitHub Actions |
| Version Control | Git, GitHub |

---

## Project Structure

```
devops-cloud-api/
├── main.py                        # FastAPI application
├── requirements.txt               # Python dependencies (fastapi, uvicorn)
├── Dockerfile                     # Container build instructions
├── .dockerignore                  # Excludes venv/ and __pycache__/
├── .gitignore                     # Excludes venv/ and __pycache__/
└── .github/
    └── workflows/
        └── deploy.yml             # CI/CD pipeline definition
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns a Hello World message |
| `GET` | `/health` | Health check for monitoring |
| `GET` | `/docs` | Interactive Swagger UI (auto-generated) |

---

## How the CI/CD Pipeline Works

On every push to `main`, the `deploy.yml` workflow:

1. Checks out the latest code
2. Logs into Docker Hub using stored credentials
3. Builds a fresh Docker image and pushes it to Docker Hub
4. SSHs into the AWS EC2 server using the stored key
5. Stops and removes the currently running container
6. Pulls the new image and runs it on port 8000

No manual deployment needed after initial setup.

---

## Setup & Deployment

### Prerequisites

- Docker and Docker Hub account
- AWS account with an EC2 instance running Ubuntu
- GitHub repository with Actions enabled

### Required GitHub Secrets

Configure these in your repository under **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub password |
| `SERVER_IP` | Public IPv4 address of your EC2 instance |
| `SERVER_KEY` | Contents of your `.pem` private key file |

### EC2 Security Group Rules

Ensure your AWS Security Group has the following inbound rules:

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 22 | TCP | Your IP | SSH access |
| 8000 | TCP | 0.0.0.0/0 | Public API access |

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/devops-cloud-api.git
cd devops-cloud-api

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Running with Docker Locally

```bash
# Build the image
docker build -t devops-api .

# Run the container
docker run -p 8000:8000 devops-api
```

### Deploy

Simply push to `main`:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

GitHub Actions handles everything from there.

---

## AWS Instance Management

> **Important:** Every time you stop and restart your EC2 instance, AWS assigns a new public IP address. You must update the `SERVER_IP` secret in GitHub to match.

| Action | Effect |
|---|---|
| **Stop instance** | Saves your files, pauses billing for compute time |
| **Terminate instance** | Permanently destroys the server — only do this when finished |

The AWS Free Tier includes 750 hours/month of `t2.micro` compute — enough to run one instance 24/7 without charges.

---

## Skills Demonstrated

- Writing and containerising a Python web API
- Authoring a multi-stage `Dockerfile` with layer caching optimisation
- Provisioning and securing cloud infrastructure on AWS
- Linux server administration via SSH
- Writing a GitHub Actions CI/CD workflow from scratch
- Managing secrets securely in a CI/CD context
