import os
import requests
import json
import subprocess

def get_repo_info(repo_owner):
    token = os.environ['GITHUB_TOKEN']
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        f'https://api.github.com/repos/{repo_owner}/MMAC',
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    return None

def init_and_push(repo_owner, token):
    # Configure git
    subprocess.run(['git', 'config', '--global', 'user.name', 'MMAC Bot'], check=True)
    subprocess.run(['git', 'config', '--global', 'user.email', 'mmac-bot@users.noreply.github.com'], check=True)
    
    # Remove any existing git folder
    if os.path.exists('.git'):
        import shutil
        shutil.rmtree('.git')
    
    commands = [
        ['git', 'init'],
        ['git', 'add', '.'],
        ['git', 'commit', '-m', 'Initial commit'],
        ['git', 'branch', '-M', 'main'],
        ['git', 'remote', 'add', 'origin', f'https://x-access-token:{token}@github.com/{repo_owner}/MMAC.git'],
        ['git', 'push', '-u', 'origin', 'main', '--force']  # Force push to overwrite
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Executed {cmd[0]}: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute {cmd[0]}: {e.stderr}")
            return False
    return True

def create_release(repo_owner, tag_name="v1.0.0"):
    token = os.environ['GITHUB_TOKEN']
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    release_data = {
        'tag_name': tag_name,
        'name': 'MMAC Initial Release',
        'body': '''# MMAC Initial Release

Features:
- Customizable click intervals (milliseconds to hours)
- Multiple click types (Single, Double, Triple)
- Different mouse buttons (Left, Right, Middle)
- Fixed position or current cursor position clicking
- Hotkey support (F6 to Start/Stop, F7 to Stop)''',
        'draft': False,
        'prerelease': False
    }
    
    response = requests.post(
        f'https://api.github.com/repos/{repo_owner}/MMAC/releases',
        headers=headers,
        data=json.dumps(release_data)
    )
    
    if response.status_code != 201:
        print(f"Failed to create release: {response.status_code}")
        print(response.json())
        return None
        
    release = response.json()
    
    # Upload asset
    asset_path = 'dist/MMAC'
    if not os.path.exists(asset_path):
        print(f"Asset not found: {asset_path}")
        return None
        
    with open(asset_path, 'rb') as f:
        asset_data = f.read()
        
    upload_url = release['upload_url'].replace('{?name,label}', '')
    headers['Content-Type'] = 'application/octet-stream'
    
    response = requests.post(
        f"{upload_url}?name=MMAC",
        headers=headers,
        data=asset_data
    )
    
    if response.status_code != 201:
        print(f"Failed to upload asset: {response.status_code}")
        print(response.json())
        return None
        
    print("Release created successfully!")
    return release

def main():
    # Get user info
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("GITHUB_TOKEN not found in environment variables")
        return
        
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    user_response = requests.get('https://api.github.com/user', headers=headers)
    if user_response.status_code != 200:
        print("Failed to get user information")
        print(user_response.json())
        return
    
    repo_owner = user_response.json()['login']
    
    # Check if repository exists
    repo = get_repo_info(repo_owner)
    if not repo:
        print("Repository not found or not accessible")
        return
        
    # Initialize and push
    if not init_and_push(repo_owner, token):
        return
        
    # Create release
    release = create_release(repo_owner)
    if not release:
        return
        
    print(f"Code pushed successfully!")
    print(f"Release created: {release['html_url']}")

if __name__ == "__main__":
    main()
