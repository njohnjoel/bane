resource "aws_instance" "Private" {
    ami="ami-06cf02a98a61f9f5e"
    instance_type = "t2.micro"
    subnet_id = aws_subnet.tfprivate.id 
    vpc_security_group_ids = [aws_security_group.allow-ssh.id]  
    key_name = aws_key_pair.keypair.key_name
        tags = {
      "Name" = "PrivateInstance"
            }
    }

resource "aws_instance" "Public" {
    ami="ami-06cf02a98a61f9f5e"
    instance_type = "t2.micro"
    subnet_id = aws_subnet.tfpublic.id
    vpc_security_group_ids = [aws_security_group.allow-ssh.id,aws_security_group.allow-http.id] 
    user_data = file("/home/joelj/devops/terraform/03.Invoke_passwd_4mFile_wit_userdata/install_apache.sh")
    key_name = aws_key_pair.keypair.key_name
    tags = {
      "Name" = "PublicInstance"
            }
    
}


