# Task 1 – System Design Explanation

## Cloud Architecture & Managed Services
* **Amazon EKS:** Used to host RabbitMQ (via Helm), Algo A consumers, Data Writer, and RestAPI. EKS provides the necessary orchestration for load balancing and scaling.
* **Amazon RDS:** Provides automated backups, patching, and Multi-AZ high availability.
* **Amazon ECR:** Used to store Docker images for Algo A and RestAPI.
* **AWS Secrets Manager:** Used to store database credentials and RabbitMQ passwords securely.
* **AWS Load Balancer Controller:** Manages an Application Load Balancer (ALB) to expose the RestAPI to internet clients via HTTPS.

## Networking Strategy
* **VPC:** Custom Virtual Private Cloud configured with 3 Availability Zones (AZs) for high availability.
    * **Public Subnets:** Host the ALB (Ingress) and NAT Gateways.
    * **Private Subnets:** Host the EKS Worker Nodes to ensure secure isolation.

## Scalability
* **Cluster Scaling:** Karpenter (or Cluster Autoscaler) is configured to provision new EC2 nodes automatically if the Algo A pods require more compute resources than currently available.

## Observability
* **Logs:** Fluent Bit is installed as a DaemonSet to ship container logs to Amazon CloudWatch Logs (or an S3 bucket for cost-effective retention).

## Cost Optimization Strategy
* **EC2 (Compute):** Run `Algo A` pods on **AWS Spot Instances** to save up to 70-90% on compute costs, as these workloads are fault-tolerant.
* **Storage:** Configure **Lifecycle Policies** on Amazon ECR to automatically expire and delete untagged or old images to reduce storage costs.
