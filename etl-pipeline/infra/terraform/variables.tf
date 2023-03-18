variable "aws_region" {
  description = "AWS region to deploy DB into"
  type        = string
}

variable "rds_subnet1" {
  description = "Subnet 1 to deploy RDS instance"
  type        = string
}

variable "rds_subnet2" {
  description = "Subnet 2 to deploy RDS instance"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID to deploy RDS instance"
  type        = string
}

variable "db_instance" {
  description = "RDS instance type to use"
  type        = string
}

variable "db_storage_size" {
  description = "Storage capacity of RDS in GBs"
  type        = number
}

variable "db_username" {
  description = "RDS instance type to use"
  type        = string
}

variable "db_password" {
  description = "RDS instance type to use"
  type        = string
}