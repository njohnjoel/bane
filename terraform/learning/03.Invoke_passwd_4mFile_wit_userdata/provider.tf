provider "aws" {
  version = "~> 2.8"
  access_key = var.access
  secret_key = var.secret
  region = var.region
}

resource "aws_instance" "TFref" {
    ami           = "ami-06cf02a98a61f9f5e"
    instance_type = "t2.micro"
    security_groups = ["Open2All"]
    key_name      = "NVkey"
    user_data = file("/home/joelj/devops/terraform/03.Invoke_passwd_4mFile_wit_userdata/install_apache.sh")
    #user_data = "${file("install_apache.sh")}"
    tags = {
        Name = "FromTF"
    }
}