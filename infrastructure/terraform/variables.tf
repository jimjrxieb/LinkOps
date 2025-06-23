variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "linkops-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "linkops-aks"
}

variable "node_count" {
  description = "Number of AKS nodes"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "Size of AKS nodes"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "monitoring_vm_size" {
  description = "Size of monitoring VM"
  type        = string
  default     = "Standard_B2s"
}

variable "grafana_admin_password" {
  description = "Admin password for Grafana"
  type        = string
  sensitive   = true
  default     = "LinkOps2024!"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "demo"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "linkops"
} 