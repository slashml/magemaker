# File: scripts/update_docs.py
import argparse
import os
from datetime import datetime

def update_changelog(pr_title, pr_body, docs_dir):
    """
    Update the changelog with new PR information
    """

    print('console')
    changelog_path = os.path.join(docs_dir, 'changelog.md')
    
    # Create changelog entry
    today = datetime.now().strftime('%Y-%m-%d')
    entry = f"\n## {today}\n\n### Pull Request #{os.getenv('PR_NUMBER')}\n\n"
    entry += f"- {pr_title}\n"
    
    # If changelog doesn't exist, create it
    if not os.path.exists(changelog_path):
        os.makedirs(os.path.dirname(changelog_path), exist_ok=True)
        with open(changelog_path, 'w') as f:
            f.write("# Changelog\n")
    
    # Prepend new entry to changelog
    with open(changelog_path, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write(entry + content)

def main():
    parser = argparse.ArgumentParser(description='Update documentation based on PR')
    parser.add_argument('--pr-title', required=True, help='PR title')
    parser.add_argument('--pr-body', required=True, help='PR body')
    parser.add_argument('--docs-dir', required=True, help='Documentation directory')
    
    args = parser.parse_args()
    update_changelog(args.pr_title, args.pr_body, args.docs_dir)

if __name__ == '__main__':
    main()