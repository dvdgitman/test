resource "helm_release" "aws_secrets_provider" {
  name       = "aws-secrets-provider"
  repository = "https://aws.github.io/eks-charts"
  chart      = "secrets-store-csi-driver-provider-aws"
  namespace  = "kube-system"
}

resource "helm_release" "rabbitmq" {
  name       = "rabbitmq"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "rabbitmq"
  
  set {
    name  = "auth.username"
    value = "user"
  }

  set {
    name  = "auth.password"
    value = var.rabbitmq_password 
  }
}

resource "helm_release" "alb_controller" {
  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"
  
  set {
    name  = "clusterName"
    value = module.eks.cluster_name
  }
  set {
    name  = "serviceAccount.create"
    value = "false"
  }
  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller" 
    # Note: Requires IAM role creation in iam.tf
  }
}
