# ECommerce Backend - Fast API

This is a fastapi service that can be a standalone webapp using the static html in the 'static' direcotry or use the API endpoints to make this a solely backend service.

It also contains IaC found in the terraform directory - this will deploy the image on AWS Fargate and make the API endpoints available over http.

Commands:

Docker

docker compose up

Without docker

make dev

Terraform

terraform init

terraform apply

CDK

Not yet working

