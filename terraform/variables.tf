variable "repo_name" {
  description = "The repository name"
  type = string
  default = "coffee_api"
}

variable "branch_default_name" {
  description = "The branch name"
  type = string
  default = "env/staging"
}

variable "db_password" {
  description = "The database password"
  type = string
}

variable "db_user" {
  description = "The database user"
  type = string
  default = "dbuser"
}

variable "db_name" {
  description = "The database user"
  type = string
  default = "coffeeapi"
}

variable "db_host" {
  description = "The database host"
  type = string
  default = "coffee-db-service"
}

variable "token" {
  description = "The repo token"
  type = string
}
