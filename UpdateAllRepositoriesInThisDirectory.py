#!/usr/bin/env python3
"""
Auto-update all git repositories in a directory.
Usage: python update_repos.py [directory_path]
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


def is_git_repo(path: Path) -> bool:
    """Check if a directory is a git repository."""
    return (path / '.git').exists() and (path / '.git').is_dir()


def find_git_repos(base_dir: Path) -> List[Path]:
    """Find all git repositories in the base directory."""
    repos = []
    try:
        for item in base_dir.iterdir():
            if item.is_dir() and is_git_repo(item):
                repos.append(item)
    except PermissionError as e:
        print(f"[!] Permission denied: {base_dir}")
    return repos


def update_repo(repo_path: Path) -> Tuple[bool, str]:
    """
    Update a git repository using git pull.
    Returns (success, message) tuple.
    """
    try:
        result = subprocess.run(
            ['git', 'pull'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if 'Already up to date' in output or 'Already up-to-date' in output:
                return True, "Already up to date"
            else:
                return True, output.split('\n')[0]
        else:
            return False, result.stderr.strip().split('\n')[0]
            
    except subprocess.TimeoutExpired:
        return False, "Timeout (>60s)"
    except Exception as e:
        return False, str(e)


def main():
    # Determine target directory
    if len(sys.argv) > 1:
        base_dir = Path(sys.argv[1])
    else:
        base_dir = Path.cwd()
    
    # Validate directory
    if not base_dir.exists():
        print(f"[x] Error: Directory '{base_dir}' does not exist")
        sys.exit(1)
    
    if not base_dir.is_dir():
        print(f"[x] Error: '{base_dir}' is not a directory")
        sys.exit(1)
    
    print(f"─── Scanning for git repositories in: {base_dir.absolute()}\n")
    
    repos = find_git_repos(base_dir)
    
    if not repos:
        print("No git repositories found.")
        sys.exit(0)
    
    print(f"Found {len(repos)} repository/repositories\n")
    print("═" * 70)
    
    success_count = 0
    fail_count = 0
    
    for repo in sorted(repos):
        repo_name = repo.name
        print(f"\n╭─ {repo_name}")
        print(f"│  Path: {repo}")
        
        success, message = update_repo(repo)
        
        if success:
            print(f"│  -> {message}")
            success_count += 1
        else:
            print(f"│  ✗ Failed: {message}")
            fail_count += 1
    
    print("\n" + "═" * 70)
    print(f"\n╭─ Summary ──────────────────────────────────────────────")
    print(f"│  Total:   {len(repos)}")
    print(f"│  Success: {success_count}")
    print(f"│  Failed:  {fail_count}")
    print("╰─────────────────────────────────────────────────────────")


if __name__ == "__main__":
    main()
