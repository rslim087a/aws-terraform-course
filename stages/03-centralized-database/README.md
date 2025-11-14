# Stage 3: Production Architecture (ECS + RDS)

This stage solves the data consistency problem by adding a centralized RDS MySQL database in private subnets, shared by all ECS tasks. Run `terraform init && terraform apply` (takes ~5 min for RDS to provision), then `./build-and-push.sh us-east-1 guestbook-stage3` to build and push the updated Docker image with MySQL support, and access the app via the ALB URL - now all tasks share the same database so data is consistent across requests, demonstrating a production-ready architecture with HA, load balancing, and centralized data storage.
