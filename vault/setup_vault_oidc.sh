#!/usr/bin/env bash

# Vault configuration helper script used by DevOps Automator
# Set Vault Address and Admin Token
# export VAULT_ADDR="https://vault.internal.factory.com"
# export VAULT_TOKEN="hvs.xxxxxxxxxx"

# 1. Enable JWT Auth method for GitHub Actions OIDC if not enabled
vault auth list | grep -q "github-actions-oidc"
if [ $? -ne 0 ]; then
  echo "Enabling JWT auth method for GitHub Actions..."
  vault auth enable -path=github-actions-oidc jwt
fi

# 2. Configure JWT auth method to trust GitHub OIDC Token Issuer
echo "Configuring JWT Auth settings for GitHub..."
vault write auth/github-actions-oidc/config \
  oidc_discovery_url="https://token.actions.githubusercontent.com" \
  bound_issuer="https://token.actions.githubusercontent.com"

# 3. Dynamic setup function for new applications
setup_app_security() {
  local app_id=$1
  local app_name=$2
  local repo_path=$3 # e.g. org/appFactory
  
  local policy_name="${app_id}-${app_name}-policy"
  local role_name="${app_id}-${app_name}-role"
  
  echo "Setting up Vault security for ${app_id}-${app_name}..."
  
  # A. Generate policy file from template
  local policy_file="/tmp/${policy_name}.hcl"
  sed -e "s/\$APP_ID/${app_id}/g" -e "s/\$APP_NAME/${app_name}/g" \
      vault/policies/app-policy-template.hcl > "$policy_file"
  
  # B. Write policy to Vault
  vault policy write "$policy_name" "$policy_file"
  rm "$policy_file"
  
  # C. Create JWT Role mapping in Vault for GitHub OIDC claims
  vault write auth/github-actions-oidc/role/"$role_name" - <<EOF
{
  "role_type": "jwt",
  "token_policies": ["$policy_name"],
  "token_ttl": 3600,
  "token_max_ttl": 7200,
  "bound_audiences": ["https://github.com/${repo_path}"],
  "user_claim": "actor",
  "bound_claims": {
    "repository": "${repo_path}",
    "ref": "refs/heads/feature/${app_id}-${app_name}"
  },
  "bound_claims_type": "glob"
}
EOF

  echo "Successfully registered Vault policy '$policy_name' and OIDC role '$role_name'!"
}

# Example usage
# setup_app_security "app-01" "nebula" "org/appFactory"
