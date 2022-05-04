import requests
from bs4 import BeautifulSoup
import re


class Crawler:

    def __init__(self, root_url):
        self.root_url = root_url
        self.authority = self.parse_authority()
        self.link_list = []
        self.link_tree = {}

    def parse_authority(self):
        parsed = re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*['
                            r'\w\-\@?^=%&/~\+#])?', self.root_url)
        return f"{parsed[0][0]}://{parsed[0][1]}"

    def recursive_crawl(self, url):
        response = requests.get(url)
        link_list = []
        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('a'):
            link = item.get('href')
            if link not in link_list and link is not None:
                if not link.__contains__(self.authority) and not link.__contains__("http"):
                    link = f"{self.authority}{link}"
                link_list.append(link)
        self.link_tree.update({url: link_list})

    def start_crawl(self):
        self.recursive_crawl(self.root_url)

    def single_crawl(self, url):
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('a'):
            link = item.get('href')
            if link not in self.link_list:
                self.link_list.append(link)

    def print_all_links(self):
        for parent, children in self.link_tree.items():
            print(f"{parent}:\n")
            print('\n'.join([str(Child) for Child in [*children]]))



if __name__ == '__main__':
    spider = Crawler("http://192.168.139.133/twiki/bin/view/Main/WebHome")

    spider.start_crawl()
    spider.print_all_links()

