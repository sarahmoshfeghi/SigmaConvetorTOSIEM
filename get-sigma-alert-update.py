import re
from time import sleep
import requests
from bs4 import BeautifulSoup
import pymongo
import urllib.request
import os
def ioc_reporter():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['Rules']
    web_repo_urls = ['https://github.com/SigmaHQ/sigma/tree/master/rules/web/product/apache',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/web/product/nginx',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/web/webserver_generic',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/category/antivirus',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/category/database',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/file/file_access',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/create_remote_thread',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/network_connection',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/process_tampering',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/powershell/powershell_script',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/powershell/powershell_module',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/powershell/powershell_classic',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/process_creation',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/registry/registry_add',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/registry/registry_delete',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/registry/registry_set',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/sysmon',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/wmi_event',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/windows/process_access',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/auditd',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/builtin/auth',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/builtin/cron',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/builtin/sshd',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/builtin/sudo',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/builtin/syslog',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/file_event',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/network_connection',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/linux/process_creation',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/network/firewall',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/network/dns',
                     'https://github.com/SigmaHQ/sigma/tree/master/rules/network/zeek']

    base_web_url = 'https://raw.githubusercontent.com'
    for web_repo_url in web_repo_urls:
        response = requests.get(web_repo_url, allow_redirects=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'})
        sleep(5)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser', from_encoding="iso-8859-1")
        results = soup.find_all('a', attrs={'class': 'Link--primary'})
        regex = r'"tree":{"items":\[{"name":'
        for result in results:
            Title = result['title']
            Link = result['href']
            if 'rules/web' in web_repo_url:
                mycol = mydb['web']
            elif 'category/antivirus' in web_repo_url:
                mycol = mydb['antivirus']
            elif 'rules/linux' in web_repo_url:
                mycol = mydb['linux']
            elif 'rules/windows' in web_repo_url:
                mycol = mydb['windows']
            elif 'category/database' in web_repo_url:
                mycol = mydb['database']
            elif 'rules/network' in web_repo_url:
                mycol = mydb['network']
            res_j={}
            res_j['Title'] = Title
            url = re.sub('/blob/', '/', Link)
            url = base_web_url + url
            res_j['url'] = url
            res_j['Category'] = mycol.name
            category = mycol.find_one({'Category': mycol.name})
            # print(category['Category'])
            # print(mycol.name)
            if mycol.count_documents({'Title': Title}, limit=1) != 0 and category['Category'] == mycol.name :
                # print('return')
                continue
            print(res_j)
            fullfilename = os.path.join('/pathtotheyamlfile/yamlfile', Title)
            mycol.insert_one(res_j)
            try:
                urllib.request.urlretrieve(url,fullfilename)
            except:
                continue

