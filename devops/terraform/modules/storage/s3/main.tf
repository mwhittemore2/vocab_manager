resource "aws_s3_bucket" "dictionaries" {
    bucket = var.dictionaries_bucket
    acl = "private"

    tags = {
        Name = join(".", [var.project_name, var.deployment, "dictionary_data", "s3"])
    }
}