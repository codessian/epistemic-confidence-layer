#!/usr/bin/env bash
set -euo pipefail
# Apply branch protection using GitHub CLI
# Usage: ./ops/branch_protection_gh_cli.sh owner repo
OWNER="${1:-$GITHUB_REPOSITORY_OWNER}"
REPO="${2:-$(basename "$GITHUB_REPOSITORY")}"
gh api \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${OWNER}/${REPO}/branches/main/protection" \
  --input ops/branch_protection.json
echo "Applied branch protection to ${OWNER}/${REPO}@main"