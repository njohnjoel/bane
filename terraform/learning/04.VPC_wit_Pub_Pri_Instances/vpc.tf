provider "aws" {
  version = "~> 2.8"
  access_key = var.access
  secret_key = var.secret
  region = var.region
}

resource "aws_vpc" "tfvpc" {
    cidr_block = "10.0.0.0/16"
    instance_tenancy = "default"
    #Default/Shared Tenancy means that multiple EC2 instances from different customers may reside on the same piece of physical hardware. 
    #The dedicated model means that your EC2 instances will only run on hardware with other instances that you've deployed, 
    #no other customers will use the same piece of hardware as you
    enable_dns_support = "true"
    #https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcAttribute.html
    enable_dns_hostnames = "true"
    #https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html
    enable_classiclink = "false"
    #https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/vpc-classiclink.html

    tags = {
        name = "Terraform"
    }
  #Tags are not working generally for VPC , refer : https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/resource-tagging


}

#Subnets
resource "aws_subnet" "tfpublic" {
  vpc_id                  = aws_vpc.tfvpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = "true"
  availability_zone       = var.az
  tags = {
    Name = "Public"
  }
}

resource "aws_subnet" "tfprivate" {
  vpc_id                  = aws_vpc.tfvpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = "false"
  availability_zone       = var.az
  tags = {
    Name = "Private"
  }
}

#internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.tfvpc.id

  tags = {
    Name = "tfigw"
  }
}

# route tables
resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.tfvpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "tf_RT"
  }
}


# route associations public
resource "aws_route_table_association" "route_association" {
  subnet_id      = aws_subnet.tfpublic.id
  route_table_id = aws_route_table.RT.id      
  
}


#Security Groups
resource "aws_security_group" "allow-ssh" {
  vpc_id = aws_vpc.tfvpc.id
  name= "allow-ssh"
  description = "security group that allow ssh and all outgoing traffic"

#Ingress = incoming / inbound
#egress = Outgoing / outbound 
        egress  {
                  from_port=0
                  to_port=0
                  protocol = "-1"
                  cidr_blocks = ["0.0.0.0/0"]
                  }


        ingress {
                  from_port=22
                  to_port=22
                  protocol="tcp"
                  cidr_blocks=["0.0.0.0/0"]
                }
        tags = {
            Name = "allow-ssh"
        }
}


resource "aws_security_group" "allow-http" {
  vpc_id = aws_vpc.tfvpc.id
  name= "allow-https"
  description = "allow ssh, http, https"

#Ingress = incoming 
#egress = Outgoing
        egress  {
                  from_port=0
                  to_port=0
                  protocol = "-1"
                  cidr_blocks = ["0.0.0.0/0"]
                  }


        ingress {
                  from_port=22
                  to_port=22
                  protocol="tcp"
                  cidr_blocks=["0.0.0.0/0"]
                }

         tags = {
            Name = "allow-ssh"
        }
}

resource "aws_key_pair" "keypair" {
    key_name = "keypair.pub"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDXupJ6mOO5DEcYa962o5JlSqBIpeLEGucZuMFiU8ircJf2iHy6+K6bOgsBn/MkPvZrSKdf8tSiJ2/qkXjn86wqsJewXObLj2U8zotHRnrYParg4D+TTy2mq4jSjHcuysnYFX8yrYC9OILxVzrhzm1jqOA275v0/WbJtAYCMqMNBGo4Ie38Cny1uIShTT8m48K0hkgoS9UyL4qJ8qhZGMuOir85vYnohmR4JXiwuGdYDlSJubDXKaXhWDPb17Gwn0kXzgqaEn9i1q2/geolctdWZSZZ5KJowd8EStSGSMf2XycQHGItFAvFc2TEJxZzh8Tusl88ikxL4GMHamP0iW5L joelj@global"
}