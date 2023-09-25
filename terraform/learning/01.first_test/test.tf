provider "aws" {
  version = "~> 2.8"
  region  = "us-east-1"
  access_key ="AKIA5R33I4J3NCKKZ2WI"
  secret_key = "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"
}

resource "aws_instance" "Praveen" {
  ami           = "ami-0ff8a91507f77f867"
  instance_type = "t2.micro"
  key_name      = "NVkey"
  #subnet_id    = subnet-859a96d9

  tags = {
    Name = "Terraform-Instance"
  }
}