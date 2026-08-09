# Kubernetes Flask API

## Project Overview

This project demonstrates how to containerize a Python Flask API with Docker and depoly the application to Kubernetes.

The purpose of this project is to gain hands-on experience with Docker, Kubernetes workloads.

## Technologies Used

- Python
- Flask
- Docker
- Kubernetes
- kubectl
- Git

## Architecture

The app follows this request flow:

Client
  |
  v
Kubernetes Service
  |
  v
Kubernetes Deployment
  |
  v
Pods
  |
  v
Docker Containers
  |
  v
Flask API

## Application Endpoints

The Flask application exposes the following endpoints:

### GET /

Returns basic information about the application.

### GET /health

Returns the health status of the application.

This endpoint is also used by the Kubernetes readiness and liveness probes.

### GET /users

Returns a list of example users.

## Project Structure

kubernetes-flask-api/
|
├── app/
│   ├── app.py
│   └── requirements.txt
|
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
|
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md

## Docker

The Flask application is packaged into a Docker image.

Build the image:

```bash
docker build -t kubernetes-flask-api:v1 .
```
Run the container

```bash
docker run --name flask-api -p 8000:8000 kubernetes-flask-api:v1
```

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/users
```


















