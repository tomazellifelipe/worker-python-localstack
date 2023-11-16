variable "queue_name" {
  description = "Application name"
  type        = string
  validation {
    condition     = length(var.queue_name) <= 64
    error_message = "Lenght of application name must be less or equal than 64 chars."
  }
}

variable "localstack_endpoint" {
  description = "Localstack endpoint, this may change if using inside a docker compose"
  type        = string
  default     = "http://localhost:4566"
}
