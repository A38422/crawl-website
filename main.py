import requests
from lxml import html
from urllib.parse import urlparse
import re
import datetime

response = requests.get("https://vnexpress.net").text
tree = html.fromstring(response)
links = tree.xpath('//a/@href')

new_links = []
for link in links:
    if 'https' in link:
        new_links.append(link)
new_links = list(set(new_links))

for link in new_links:
    try:
        news = requests.get(link).text
        root = html.fromstring(news)
        title = root.xpath('//meta[@property="og:title"]/@content')
        description = root.xpath('//p[@class="description"]/text()')
        time = root.xpath('//span[@class="date"]/text()')
        content = root.xpath('//p[@class="Normal"]/text()')
        author = root.xpath('//p[@style="text-align:right;"]/strong/text()')
        timestamp = 0
        if "GMT" in str(time):
            time = re.sub(r"\(GMT\+\d+\)", "", str(time))
            time = re.findall(r'\d+', time)
            time = ' '.join(time)
            timestamp = datetime.datetime.strptime(time, "%d %m %Y %H %M").timestamp()
        content = '\n\n'.join(content)
        temp = urlparse(link)
        file_name = temp.path.split('/')[-1]
        if file_name:
            with open(file_name, 'w', encoding='UTF-8') as f:
                f.writelines(title)
                f.write("\n\n\n")
                f.write(str(timestamp) + "\n\n\n")
                f.writelines(description)
                f.write("\n\n")
                f.write(content + "\n\n")
                f.writelines(author)
    except ValueError:
        print("Invalid link " + link)
