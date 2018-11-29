import requests
import re

def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

if __name__ == '__main__':
    url = "http://jmjh.miit.gov.cn/newsInfoWebMessage.action?newsId=12829621&moduleId=1062"
    html = get_page(url)
    pattern = re.compile('<div id="con_con" class="con_con">(.*?)</div>',re.S)
    rs = re.findall(pattern, html)
    print(len(rs))
    for r in rs:
        if r != None:
            print(r.strip())

