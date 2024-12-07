# Define the provider
provider "aws" {
  region = "us-east-1"
}

# Define tags locally
locals {
  default_tags = {
    "env" = "production"  # Example environment tag
    "Name" = "clo835-finalproject"
  }
}

# ECR Repository for webapp
resource "aws_ecr_repository" "webapp" {
  name                 = "clo835-finalproject-webapp"
  image_tag_mutability = "MUTABLE"

  tags = merge(local.default_tags,
    {
      "Name" = "clo835-finalproject-webapp"
    }
  )
}

# ECR Repository for dbapp
resource "aws_ecr_repository" "dbapp" {
  name                 = "clo835-finalproject-mysql"
  image_tag_mutability = "MUTABLE"

  tags = merge(local.default_tags,
    {
      "Name" = "clo835-finalproject-mysql"
    }
  )
}

# EBS Volume for DB (gp2 type, 10 GB)
resource "aws_ebs_volume" "db_volume" {
  availability_zone = "us-east-1a"  # Adjust the availability zone as needed
  size              = 10            # Size of the volume in GiB (10 GB)
  type              = "gp2"          # General Purpose SSD (gp2)

  tags = merge(local.default_tags,
    {
      "Name" = "db-volume"
    }
  )
}
