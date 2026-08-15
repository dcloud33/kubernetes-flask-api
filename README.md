Kubernetes Flask API

A containerized Python REST API deployed to Kubernetes, built as a hands-on project to demonstrate containerization, Kubernetes workload management, service networking, health monitoring, configuration management, scaling, self-healing, and troubleshooting.

Project Overview

This project demonstrates the process of taking a Python Flask application from local development to a containerized workload running on Kubernetes.

The application is first packaged into a Docker image and then deployed to Kubernetes using declarative YAML manifests.

Kubernetes manages multiple replicas of the application, provides stable network access through a Service, performs application health checks, injects configuration through a ConfigMap, and maintains the desired number of running Pods.

The project also includes intentional failure testing to practice troubleshooting Kubernetes workloads and networking.

---

Architecture

                    Client
                      |
                      | HTTP
                      v
             Kubernetes Service
                  Port 80
                      |
               app=flask-api
                      |
              +-------+-------+
              |               |
              v               v
           Pod 1            Pod 2
              |               |
              v               v
       Flask Container   Flask Container
           :8000             :8000
              |               |
              +-------+-------+
                      |
                /health endpoint
                      |
              Readiness/Liveness
                    Probes

Kubernetes Workload Architecture

Kubernetes Cluster
        |
        v
Namespace: flask-api
        |
        +--------------------+
        |                    |
        v                    v
   Deployment             ConfigMap
        |                    |
        v                    | APP_ENV
    ReplicaSet                |
        |                     |
   +----+----+                |
   |         |                |
   v         v                |
 Pod 1     Pod 2 <------------+
   |         |
   v         v
Container  Container
   |         |
   v         v
 Flask     Flask

---

Technologies

- Python
- Flask
- Docker
- Kubernetes
- kubectl
- Git

---

Project Structure

kubernetes-flask-api/
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
│
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md

File Responsibilities

File| Purpose
"app/app.py"| Flask API application
"app/requirements.txt"| Python application dependencies
"Dockerfile"| Defines how the Flask container image is built
".dockerignore"| Excludes unnecessary files from the Docker build context
".gitignore"| Prevents local and generated files from being committed
"namespace.yaml"| Creates the Kubernetes namespace
"deployment.yaml"| Defines and manages the Flask application workload
"service.yaml"| Provides stable network access to the Flask Pods
"configmap.yaml"| Provides external application configuration

---

Flask API

The application provides a small REST API used to demonstrate container and Kubernetes functionality.

Endpoints

"GET /"

Returns basic application information and the current application environment.

Example:

{
  "message": "Welcome to my Kubernetes Flask API",
  "environment": "kubernetes"
}

"GET /health"

Returns the health status of the application.

{
  "status": "healthy"
}

This endpoint is also used by Kubernetes readiness and liveness probes.

"GET /users"

Returns example user data.

---

Running the Application Locally

1. Create a Python Virtual Environment

python3 -m venv .venv

Activate it:

source .venv/bin/activate

2. Install Dependencies

pip install -r app/requirements.txt

3. Start the Application

python app/app.py

The application listens on:

http://localhost:8000

Test:

curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/users

---

Docker

The Flask application is packaged into a Docker image so the application and its runtime dependencies can be deployed consistently.

Build the Image

From the project root:

docker build -t kubernetes-flask-api:v1 .

The build process follows:

Application Source
       |
       v
Dockerfile
       |
       v
docker build
       |
       v
Docker Image
kubernetes-flask-api:v1

Run the Container

docker run --name flask-api -p 8000:8000 kubernetes-flask-api:v1

Request path:

localhost:8000
      |
      v
Docker Host Port :8000
      |
      v
Container Port :8000
      |
      v
Flask

Verify:

curl http://localhost:8000/health

---

Kubernetes

The containerized Flask API is deployed to a local Kubernetes cluster.

Kubernetes manages the application's desired state rather than requiring individual containers to be manually created and maintained.

---

Namespace

The application runs inside the dedicated:

flask-api

namespace.

Deploy it:

kubectl apply -f kubernetes/namespace.yaml

Verify:

kubectl get namespaces

Using a dedicated namespace logically groups the resources belonging to the application.

---

Deployment

The Flask API runs as a Kubernetes Deployment.

Deploy:

kubectl apply -f kubernetes/deployment.yaml

Verify:

kubectl get deployments -n flask-api

View Pods:

kubectl get pods -n flask-api

The workload relationship is:

Deployment
    |
    v
ReplicaSet
    |
    +-------------+
    |             |
    v             v
  Pod 1         Pod 2
    |             |
    v             v
Container      Container
    |             |
    v             v
 Flask           Flask

The Deployment declares two application replicas.

replicas: 2

Kubernetes continuously works to maintain that desired state.

---

Kubernetes Service Networking

Pods are ephemeral and can be replaced during failures, scaling operations, or deployments.

Instead of connecting directly to individual Pods, the application uses a Kubernetes "ClusterIP" Service.

Deploy the Service:

kubectl apply -f kubernetes/service.yaml

Verify:

kubectl get services -n flask-api

The Service listens on port "80" and forwards requests to the Flask application on port "8000".

Client
   |
   v
Service :80
   |
   | selector
   | app=flask-api
   |
   +-------------+
   |             |
   v             v
Pod :8000     Pod :8000
   |             |
   v             v
 Flask          Flask

The Service discovers the application Pods through Kubernetes labels and selectors.

The Service selector:

selector:
  app: flask-api

matches the Pod label:

labels:
  app: flask-api

---

Accessing the Application

Because the application uses a "ClusterIP" Service, port forwarding can be used for local access.

kubectl port-forward service/flask-api 8080:80 -n flask-api

The complete request path becomes:

localhost:8080
      |
      v
kubectl port-forward
      |
      v
Kubernetes Service :80
      |
      v
Pod :8000
      |
      v
Flask Container
      |
      v
Flask API

From another terminal:

curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/users

---

Application Health Checks

The Deployment uses both Kubernetes readiness and liveness probes against the Flask "/health" endpoint.

Readiness Probe

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 3
  periodSeconds: 5

The readiness probe answers:

«Is this application ready to receive traffic?»

Conceptually:

Kubelet
   |
   | HTTP GET
   v
Pod :8000/health
   |
   v
Flask
   |
   +---- Healthy ----> Pod Ready
   |                       |
   |                       v
   |                Receive traffic
   |
   +---- Failed -----> Pod NotReady
                           |
                           v
                   Do not route normal
                   Service traffic here

---

Liveness Probe

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10

The liveness probe answers:

«Is the application still functioning correctly?»

Kubelet
   |
   | HTTP GET
   v
/health
   |
   +---- Healthy
   |        |
   |        v
   |   Keep running
   |
   +---- Repeated failures
            |
            v
       Restart container

This demonstrates two different operational concerns:

Readiness

Should traffic be sent to this Pod?

Liveness

Should this container continue running?

---

Kubernetes Configuration Management

Application configuration is externalized using a Kubernetes ConfigMap.

The ConfigMap contains:

APP_ENV=kubernetes

Deploy:

kubectl apply -f kubernetes/configmap.yaml

The Deployment injects the value into the container environment.

ConfigMap
APP_ENV=kubernetes
       |
       v
Deployment
       |
       v
Pod
       |
       v
Container Environment
       |
       v
APP_ENV
       |
       v
Python
       |
       v
os.getenv("APP_ENV")

This separates application configuration from application source code.

---

Scaling

The Deployment can be manually scaled to demonstrate Kubernetes replica management.

Scale to four Pods:

kubectl scale deployment flask-api --replicas=4 -n flask-api

Verify:

kubectl get pods -n flask-api

The desired state becomes:

Deployment
Desired Replicas = 4
        |
        v
ReplicaSet
        |
   +----+----+----+----+
   |    |    |    |    |
   v    v    v    v
 Pod  Pod  Pod  Pod

Scale back:

kubectl scale deployment flask-api --replicas=2 -n flask-api

---

Kubernetes Self-Healing

The project demonstrates Kubernetes reconciliation by intentionally deleting a running Pod.

View Pods:

kubectl get pods -n flask-api

Delete one:

kubectl delete pod <pod-name> -n flask-api

Watch:

kubectl get pods -n flask-api -w

The Deployment still declares:

Desired replicas = 2

Deleting one Pod produces:

Desired = 2
Actual = 1
     |
     v
Kubernetes detects mismatch
     |
     v
ReplicaSet creates replacement Pod
     |
     v
Desired = 2
Actual = 2

This demonstrates Kubernetes' reconciliation and desired-state model.

---

Rolling Application Updates

Application updates can be deployed by building a new image version.

Example:

docker build -t kubernetes-flask-api:v2 .

Update the Deployment image:

image: kubernetes-flask-api:v2

Apply:

kubectl apply -f kubernetes/deployment.yaml

Monitor:

kubectl rollout status deployment/flask-api -n flask-api

Conceptually:

Deployment
     |
     +------ Old ReplicaSet
     |         |
     |         +-- v1 Pods
     |
     +------ New ReplicaSet
               |
               +-- v2 Pods

Kubernetes progressively replaces the old application Pods with the new version.

---

Troubleshooting Exercises

An important goal of this project is learning how to diagnose Kubernetes problems rather than only deploying a working application.

Pod Troubleshooting

Check workload state:

kubectl get pods -n flask-api

Inspect a Pod:

kubectl describe pod <pod-name> -n flask-api

Inspect logs:

kubectl logs <pod-name> -n flask-api

Follow logs:

kubectl logs -f <pod-name> -n flask-api

A general troubleshooting workflow is:

Problem
   |
   v
kubectl get pods
   |
   v
Identify abnormal state
   |
   v
kubectl describe pod
   |
   v
Inspect Events
   |
   v
kubectl logs
   |
   v
Determine root cause

---

ImagePullBackOff Testing

An invalid image tag can be intentionally configured:

image: kubernetes-flask-api:does-not-exist

The resulting Pod state can then be investigated with:

kubectl get pods -n flask-api

and:

kubectl describe pod <pod-name> -n flask-api

This demonstrates troubleshooting container image retrieval and Pod startup failures.

---

Service Networking Troubleshooting

The Service selector can intentionally be changed from:

selector:
  app: flask-api

to:

selector:
  app: wrong-app

Because the selector no longer matches the Pod labels, the Service will not identify the expected application backends.

Investigate with:

kubectl get services -n flask-api

kubectl get endpoints -n flask-api

kubectl get endpointslices -n flask-api

This demonstrates the relationship between:

Service selector
      |
      v
Pod labels
      |
      v
Service backend discovery

---

Useful Kubernetes Commands

# Cluster
kubectl get nodes

# Namespaces
kubectl get namespaces

# Deployments
kubectl get deployments -n flask-api

# Pods
kubectl get pods -n flask-api

# Detailed Pod information
kubectl describe pod <pod-name> -n flask-api

# Logs
kubectl logs <pod-name> -n flask-api

# Services
kubectl get services -n flask-api

# Service endpoints
kubectl get endpoints -n flask-api

# EndpointSlices
kubectl get endpointslices -n flask-api

# Deployment rollout
kubectl rollout status deployment/flask-api -n flask-api

# Scale application
kubectl scale deployment flask-api --replicas=4 -n flask-api

# Watch Pods
kubectl get pods -n flask-api -w

---

Key Concepts Demonstrated

This project demonstrates hands-on experience with:

- Python REST API development
- Python dependency management
- Docker image creation
- Containerized application deployment
- Kubernetes namespaces
- Kubernetes Deployments
- ReplicaSets
- Pods
- Containers
- Kubernetes labels and selectors
- ClusterIP Services
- Kubernetes service discovery
- Container and Service port mapping
- Readiness probes
- Liveness probes
- ConfigMaps
- Environment-based configuration
- Manual horizontal scaling
- Kubernetes desired-state management
- Kubernetes reconciliation and self-healing
- Rolling application updates
- Pod troubleshooting
- Container log analysis
- "ImagePullBackOff" troubleshooting
- Kubernetes Service and endpoint troubleshooting

---

