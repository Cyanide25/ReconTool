import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style

class ActiveRecon:
    def __init__(self,domain="uber.com"):
        self.domain = domain

    def EnumerateWordlist(self):
        w = open('./Wordlists/DNSlist.txt','r')
        wordlist = w.read().split('\n')
        Subdomains = []

        for i in range(1000):
            sub = str(wordlist[i])+'.'+self.domain
            Subdomains.append(sub)        
        Alive = []
        NotAlive = []

        for i in Subdomains:
            try:
                response = requests.head(f"http://{i}")
                if response.status_code:
                    Alive.append(i)
                    print(f"{Fore.GREEN}{i}{Style.RESET_ALL}")
                else:
                    NotAlive.append(i)
            except Exception as e:
                NotAlive.append(i)
        return Alive, NotAlive

class WebCrawling:
    def __init__(self,domain):
        self.domain = domain

    def crawl(self):
        print("--------Starting Web Crawling--------")
        with open("./Output/WebCrawl.txt","w") as w:    
            url = f"http://{self.domain}"
            #RegexPattern = rf'href=["\'](https?://[^"\'>]*{re.escape(self.domain)}[^"\'>]*)'
            RegexPattern = rf'href=["\'](https?://(?:[^"/]*\.)?{re.escape(self.domain)}/[^"\'>]*)'
            response = requests.get(url)
            AllUrls = []
            if response.status_code == 200:
                ResponseContent = response.text
                alinks = re.findall(RegexPattern, ResponseContent) 
                AllUrls = list(set(alinks))
                for u in AllUrls:
                    w.write(u+'\n')
                    print(u)
                
            for u in AllUrls:
                response = requests.get(u)
                if response.status_code == 200:
                    ResponseContent = response.text
                    urls = re.findall(RegexPattern, ResponseContent) 
                    for n in urls:
                        if n not in AllUrls:
                            AllUrls.append(n)
                            print(n)
                            w.write(n+'\n')
                
        return AllUrls
class GetScreenShot:
    def __init__(self,domains):
        self.domains = domains
    def GetSShot(self):
        print("--------Taking Screenshots--------")
        dirpath = "./Screenshots/"
        if os.path.exists(dirpath) == False:
            os.mkdir(dirpath)

        for f in os.listdir(dirpath):
            f = os.path.join(dirpath, f)
            os.remove(f)

        for d in self.domains:
            try:
                ChromeOptions = Options()
                ChromeOptions.add_argument("--headless=new")
                ChromeOptions.add_argument("--disable-extensions")
                ChromeOptions.add_argument('--log-level=3')
                driver = webdriver.Chrome(options=ChromeOptions)
                driver.set_page_load_timeout(30)
                driver.get('http://'+d)
                driver.save_screenshot(dirpath +d+'.png')
                print(f"took screenshot for {d}")
                driver.quit()
            except:
                print(f"couldn't take a screenshot for {d}")

def main(domain):
    print("\n---------Starting Active Scan----------")
    print(f"\nAlive subdomains for {domain} in wordlist:")

    DomainRecon = ActiveRecon(domain)
    Alive,NotAlive = DomainRecon.EnumerateWordlist()

    print(f"\nNot alive subdomains for {domain} in wordlist:")
    for d in NotAlive:
        print(f"{Fore.RED}{d}{Style.RESET_ALL}")

    Crawl = WebCrawling(domain)
    URLS = Crawl.crawl()
    
    ss = GetScreenShot(Alive)
    ss.GetSShot()

if __name__ == "__main__":
 
    domain = input("Please enter your domain: ")
    main(domain)

    