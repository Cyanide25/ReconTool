import requests
import re
from colorama import Fore, Style

class AzureBLobs:
    def __init__(self,domain):
        self.domain = domain
    
    def Permutations(self):
        filePath = "./Wordlists/Permutations.txt"
        file = open(filePath,"r").read().splitlines()

        d = self.domain
        c = d.split('.')
        CompanyName = c[0]

        words = open("./Temp/blobhunting.txt","w")
        words.close()

        words = open("./Temp/blobhunting.txt","a")

        words.write(CompanyName+'\n')

        for w in file:
            words.write(CompanyName + w + '\n')
            words.write(w + CompanyName + '\n')

        for w in file:
            words.write(w + CompanyName + w +'\n')
            words.write(CompanyName + w + w +'\n')
            words.write(w + w + CompanyName + '\n')
        
        words.close()

    def StorageHunting(self):
        print("------Hunting Storage Accounts------")
        baseURL = ".blob.core.windows.net"
        StorageAcc = open("./Output/AzureStorages.txt","w")
        StorageAcc.close()
        StorageAcc = open("./Output/AzureStorages.txt","a")
        words = open("./Temp/blobhunting.txt","r").read().splitlines()

        for w in words:
            url ="https://" + w + baseURL
            try:
                resp = requests.get(url)
            except Exception as error:
                continue

            print("Storage Account Found: " + w + baseURL)
            StorageAcc.write(w+baseURL+'\n')
        StorageAcc.close()

    def ContainerHunting(self):
        def ParsingBlobs(response,blobs):
            regex = r'<Url>(.*?)<\/Url>'
            BlobsL = re.findall(regex, response)
            blobs.extend(BlobsL)
            return blobs


        print("\n----------Starting Container Hunting---------")
        Cpath = "./Wordlists/containers.txt"
        Accounts = open("./Output/AzureStorages.txt","r").read().splitlines()
        Containers = open(Cpath,"r").read().splitlines()
        #ContainersList = open("./Output/containersfound.txt","w")
        #ContainersList.close()
        #ContainersList = open("./Output/containersfound.txt","a")
        ContainersL = []
        Blobs = []
        for a in Accounts:
            for c in Containers:
                url = "https://"+ a +"/" + c + "?restype=container&comp=list"
                try:
                    resp = requests.get(url)
                    if resp.status_code == 200:
                        print("Container Found:"+a+'/'+c)
                        #ContainersList.write(a+'/'+c+'\n')
                        ContainersL.append(a+'/'+c)
                        Blobs = ParsingBlobs(resp.text,Blobs)
                except Exception as error:
                    continue
        #ContainersList.close()
        return Blobs
        
class AWSBuckets:
    def __init__(self,domain):
        self.domain = domain
    
    def Permutations(self):
        filePath = "./Wordlists/Permutations.txt"
        file = open(filePath,"r").read().splitlines()

        d = self.domain
        c = d.split('.')
        CompanyName = c[0]

        words = open("./Temp/Buckethunting.txt","w")
        words.close()

        words = open("./Temp/Buckethunting.txt","a")

        words.write(CompanyName+'\n')

        for w in file:
            words.write(CompanyName + w + '\n')
            words.write(w + CompanyName + '\n')

        for w in file:
            words.write(w + CompanyName + w +'\n')
            words.write(CompanyName + w + w +'\n')
            words.write(w + w + CompanyName + '\n')
        
        words.close()

    def GetBuckets(self):
        def ParsingAWSBuckets(url,response,bucket):
            regex = r'<Key>(.*?)<\/Key>'
            links = re.findall(regex,response)
            for l in links:
                bucket.append(url+l)
            return bucket
            
        baseURL = ".s3.amazonaws.com/"
        words = open("./Temp/Buckethunting.txt","r").read().splitlines()
        BucketL = []
        for w in words:
            url ="https://" + w + baseURL
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    print("AWS Bucket Found: " + w + baseURL)
                    BucketL = ParsingAWSBuckets(url,resp.text,BucketL)
                elif resp.status_code == 403:
                    print("Protected AWS Bucket Found: " + w + baseURL)
                else:
                    continue
            except Exception as error:
                continue

        return BucketL
            

class GCPBuckets:
    def __init__(self,domain):
        self.domain = domain
    
    def Permutations(self):
        filePath = "./Wordlists/Permutations.txt"
        file = open(filePath,"r").read().splitlines()

        d = self.domain
        c = d.split('.')
        CompanyName = c[0]

        words = open("./Temp/GCPBuckethunting.txt","w")
        words.close()

        words = open("./Temp/GCPBuckethunting.txt","a")

        words.write(CompanyName+'\n')

        for w in file:
            words.write(CompanyName + w + '\n')
            words.write(w + CompanyName + '\n')
            words.write(CompanyName + '-' + w +'\n')
            words.write(w + '-' + CompanyName + '\n')

        for w in file:
            words.write(w + CompanyName + w +'\n')
            words.write(CompanyName + w + w +'\n')
            words.write(w + w + CompanyName + '\n')
            
        words.close()
    
    def GetBuckets(self):
        def ParsingGCPBuckets(url,response,bucket):
            regex = r'<Key>(.*?)<\/Key>'
            links = re.findall(regex,response)
            for l in links:
                bucket.append(url+'/'+l)
            return bucket
        
        baseURL = "https://storage.googleapis.com/"
        words = open("./Temp/GCPBuckethunting.txt","r").read().splitlines()
        BucketL = []
        for w in words:
            url = baseURL + w
            try:
                resp = requests.get(url)
                
                if resp.status_code == 200:
                    print("GCP Bucket Found: " + baseURL + w)
                    BucketL = ParsingGCPBuckets(url,resp.text,BucketL)
                elif resp.status_code == 403:
                    print("Protected GCP Bucket Found: " + baseURL + w)
                else:
                    continue
            except Exception as error:
                continue

        return BucketL

def main(domain):
    print("\n----------Cloud Storage Recon----------")
    print(f"{Fore.MAGENTA}-------------------Hunting for Azure Blobs-------------------{Style.RESET_ALL}")

    Hunt = AzureBLobs(domain)
    Hunt.Permutations()
    Hunt.StorageHunting()
    BlobsList = Hunt.ContainerHunting()
    print("\n-------Printing Blobs Found:---------")
    for blob in BlobsList:
        print(blob)
    
    print(f"\n{Fore.MAGENTA}-------------------Hunting for AWS Buckets-------------------{Style.RESET_ALL}")
    awshunt = AWSBuckets(domain)
    awshunt.Permutations()
    awsBs = awshunt.GetBuckets()
    print("\nPrinting AWS Bucket links:")
    for l in awsBs:
        print(l)
    
    print(f"\n{Fore.MAGENTA}-------------------Hunting for GCP Buckets-------------------{Style.RESET_ALL}")
    gcphunt = GCPBuckets(domain)
    gcphunt.Permutations()
    gcpBs = gcphunt.GetBuckets()
    print("\nPrinting GCP Bucket links:")
    for l in gcpBs:
        print(l)

if __name__ == "__main__":
    
    domain = input("Please enter a domain: ")

    main(domain)
   