# Set up project info
import subprocess


def get_git_root():
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()


repo_root = get_git_root()
project_name = "example_project"
project_path = f"{repo_root}/scrape_pipelines/{project_name}"
scripts_path = f"{repo_root}/scripts"
