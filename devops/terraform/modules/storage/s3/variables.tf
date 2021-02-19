variable "deployment" {
    type        = string
    description = "The environment being deployed to"
    default     = "dev"
}

variable "dictionaries_bucket" {
    type        = string
    description = "Stores dictionary data for translation service"
    default     = "mwhittemore-vocab-manager-dictionaries"
}

variable "project_name" {
    type        = string
    description = "The name of the project being deployed"
    default     = "vocabulary_manager"
}