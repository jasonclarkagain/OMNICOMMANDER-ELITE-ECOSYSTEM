#!/zsh
WEBHOOK_URL="https://discord.com/api/webhooks/1460465226708422783/QR-8HK65lnGKmFqO38WP7syTd0enKP_BqM12D5qEW_uTXgyCHNqFx9jZl-ifVsvs_GnC"
REPO_NAME="omnicommander_elite"

# Push to GitHub
/usr/bin/git push origin main

# If push is successful, notify Discord
if [ $? -eq 0 ]; then
  MESSAGE="🚀 **Project Update:** `$REPO_NAME` has been pushed to GitHub successfully. Environment is stable and local LLMs are synced."
  /usr/bin/curl -H "Content-Type: application/json" -X POST -d "{\"content\": \"$MESSAGE\"}" $WEBHOOK_URL
else
  echo "Push failed. Discord notification not sent."
fi
