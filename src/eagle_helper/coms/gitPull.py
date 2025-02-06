import os
import json
import time
import subprocess
import eagle_helper

def git_pull(repo_url, repo_name=None, branch="main", force=False):
    """Pull a git repository with time-based caching and branch support
    
    Args:
        repo_url (str): URL of the git repository to pull
        repo_name (str, optional): Name of the repository folder. Defaults to last part of URL
        branch (str): Branch to checkout/pull. Defaults to "main"
        force (bool): Force pull regardless of last pull time
    """
    # Determine repo folder name
    if repo_name is None:
        repo_name = repo_url.split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
    
    # Paths
    os.makedirs(eagle_helper.HOME_DIR, exist_ok=True)
    repo_dir = os.path.join(eagle_helper.HOME_DIR, repo_name)
    config_path = os.path.join(eagle_helper.HOME_DIR, "config.json")
    
    # Initialize config if it doesn't exist
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            json.dump({"repos": {}}, f)
    
    # Load config
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Initialize repo config if it doesn't exist
    if repo_name not in config["repos"]:
        config["repos"][repo_name] = {"last_pull": 0, "branch": branch}
    
    # Check if repo exists
    if os.path.exists(repo_dir):
        # Get folder modification time
        folder_mtime = os.path.getmtime(repo_dir)
        # Update config if folder is newer than last pull
        if folder_mtime > config["repos"][repo_name].get("last_pull", 0):
            config["repos"][repo_name]["last_pull"] = folder_mtime
            with open(config_path, "w") as f:
                json.dump(config, f)
    
    # Check if we should skip pull
    if not force and time.time() - config["repos"][repo_name].get("last_pull", 0) < 86400:  # 24 hours
        return
    
    # Ensure git is installed
    if not eagle_helper.GIT_IS_INSTALLED:
        raise RuntimeError("Git is not installed")
    
    # Clone or pull the repository
    if not os.path.exists(repo_dir):
        subprocess.run(["git", "clone", "--branch", branch, repo_url, repo_dir], check=True)
    else:
        # Check if branch needs to be changed
        current_branch = subprocess.run(
            ["git", "-C", repo_dir, "branch", "--show-current"],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        if current_branch != branch:
            subprocess.run(["git", "-C", repo_dir, "checkout", branch], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Update last pull time and branch in config
    config["repos"][repo_name]["last_pull"] = time.time()
    config["repos"][repo_name]["branch"] = branch
    with open(config_path, "w") as f:
        json.dump(config, f)


