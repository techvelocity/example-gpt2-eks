# velocity-gpt2-eks-example

## Create EKS cluster

```
eksctl create cluster -f cluster.yaml 
```
```
aws eks update-kubeconfig --region <region> --name <cluster name>
```
```
eksctl utils associate-iam-oidc-provider --region=<region> --cluster=<cluster name> --approve
```
```
eksdemo install storage-ebs-csi -c <cluster name> --region <region>
```
## Add AWS Creds
```
kubectl create secret generic aws-credentials \
    --from-literal=aws_access_key_id=<your-access-key-id> \
    --from-literal=aws_secret_access_key=<your-secret-access-key> \
    --from-literal=aws_session_token=<your-session-token>
```
## Train model in EKS & store in S3
```
kubectl apply -f train.yaml
```
## Dockerize FastAPI app

See Dockerfile for example
>**NOTE:** the tensorflow/tensorflow base image ships with Python3.8, which I updated to 3.10 for compatibility with FastAPI

Push to registry

## Deploy to EKS
```
kubectl apply -f deployment.yaml
```
## Test the deployment
```
kubectl get all    

kubectl exec -it <pod name> -- /bin/bash
```
```
curl -X 'POST' \
  'http://localhost:8000/api/generate?prompt=computers%20are%20cool' \
  -H 'accept: application/json' \
  -d ''
```
