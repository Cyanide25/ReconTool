import requests
import re
from colorama import Fore, Style
from tld import get_tld
import whois

class rapidDNS:
    def __init__(self, domain):
        self.domain = domain

    def EnumSubdomains(self):
        url = f"https://rapiddns.io/s/{self.domain}#result"
        response = requests.get(url)
        if response.status_code == 200:
            ResponseContent = response.text
            RegexPattern =  r'<td>([a-zA-Z0-9.-]+\.{}|{})</td>'.format(self.domain, self.domain)
            subdomains = re.findall(RegexPattern, ResponseContent) #returns subdomains as a list of strings
            subdomains = list(set(subdomains))  # Remove duplicates
            print(f"{Fore.BLUE}... Subdomains collected from rapiddns.io successfully ...{Style.RESET_ALL}")
            return subdomains
        else:
            print(f"Failed to fetch subdomains from {url}")
            return []
        
class crtSH:
    def __init__(self, domain):
        self.domain = domain

    def EnumSubdomains(self):
        url = f"https://crt.sh/?q={self.domain}"
        response = requests.get(url)
        if response.status_code == 200:
            ResponseContent = response.text
            RegexPattern = r'<TD>([a-zA-Z0-9.-]+\.{}|{})</TD>'.format(self.domain, self.domain)
            subdomains = re.findall(RegexPattern, ResponseContent)
            subdomains = list(set(subdomains))
            print(f"{Fore.BLUE}... Subdomains collected from crt.sh successfully ...{Style.RESET_ALL}")
            return subdomains
        else:
            print(f"Failed to fetch subdomains from {url}")
            return []
        
    def EnumInJSON(self):
        url = f"https://crt.sh/?q={self.domain}&output=json"
        response = requests.get(url)
        if response.status_code == 200:
            ResponseDictionary = response.json()
            subdomains = []
            for entry in ResponseDictionary:
                subdomains.append(entry['common_name'])
            subdomains = list(set(subdomains))

            #IF we want to remove subdomains that dont contain our domain 
            #for d in subdomains:
            #    if f"{self.domain}" not in d:
            #        subdomains.remove(d)
            
            print(f"{Fore.BLUE}... Subdomains collected from crt.sh JSON output successfully ...{Style.RESET_ALL}")
            return subdomains
        else:
            print(f"Failed to fetch subdomains from {url}")
            return []

#Checks the subdomains if alive by making an HTTP request to each and checking the returned status code
class SubdomainChecker:
    def __init__(self, subdomains):
        self.subdomains = subdomains

    def check(self):
        Alive = []
        NotAlive = []
        for sub in self.subdomains:
            try:
                response = requests.head(f"http://{sub}", timeout=5)
                if response.status_code:
                    Alive.append(sub)
                else:
                    NotAlive.append(sub)
            except requests.ConnectionError:
                NotAlive.append(sub)
            except requests.exceptions.InvalidURL:
                NotAlive.append(sub)
        return Alive, NotAlive

def main(domain):
    print("\n---------Starting Active Scan----------")
    rapid = rapidDNS(domain)
    crt = crtSH(domain)
    
    subdomainsRapid = rapid.EnumSubdomains()
    subdomainsCRT = crt.EnumSubdomains()
    subdomainsCRTJSON = crt.EnumInJSON()

    #Combine subdomains and remove duplicates
    AllSubDomains = list(set(subdomainsRapid + subdomainsCRT))
    print(f"\nAll Subdomains collected for {domain}:")
    print(f"Total Number of Subdomains: {len(AllSubDomains)}\n")
    for s in AllSubDomains:
        print(s)

    print("\n-----------------------")
    print(f"{Fore.MAGENTA}Extra subdomains collected only from crt.sh JSON format:\n{Style.RESET_ALL}")
    for s in subdomainsCRTJSON:
        if s not in AllSubDomains:
            print(f"{Fore.MAGENTA}{s} {Style.RESET_ALL}")

    print("---------Validating Subdomains---------")
    Checker = SubdomainChecker(AllSubDomains)
    alive , notAlive = Checker.check() 
    
    print("\n-----------------------")
    print(f"{Fore.GREEN}Alive Subdomains:\n{Style.RESET_ALL}")
    for s in alive:
        print(f"{Fore.GREEN}{s} {Style.RESET_ALL}") 
        
    print("\n-----------------------")
    print(f"{Fore.RED}Not alive subdomains:\n{Style.RESET_ALL}")
    for s in notAlive:
        print(f"{Fore.RED}{s} {Style.RESET_ALL}")

    print("\n-----------------------")
    print(f"Results of Whois {domain}:")
    w = whois.whois(domain)
    print(w) 

if __name__ == "__main__":
    domain = input("Enter a valid domain name: ")

    main(domain)

    print("\nTHE END\n")

    