import os
import git  # type: ignore

def clone_repositories(source_repo_url, dest_repo_url, source_clone_dir, dest_clone_dir, pat, username):
    if not os.path.exists(source_clone_dir):
        git.Repo.clone_from(source_repo_url, source_clone_dir)
        print("Source repository cloned.")
    else:
        print("Source repository already exists. Skipping clone.")

    if not os.path.exists(dest_clone_dir):
        dest_repo_url_with_auth = dest_repo_url.replace("https://", f"https://{username}:{pat}@")
        git.Repo.clone_from(dest_repo_url_with_auth, dest_clone_dir)
        print("Destination repository cloned.")
    else:
        print("Destination repository already exists. Skipping clone.")

if __name__ == "__main__":
    source_repo_url = "https://github.com/venkatesh-reddy-prog/Template_Repo"
    source_clone_dir = os.path.expanduser("~/Clone_Repo/Template_Repo")
    
    dest_repo_url = os.environ.get("DEST_REPO_URL")
    pat = os.environ.get("GITHUB_PAT")
    username = os.environ.get("GITHUB_USERNAME")

    if not dest_repo_url or not pat or not username:
        print("Please set the environment variables DEST_REPO_URL, GITHUB_PAT, and GITHUB_USERNAME.")
        exit(1)

    dest_clone_dir = os.path.expanduser("~/Clone_Repo/Demo1-Folder")

    clone_repositories(source_repo_url, dest_repo_url, source_clone_dir, dest_clone_dir, pat, username)
