import Passive
import Active
import Cloud
from colorama import Fore, Style
from tld import get_tld

def ValidateDomain(domain):
    try:
        get_tld(domain, fix_protocol=True)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print("----------Reconnaissance Tool-----------")
    domain = input("Please enter a domain: ")
    if(ValidateDomain(domain)):
        print(f"{Fore.BLUE}... Starting Recon ... {Style.RESET_ALL}")
    else:
        print("Please enter valid domain")
        exit()

    mod = int(input("""Please enter the number of the mode you would like to start with: 
    1- Passive Scan
    2- Active Scan
    3- Cloud Storage Hunting
Your input: """))
    if mod == 1:
        Passive.main(domain)
    elif mod == 2:
        Active.main(domain)
    elif mod == 3:
        Cloud.main(domain)
    else:
        print("Please enter a valid option")
        exit()

    print("\nTHE END\n")

    