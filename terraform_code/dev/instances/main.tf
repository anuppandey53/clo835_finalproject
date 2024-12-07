provider "aws" {
  region = "us-east-1"  # Adjust the region as needed
}

# Create ECR repository for DB
resource "aws_ecr_repository" "dbapp" {
  name = "db-repository"
}

# Create ECR repository for App
resource "aws_ecr_repository" "webapp" {
  name = "app-repository"
}


# Create an EBS volume with gp2 type and 16 GiB size
resource "aws_ebs_volume" "db_volume" {
  availability_zone = "us-east-1a"  # Adjust the availability zone as needed
  size              = 16            # Size updated to 16 GiB
  type              = "gp2"          # General Purpose SSD
  tags = {
    Name = "db-volume"
  }
}
