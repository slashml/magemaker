# File: scripts/update_docs.py
import argparse
import os
import shutil
from datetime import datetime

def update_quickstart(docs_dir):
    """
    Update the quick-start.mdx file with content from new-quick-start.mdx
    """
    # Define paths
    source_quickstart = os.path.join('.github', 'scripts', 'new-quick-start.mdx')
    target_quickstart = os.path.join(docs_dir, 'quick-start.mdx')
    
    # Ensure the source file exists
    if not os.path.exists(source_quickstart):
        raise FileNotFoundError(f"Source file {source_quickstart} not found")
    
    # Copy the new quick start guide
    shutil.copy2(source_quickstart, target_quickstart)
    print(f"Updated {target_quickstart} with new content")

def main():
    parser = argparse.ArgumentParser(description='Update documentation based on PR')
    parser.add_argument('--pr-title', required=True, help='PR title')
    parser.add_argument('--pr-body', required=True, help='PR body')
    parser.add_argument('--docs-dir', required=True, help='Documentation directory')
    
    args = parser.parse_args()
    
    try:
        update_quickstart(args.docs_dir)
        print("Documentation update completed successfully")
    except Exception as e:
        print(f"Error updating documentation: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()