#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def main():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        capture_output=True,
        text=True
    )
    
    changed_files = result.stdout.strip().split('\n')
    txt_files_changed = [f for f in changed_files if f.startswith('data/') and f.endswith('.txt')]
    
    if not txt_files_changed:
        sys.exit(0)
    
    print("Wordlist files detected, checking for duplicates...")
    print()
    
    result = subprocess.run(
        ['python', 'scripts/check_duplicates.py'],
        capture_output=False
    )
    
    if result.returncode != 0:
        print()
        print("=" * 60)
        print("COMMIT BLOCKED: Duplicates detected!")
        print("=" * 60)
        print()
        print("Please remove the duplicates and try committing again.")
        print("To bypass this check (not recommended), use: git commit --no-verify")
        sys.exit(1)
    
    print()
    print("No duplicates found. Proceeding with commit...")
    sys.exit(0)


if __name__ == '__main__':
    main()
