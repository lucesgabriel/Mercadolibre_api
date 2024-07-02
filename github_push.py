import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error: {error.decode('utf-8')}")
        return False
    return True

def push_to_github(repo_name, commit_message):
    commands = [
        "git init",
        "git add .",
        f'git commit -m "{commit_message}"',
        f"git remote add origin https://github.com/lucesgabriel/{repo_name}.git",
        "git push -u origin main"
    ]

    for command in commands:
        if not run_command(command):
            print(f"Failed at command: {command}")
            return False
    
    print("Successfully pushed to GitHub!")
    return True

if __name__ == "__main__":
    repo_name = "mercadolibre-product-tracker"
    commit_message = "Commit inicial: MercadoLibre Product Tracker"
    push_to_github(repo_name, commit_message)