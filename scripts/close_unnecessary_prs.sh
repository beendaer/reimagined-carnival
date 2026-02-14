#!/usr/bin/env bash
set -euo pipefail

# Script to close unnecessary PRs created by mistake
# These PRs (108-112) contain no code changes and were created in response to STOP directives

REPO="beendaer/reimagined-carnival"
PRS_TO_CLOSE=(108 109 110 111 112)

echo "🧹 Closing unnecessary PRs in ${REPO}..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed."
    echo "   Install it from: https://cli.github.com/"
    echo ""
    echo "   Or close PRs manually via GitHub web UI:"
    for pr in "${PRS_TO_CLOSE[@]}"; do
        echo "   - https://github.com/${REPO}/pull/${pr}"
    done
    exit 1
fi

# Check if authenticated with gh
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI."
    echo "   Run: gh auth login"
    exit 1
fi

echo "ℹ️  This will close the following PRs:"
for pr in "${PRS_TO_CLOSE[@]}"; do
    echo "   - PR #${pr}"
done
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled."
    exit 0
fi

echo ""
echo "Closing PRs..."
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0

for pr in "${PRS_TO_CLOSE[@]}"; do
    echo -n "📝 Closing PR #${pr}... "
    if gh pr close "${pr}" -R "${REPO}" -c "Closing unnecessary PR created by mistake (no code changes)" 2>/dev/null; then
        echo "✅ Done"
        ((SUCCESS_COUNT++))
    else
        echo "⚠️  Failed (may already be closed)"
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Successfully closed: ${SUCCESS_COUNT}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo "⚠️  Failed/Already closed: ${FAIL_COUNT}"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Optional: Delete branches
echo "Would you also like to delete the associated branches?"
echo "(This will permanently remove: codex/stop-work-now, codex/stop-process-now,"
echo " codex/stop-button-functionality, codex/update-documentation-formatting,"
echo " codex/stop-all-work-on-repo)"
echo ""
read -p "Delete branches? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Deleting branches..."
    
    BRANCHES=(
        "codex/stop-work-now"
        "codex/stop-process-now"
        "codex/stop-button-functionality"
        "codex/update-documentation-formatting"
        "codex/stop-all-work-on-repo"
    )
    
    for branch in "${BRANCHES[@]}"; do
        echo -n "🗑️  Deleting ${branch}... "
        if git push origin --delete "${branch}" 2>/dev/null; then
            echo "✅ Done"
        else
            echo "⚠️  Failed (may not exist)"
        fi
    done
    
    echo ""
    echo "✅ Branch cleanup complete!"
else
    echo "ℹ️  Branches not deleted. You can delete them later if needed."
fi

echo ""
echo "🎉 Cleanup complete!"
echo ""
echo "Verify at: https://github.com/${REPO}/pulls?q=is%3Apr+is%3Aclosed"
