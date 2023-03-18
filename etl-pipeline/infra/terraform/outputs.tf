output "db_url_string" {
  description = "MySQL database connection URL, https://www.ietf.org/rfc/rfc1738.txt"
  value       = "mysql://${var.db_username}:${var.db_password}@${aws_db_instance.etl_mysql.address}/${aws_db_instance.etl_mysql.db_name}"
}