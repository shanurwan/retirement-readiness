provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_instance" "retirement_ec2" {
  ami           = "ami-0c5199d385b432989"  # Ubuntu 22.04 LTS in Singapore
  instance_type = "t2.micro"
  key_name      = "mlops1-key"

  tags = {
    Name = "mlops-zoomcamp"
  }

  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y docker.io
              sudo systemctl start docker
              sudo usermod -aG docker ubuntu
              docker --version
            EOF
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "retirement_data" {
  bucket        = "retirement-readiness-data-01"
  force_destroy = true

  tags = {
    Name = "Retirement Readiness Data"
  }
}

output "ec2_public_ip" {
  value = aws_instance.retirement_ec2.public_ip
}

output "bucket_name" {
  value = aws_s3_bucket.retirement_data.bucket
}
