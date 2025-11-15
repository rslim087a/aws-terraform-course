# AWS Terraform Course

This repository contains the project files for the AWS Terraform Youtube and Written course.

## Docker Course

This course will deploy apps using Docker containers (as is the standard). If you are new to containerization, I **highly** recommend checking out my Docker Course: https://rayanslim.com/course/docker-course

In this day and age, containers are industry standard.

## Prerequisites:

- **AWS Account with credentials configured:** https://rayanslim.com/course/aws-iam-course

- **Install Docker:** https://www.youtube.com/watch?v=HdDdzpakWYw

- **Terraform installed:**

**Mac**: 
```
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform --version
```

**Windows**: 
Using Chocolatey or Scoop
```powershell
choco install terraform

## OR

scoop install terraform

terraform --version
```

## Useful Links

1. https://registry.terraform.io/providers/hashicorp/aws/latest/docs#provider-configuration
2. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc
3. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/internet_gateway
4. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones
5. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet
6. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association
7. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository
8. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_cluster
9. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role
10. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment
11. https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group
