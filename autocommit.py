#!/usr/bin/env python3
import os
import sys
import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

GITHUB_NAME = os.getenv("GITHUB_NAME", "DevOps Bot")
GITHUB_EMAIL = os.getenv("GITHUB_EMAIL", "bot@example.com")
REPO_PATH = os.getenv("REPO_PATH", str(Path(__file__).resolve().parent))
GIT_REMOTE = os.getenv("GIT_REMOTE", "origin")
GIT_BRANCH = os.getenv("GIT_BRANCH", "main")

COMMIT_TYPES = ["feat", "fix", "docs", "refactor", "style", "perf", "test", "chore"]
COMMIT_SCOPES = ["auth", "api", "core", "db", "ui", "config", "logger", "utils", "router"]

COMMIT_MESSAGES_TEMPLATE = {
    "feat": [
        "add support for {scope} caching",
        "implement asynchronous {scope} handler",
        "integrate new {scope} validation middleware",
        "extend {scope} configuration options"
    ],
    "fix": [
        "resolve null pointer exception in {scope}",
        "fix race condition during {scope} initialization",
        "correct status code handling in {scope}",
        "patch memory leak in {scope} module"
    ],
    "docs": [
        "update API specification for {scope}",
        "add inline documentation for {scope} methods",
        "refresh deployment guide for VDS",
        "document error codes in {scope}"
    ],
    "refactor": [
        "optimize database query performance in {scope}",
        "clean up legacy utility functions in {scope}",
        "restructure module layout for {scope}",
        "simplify conditional branches in {scope}"
    ],
    "style": [
        "format codebase according to PEP8 standards",
        "fix indentation and trailing whitespace in {scope}",
        "organize import statements in {scope}"
    ],
    "perf": [
        "speed up JSON serialization in {scope}",
        "reduce memory overhead in {scope} parser",
        "optimize loop execution time in {scope}"
    ],
    "test": [
        "add unit tests for edge cases in {scope}",
        "improve test coverage for {scope} service",
        "fix flaky integration test in {scope}"
    ],
    "chore": [
        "bump dependencies in {scope}",
        "update gitignore and workflow definitions",
        "cleanup temporary cache files"
    ]
}

def run_git_command(cmd, env_vars=None):
    """Run a git command in the repository path."""
    full_env = os.environ.copy()
    if env_vars:
        full_env.update(env_vars)
    
    result = subprocess.run(
        cmd,
        cwd=REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=full_env
    )
    if result.returncode != 0:
        print(f"Git error on command {' '.join(cmd)}: {result.stderr.strip()}")
    return result.returncode == 0, result.stdout.strip()

def setup_git_identity():
    """Ensure git user name and email are configured locally."""
    run_git_command(["git", "config", "user.name", GITHUB_NAME])
    run_git_command(["git", "config", "user.email", GITHUB_EMAIL])

def generate_commit_message():
    """Generate a random Conventional Commit message."""
    c_type = random.choice(COMMIT_TYPES)
    c_scope = random.choice(COMMIT_SCOPES)
    template = random.choice(COMMIT_MESSAGES_TEMPLATE[c_type])
    msg = template.format(scope=c_scope)
    return f"{c_type}({c_scope}): {msg}"

def update_activity_log(timestamp_str=None):
    """Append a timestamp entry to activity_log.txt."""
    log_file = Path(REPO_PATH) / "activity_log.txt"
    ts = timestamp_str or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"Activity recorded at: {ts}\n")

def make_commit(commit_date=None):
    """Make a single commit with optional custom date."""
    setup_git_identity()
    msg = generate_commit_message()
    
    ts = commit_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_activity_log(ts)
    
    success, _ = run_git_command(["git", "add", "activity_log.txt"])
    if not success:
        return False

    env = {}
    if commit_date:
        # ISO format or standard git date format: "YYYY-MM-DD HH:MM:SS"
        env["GIT_AUTHOR_DATE"] = commit_date
        env["GIT_COMMITTER_DATE"] = commit_date

    success, _ = run_git_command(["git", "commit", "-m", msg], env_vars=env)
    if success:
        print(f"[{ts}] Committed: {msg}")
    return success

def perform_regular_run():
    """Execute standard scheduled run (2-6 commits)."""
    os.makedirs(REPO_PATH, exist_ok=True)
    setup_git_identity()
    
    # Random number of commits between 2 and 6
    num_commits = random.randint(2, 6)
    print(f"Starting regular run: generating {num_commits} commits.")
    
    successful = 0
    for _ in range(num_commits):
        if make_commit():
            successful += 1
        # Small random delay between commits in same batch
        # (simulating fast typing or sequential script tasks)
    
    if successful > 0:
        print(f"Pushing {successful} commits to {GIT_REMOTE}/{GIT_BRANCH}...")
        success, out = run_git_command(["git", "push", GIT_REMOTE, GIT_BRANCH])
        if success:
            print("Push successful.")
        else:
            print(f"Push failed: {out}")

def perform_backfill(days=90, min_commits_per_day=1, max_commits_per_day=4):
    """Backfill commit history across past N days."""
    os.makedirs(REPO_PATH, exist_ok=True)
    setup_git_identity()
    
    print(f"Starting backfill mode for the past {days} days...")
    end_date = datetime.now()
    
    total_created = 0
    for i in range(days, -1, -1):
        current_date = end_date - timedelta(days=i)
        
        # Decide whether to skip some days randomly to mimic natural human behavior (e.g. weekends/holidays)
        if current_date.weekday() >= 5 and random.random() < 0.3:
            continue
            
        num_commits = random.randint(min_commits_per_day, max_commits_per_day)
        
        for _ in range(num_commits):
            # Random hour between 9 AM and 11 PM
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_dt = current_date.replace(hour=hour, minute=minute, second=second)
            date_str = commit_dt.strftime("%Y-%m-%d %H:%M:%S")
            
            if make_commit(commit_date=date_str):
                total_created += 1

    print(f"Backfill complete. Total {total_created} historical commits created.")
    print(f"Pushing all backfilled commits to {GIT_REMOTE}/{GIT_BRANCH}...")
    success, out = run_git_command(["git", "push", GIT_REMOTE, GIT_BRANCH])
    if success:
        print("Backfill push successful.")
    else:
        print(f"Backfill push failed: {out}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--backfill":
        days_arg = 90
        if len(sys.argv) > 2:
            try:
                days_arg = int(sys.argv[2])
            except ValueError:
                pass
        perform_backfill(days=days_arg)
    else:
        perform_regular_run()
