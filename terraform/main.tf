terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}
provider "aws" {
  region = "eu-west-1"
}
resource "aws_ecr_repository" "api_ecr" {
  name = "ecommerce-backend-repository"
}
data "aws_vpc" "default" {
  default = true

}
data "aws_internet_gateway" "default" {
  filter {
    name   = "attachment.vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
module "subnets" {
  source              = "git::https://github.com/cloudposse/terraform-aws-dynamic-subnets.git?ref=tags/0.32.0"
  namespace           = "rdx"
  stage               = "dev"
  name                = "ecommerce-api"
  vpc_id              = data.aws_vpc.default.id
  igw_id              = data.aws_internet_gateway.default.id
  cidr_block          = "172.31.0.0/23"
  availability_zones  = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
}
module "security_group" {
  source = "terraform-aws-modules/security-group/aws//modules/http-80"

  name                = "ecommerce-api-sg"
  vpc_id              = data.aws_vpc.default.id
  ingress_cidr_blocks = ["0.0.0.0/0"]
}
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 5.0"

  name            = "ecommerce-api-alb"
  vpc_id          = data.aws_vpc.default.id
  subnets         = module.subnets.public_subnet_ids
  security_groups = [module.security_group.security_group_id]

  target_groups = [
  {
    name         = "ecommerce-api-tg"
    backend_protocol = "HTTP"
    backend_port = 80
    protocol     = "HTTP"
    target_type  = "ip"
    vpc_id       = data.aws_vpc.default.id
    # vpc_id       = module.aws_vpc.default.id
    health_check = {
      path    = "/docs"
      port    = "80"
      matcher = "200-399"
    }
  }
]
http_tcp_listeners = [
  {
    port               = 80
    protocol           = "HTTP"
    target_group_index = 0
  }
]
}
resource "aws_ecs_cluster" "cluster" {
  name = "ecommerce-api-cluster"
}
module "container_definition" {
  source = "git::https://github.com/cloudposse/terraform-aws-ecs-container-definition.git?ref=tags/0.44.0"

  container_name  = "ecommerce-backend-container"
  container_image = "619392411736.dkr.ecr.eu-west-1.amazonaws.com/ecommerce-backend-repository"
  port_mappings   = [
    {
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }
  ]
}
module "ecs_alb_service_task" {
  source = "git::https://github.com/cloudposse/terraform-aws-ecs-alb-service-task.git?ref=tags/0.40.2"

  namespace                 = "rdx"
  stage                     = "dev"
  name                      = "ecommerce-api"
  container_definition_json = module.container_definition.json_map_encoded_list
  ecs_cluster_arn           = aws_ecs_cluster.cluster.arn
  launch_type               = "FARGATE"
  vpc_id                    = data.aws_vpc.default.id
  security_group_ids        = [module.security_group.security_group_id]
  subnet_ids                = module.subnets.public_subnet_ids
  assign_public_ip          = true 

  health_check_grace_period_seconds  = 60
  ignore_changes_task_definition     = false

  ecs_load_balancers = [
    {
      target_group_arn = module.alb.target_group_arns[0]
      elb_name         = ""
      container_name   = "ecommerce-backend-container"
      container_port   = 80
  }]
}


# Set up serverless cluster