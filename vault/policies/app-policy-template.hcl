# HashiCorp Vault Policy Template for App Factory
# Policy name format: app-[id]-[name]-policy
# Example: app-01-nebula-policy

# Grant read/list permissions only to the specific application's path
path "secret/data/app-factory/app-$APP_ID-$APP_NAME/*" {
  capabilities = ["read", "list"]
}

# Explicitly deny access to other app paths (Defense in Depth)
path "secret/data/app-factory/app-*" {
  capabilities = ["deny"]
}

# Allow reading public/shared config keys (optional global settings)
path "secret/data/app-factory/shared/*" {
  capabilities = ["read", "list"]
}
