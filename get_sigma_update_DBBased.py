import os
import re
import requests
import pymongo
import urllib.request
from time import sleep
from bs4 import BeautifulSoup

def fetch_updated_yaml_files():
    """
    Fetch updated YAML files from the Sigma repository and store metadata in MongoDB.
    """
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = mongo_client['Rules']
    base_url = 'https://raw.githubusercontent.com'
    
    repo_urls = [
        'https://github.com/SigmaHQ/sigma/tree/master/rules/web/product/apache',
        'https://github.com/SigmaHQ/sigma/tree/master/rules/web/product/nginx',
        'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/process_creation',
        'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/network_connection',
        'https://github.com/SigmaHQ/sigma/tree/master/rules/network/firewall'
    ]
    
    for repo_url in repo_urls:
        response = requests.get(repo_url, headers={'User-Agent': 'Mozilla/5.0'})
        sleep(5)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('a', {'class': 'Link--primary'})
        
        for result in results:
            title = result['title']
            link = result['href']
            url = base_url + re.sub('/blob/', '/', link)
            
            # Determine category
            if 'rules/web' in repo_url:
                collection = database['web']
            elif 'rules/windows' in repo_url:
                collection = database['windows']
            elif 'rules/linux' in repo_url:
                collection = database['linux']
            elif 'rules/network' in repo_url:
                collection = database['network']
            else:
                collection = database['misc']
            
            # Check if already exists in MongoDB
            if collection.count_documents({'Title': title}, limit=1) != 0:
                continue  # Skip if already stored
            
            # Store metadata
            metadata = {'Title': title, 'url': url, 'Category': collection.name}
            collection.insert_one(metadata)
            print(f"Stored metadata: {metadata}")
            
            # Download YAML file
            output_dir = f"./yaml_files/{collection.name}"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, title)
            try:
                urllib.request.urlretrieve(url, output_path)
                print(f"Downloaded: {title}")
            except Exception as e:
                print(f"Failed to download {title}: {e}")

if __name__ == "__main__":
    fetch_updated_yaml_files()
