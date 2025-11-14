#!/bin/bash
set -e

AWS_REGION=${1:-us-east-1}
PROJECT_NAME=${2:-guestbook-stage1}

ECR_REPO="${PROJECT_NAME}-app"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Build image for AMD64 (ECS Fargate architecture)
docker build --platform linux/amd64 -t ${ECR_REPO}:latest .

# Tag image
docker tag ${ECR_REPO}:latest ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:latest

# Push to ECR
docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:latest

echo "Done! Image pushed to ECR"
