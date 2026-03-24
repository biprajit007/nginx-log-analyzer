# nginx-log-analyzer

A FastAPI web app for uploading an nginx access log and getting a parsed summary of referrers, paths, status codes, and user agents.

## Key features

- Browser upload form
- Regex-based parsing of common nginx access log format
- Top-N summaries for referrers, paths, and user agents
- Runs in Docker via the supplied Dockerfile and Compose file

## Project structure

- `app.py` — Upload endpoint, regex parser, and HTML UI
- `Dockerfile` — Container image build
- `docker-compose.yml` — Local app runtime

## Requirements

- Docker and Docker Compose, or Python 3.11 with the listed requirements

## Setup

```bash
git clone https://github.com/biprajit007/nginx-log-analyzer.git
cd nginx-log-analyzer
docker compose up --build
```

## Usage

### Open the UI

```bash
http://localhost:18200/
```

### Upload an access log

```bash
Use the file picker in the browser, or POST a multipart file to /analyze
```

## Limitations / next improvements

- Parser expects a specific access log format
- Large files are processed in memory
- No saved reports or auth
