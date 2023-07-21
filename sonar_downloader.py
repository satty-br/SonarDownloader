import os
import requests
import argparse
from colorama import init, Fore

# Initialize colorama for colored text
init(autoreset=True)

# ASCII Art for the project name
project_name_ascii = r"""
  ___|                         __ \                       |                 |           
\___ \   _ \  __ \   _` |  __| |   |  _ \\ \  \   / __ \  |  _ \   _` |  _` |  _ \  __| 
      | (   | |   | (   | |    |   | (   |\ \  \ /  |   | | (   | (   | (   |  __/ |    
_____/ \___/ _|  _|\__,_|_|   ____/ \___/  \_/\_/  _|  _|_|\___/ \__,_|\__,_|\___|_|    
"""
satty_text = "                                                                        by Satty.com.br"

SONARQUBE_URL = 'https://sonarcloud.io/api/'

headers = {}

def get_orgs():
    response = requests.get(f"{SONARQUBE_URL}organizations/search?member=true", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("organizations", [])
    if response.status_code == 401:
        print(f"{Fore.RED}Token not valid")
    else:
        print(f"{Fore.RED}Failed to fetch projects: {response.status_code} - {response.json().get('errors')}")
    return []

def get_projects(org):
    projects = []
    page = 1

    while True:
        response = requests.get(f"{SONARQUBE_URL}components/search_projects?p={page}&organization={org}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            projects.extend(data.get('components', []))
            if data.get('paging', {}).get('pageIndex') >= data.get('paging', {}).get('total'):
                break
            page += 1
        else:
            print(f"{Fore.RED}Failed to fetch projects: {response.status_code} - {response.json().get('errors')}")
            break

    return projects

def download_project_files(project_key,base_proj_folder):

    file_tree_response = requests.get(f"{SONARQUBE_URL}measures/component_tree?component={project_key}&metricKeys=files", headers=headers)

    if file_tree_response.status_code == 200:
        file_tree_data = file_tree_response.json()
        files = file_tree_data.get('components',{})
        for file in files:
            file_path = file.get('path')
            file_dir = os.path.dirname(file_path)
            dir_path = os.path.join(base_proj_folder, file_dir)
            if file_dir and not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if file.get('qualifier',"") == 'DIR':
                continue

            file_response = requests.get(f"{SONARQUBE_URL}sources/raw?key={project_key}:{file_path}", headers=headers)
            if file_response.status_code == 200:
                with open(os.path.join(base_proj_folder, file_path), 'wb') as f:
                    f.write(file_response.content)
            else:
                print(f"{Fore.RED}Failed to download {file_path}: {file_response.status_code} - {file_response.json().get('errors')}")

    else:
        print(f"{Fore.RED}Failed to fetch file tree for project {project_key}: {file_tree_response.status_code} - {file_tree_response.json().get('errors')}")

def download_projects(projects,base_org_folder):
    for project in projects:
        project_key = project['key']
        project_name = project['name']
        base_proj_folder = f"{base_org_folder}/{project_name}/"
        if not os.path.exists(base_proj_folder):
                os.makedirs(base_proj_folder)
        print(f"{Fore.YELLOW}Downloading {project_name}...")
        download_project_files(project_key,base_proj_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, default=None, help='Sonar token.')
    parser.add_argument('--org', type=str, default=None, help='Only for a specfic org.')
    parser.add_argument('--url', type=str, default=None, help='Sonar Url  defaul = https://sonarcloud.io/api/.')
    args = parser.parse_args()
    SONAR_API_KEY = args.key
    if not SONAR_API_KEY:
        SONAR_API_KEY = os.getenv('SONAR_API_KEY')
    url =args.url
    if url:
        if not url.endswith('/api/'):
            url += '/api/'
        SONARQUBE_URL = url

    headers = {'Authorization': f'Bearer {SONAR_API_KEY}'}
    print(f"{Fore.GREEN}{project_name_ascii}")
    print(f"{Fore.BLUE}{satty_text}")
    if not SONAR_API_KEY:
        print(f"{Fore.RED}Please set the 'SONAR_API_KEY' environment or use --key=yoursonarkey  with your SonarQube API key.")
    else:
        if not os.path.exists('projects'):
            os.makedirs('projects')

        for org in get_orgs():
            if args.org and args.org != org["key"]:
                continue
            base_org_folder = f'projects/{org["key"]}'
            if not os.path.exists(base_org_folder):
                os.makedirs(base_org_folder)
            projects = get_projects(org["key"])
            download_projects(projects,base_org_folder)
