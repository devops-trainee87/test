terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
  backend "local" {
  }
}

provider "github" {
  token = var.token
}

resource "github_repository" "repo" {
  name        = var.repo_name
  description = "Repository for the Coffee API service"
  visibility = "public"
  auto_init = true
  security_and_analysis {
    secret_scanning {
      status = "enabled"
    }
    secret_scanning_push_protection {
      status = "enabled"
    }
  }
}

resource "github_branch" "stage" {
  repository = github_repository.repo.name
  branch     = var.branch_default_name
}

resource "github_branch_default" "default" {
  repository = github_repository.repo.name
  branch     = github_branch.stage.branch
}

resource "github_branch_protection" "main" {
  repository_id = github_repository.repo.name
  pattern = "main"
}

resource "github_branch_protection" "stage" {
  repository_id = github_repository.repo.name
  pattern = var.branch_default_name
}

resource "github_actions_secret" "db_password" {
  repository       = github_repository.repo.name
  secret_name      = "POSTGRES_PASSWORD"
  plaintext_value  = var.db_password
}

resource "github_actions_variable" "db_user" {
  repository       = github_repository.repo.name
  variable_name    = "POSTGRES_USER"
  value  = var.db_user
}

resource "github_actions_variable" "db_name" {
  repository       = github_repository.repo.name
  variable_name    = "POSTGRES_DB"
  value  = var.db_name
}

resource "github_actions_variable" "db_host" {
  repository       = github_repository.repo.name
  variable_name    = "DB_HOST"
  value  = var.db_host
}
