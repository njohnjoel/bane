provider "aws" {
  version = "~> 2.8"
  region  = "us-east-1"
    access_key ="AKIA5R33I4J3PQQUHL7G"
    secret_key = "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"
  #access_key ="${var.access_key}"
  #secret_key = "${var.secret_key}"
}
resource "aws_instance" "terraform" {

  count = 5
  ami           = "ami-0ff8a91507f77f867"
  instance_type = "t2.micro"
  key_name      = "NVkey"
  #user_data = "value"
  #subnet_id    = subnet-859a96d9

  tags = {
    Name = "aws1"
  }
}