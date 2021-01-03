import requests
import json
import random
import time
import logging
import argparse
import string
import json
import multiprocessing
from functools import partial

def main(maxFileCount:int, corruptionRate:int, maxFileCharCount:int, timeout:int, url:str, requestsCount: int):
    #Create the processing pool
    with multiprocessing.Pool(requestsCount) as pool:
         #Create the function with the arguments to pass in each process
         func = partial(run, maxFileCount, corruptionRate,
         maxFileCharCount, timeout, url)
         pool.map(func=func, iterable=range(1,requestsCount))

def run(maxFileCount, corruptionRate, maxFileCharCount, timeout, url, *args):
    #Create the generator instance    
    generator = FileGenerator(maxFileCount=maxFileCount, corruptionRate=corruptionRate,
    maxFileCharCount=maxFileCharCount, timeout=timeout)
    while True:
        try:
            generator.SendFiles(url=url)
        except Exception as e:
            logging.error(f'An error occurred {e}')

class FileGenerator():
    def __init__(self,maxFileCount:int, corruptionRate:int, maxFileCharCount:int, timeout:int):
        self.maxFileCount = maxFileCount
        self.corruptionRate = corruptionRate
        self.maxFileCharCount = maxFileCharCount
        self.timeout = timeout

    def SendFiles(self,url:str):
        """Will generate random file names and send to the provided URL"""
        body = json.dumps({
            "files":self.Generate_Random_Files_Dict()
        })
        logging.debug(f'Sending request to {url}')
        response = requests.post(url=url, timeout=self.timeout, data=body)
        logging.debug(f'Server response {response.status_code}:{response.content}')
    
    def Generate_Random_Files_Dict(self) -> dict:
        """Will generate a random dictionary where the key is the file name and value is a boolean indication whether the file is corrupted."""
        file_count = random.randint(1,self.maxFileCount)
        #Set true if to include corrupted file and false otherwise
        includes_corrupted = (random.random() * 100 <= self.corruptionRate)
        files_dict = {}
        #Create the files
        logging.debug(f'Going to generate {file_count} files')
        for i in range(0, file_count):
            file_name = Get_Random_File_Name(self.maxFileCharCount)
            files_dict[file_name] = False
        
        #Set random key value to true if to include a corrupted file
        if includes_corrupted:
            random_key = random.choice(list(files_dict.keys()))
            files_dict[random_key] = True
            logging.debug(f'Request will corrupted file {random_key}')
        return files_dict

def Get_Random_File_Name(count:int) -> str:
    """Will return a random file name will number of character between 1 - count"""
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k= random.randint(1,count)))
    file_extension = ''.join(random.choices(string.ascii_letters + string.digits, k= random.randint(1,count)))
    return f'{file_name}.{file_extension}'

if __name__ == '__main__':
    #Parse commandline args
    parser = argparse.ArgumentParser(description='Tool to load the transfer service')
    parser.add_argument("--config", const=True, default='config.json', nargs='?', help="The path to the JSON configuration file")
    parser.add_argument("--log", help='The log level')
    parser.add_argument("--url", const=True,nargs='?', help='The URL to send the file names to')
    args = parser.parse_args()
    #Set log level
    logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=getattr(logging, str(args.log).upper())
    )
    #Read config and load it
    configText = ''
    with open(args.config, 'r') as f:
        configText = f.read()
    config = json.loads(configText)
    logging.info(f'Requests will be sent to {args.url}')
    main(
        maxFileCount=config['MaxNumberOfFiles'],
        corruptionRate=config['CorruptionRate'],
        maxFileCharCount=config['MaxFileCharCount'],
        timeout=config['Timeout'],
        url=args.url,
        requestsCount= config["MaxNumberOfParallelRequests"]
    )