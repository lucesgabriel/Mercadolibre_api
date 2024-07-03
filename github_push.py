import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error: {error.decode('utf-8')}")
        return False
    return True

def get_current_branch():
    process = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode('utf-8').strip()

def remote_exists():
    process = subprocess.Popen(["git", "remote"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return "origin" in output.decode('utf-8')

def push_to_github(repo_name, commit_message):
    current_branch = get_current_branch()
    remote_url = f"https://github.com/lucesgabriel/{repo_name}.git"
    
    commands = [
        "git init",
        "git add .",
        f'git commit -m "{commit_message}"'
    ]

    if remote_exists():
        commands.append(f"git remote set-url origin {remote_url}")
    else:
        commands.append(f"git remote add origin {remote_url}")

    commands.append(f"git push -u origin {current_branch}:{current_branch}")

    for command in commands:
        if not run_command(command):
            print(f"Failed at command: {command}")
            return False
    
    print("Successfully pushed to GitHub!")
    return True

if __name__ == "__main__":
    repo_name = "Mercadolibre_api"
    commit_message = "Commit inicial: MercadoLibre Product Tracker"
    push_to_github(repo_name, commit_message)