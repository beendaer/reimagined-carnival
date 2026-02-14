#!/usr/bin/env python3
"""
Script to close unnecessary PRs created by mistake.

These PRs (108-112) contain no code changes and were created in response
to STOP directives. This script uses the GitHub API to close them.

Requirements:
    pip install requests

Usage:
    # Set GitHub token
    export GITHUB_TOKEN="your_personal_access_token"
    
    # Run script
    python scripts/close_unnecessary_prs.py
"""

import os
import sys
import requests
from typing import List, Tuple


REPO_OWNER = "beendaer"
REPO_NAME = "reimagined-carnival"
PRS_TO_CLOSE = [108, 109, 110, 111, 112]
CLOSE_COMMENT = "Closing unnecessary PR created by mistake (no code changes)"


def get_github_token() -> str:
    """Get GitHub token from environment."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN environment variable not set.")
        print("   Create a token at: https://github.com/settings/tokens")
        print("   Then run: export GITHUB_TOKEN='your_token'")
        sys.exit(1)
    return token


def close_pr(pr_number: int, token: str) -> Tuple[bool, str]:
    """
    Close a pull request via GitHub API.
    
    Args:
        pr_number: PR number to close
        token: GitHub personal access token
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # First, add a comment
    comment_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"
    comment_data = {"body": CLOSE_COMMENT}
    
    try:
        comment_response = requests.post(comment_url, json=comment_data, headers=headers)
        if comment_response.status_code not in (200, 201):
            return False, f"Failed to add comment: {comment_response.status_code}"
    except Exception as e:
        return False, f"Failed to add comment: {str(e)}"
    
    # Then, close the PR
    pr_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"
    pr_data = {"state": "closed"}
    
    try:
        response = requests.patch(pr_url, json=pr_data, headers=headers)
        if response.status_code == 200:
            return True, "Closed successfully"
        elif response.status_code == 404:
            return False, "PR not found (may already be closed)"
        else:
            return False, f"Failed: HTTP {response.status_code}"
    except Exception as e:
        return False, f"Failed: {str(e)}"


def main():
    """Main function."""
    print(f"🧹 Closing unnecessary PRs in {REPO_OWNER}/{REPO_NAME}...")
    print()
    
    token = get_github_token()
    
    print("ℹ️  This will close the following PRs:")
    for pr in PRS_TO_CLOSE:
        print(f"   - PR #{pr}")
    print()
    
    response = input("Continue? (y/N): ").strip().lower()
    if response not in ("y", "yes"):
        print("❌ Cancelled.")
        sys.exit(0)
    
    print()
    print("Closing PRs...")
    print()
    
    success_count = 0
    fail_count = 0
    
    for pr in PRS_TO_CLOSE:
        print(f"📝 Closing PR #{pr}... ", end="", flush=True)
        success, message = close_pr(pr, token)
        
        if success:
            print(f"✅ {message}")
            success_count += 1
        else:
            print(f"⚠️  {message}")
            fail_count += 1
    
    print()
    print("━" * 40)
    print(f"✅ Successfully closed: {success_count}")
    if fail_count > 0:
        print(f"⚠️  Failed/Already closed: {fail_count}")
    print("━" * 40)
    print()
    
    print("🎉 Cleanup complete!")
    print()
    print(f"Verify at: https://github.com/{REPO_OWNER}/{REPO_NAME}/pulls?q=is%3Apr+is%3Aclosed")


if __name__ == "__main__":
    main()
