#!/usr/bin/python3

import argparse
from os.path import exists
from urllib.parse import urlparse, parse_qs, urlencode
import sys
parser = argparse.ArgumentParser(description='Modify the values of query parameters in a list of URLs.')
parser.add_argument('-f', '--file', help='the file containing the list of URLs to modify.')
parser.add_argument('-q', '--query', help='the file containing the list of parameters to filter.', default=False)
parser.add_argument('-p', '--payload', help='the payload to substitute.', default='W00t')
parser.add_argument('-i', '--input', help='receive input from a piped tool.')
args = parser.parse_args()

def parse_query_params(wordlist):
    modified_url = []
    for url in wordlist:
        parsed_url = urlparse(url)
        if not parsed_url.query:
            continue
        if '.css' in parsed_url.path or '.js' in parsed_url.path:
            continue
        query_params = parse_qs(parsed_url.query, keep_blank_values=True, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)
        updated_url = modify_query_params(parsed_url, query_params, modified_url)
    return updated_url

def modify_query_params(parsed_url, query_params, modified_url):
    if args.query != False and exists(f'{args.query}'):

        for i, key in enumerate(query_params):
            filtered_params = open(f'{args.query}')
            for query in filtered_params.readlines():
                if key != query.strip():
                    continue
                else:
                    query_params[key] = args.payload
                    updated_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
                    modified_url.append(updated_url)
                    query_params[key] = parse_qs(parsed_url.query, keep_blank_values=True)[key][0]
    
    elif args.query == False or not exists(f'{args.query}'):
        
        for i, key in enumerate(query_params):
            query_params[key] = args.payload
            updated_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
            modified_url.append(updated_url)
            query_params[key] = parse_qs(parsed_url.query, keep_blank_values=True)[key][0]
    else:
        parser.error('Query file not found...')

    return modified_url


def main():
    if args.input == '-':
        wordlist = [line.strip() for line in sys.stdin]
        modified_urls = parse_query_params(wordlist)
    
    elif exists(f'{args.file}'):
        with open(f'{args.file}', 'r') as f:
            wordlist = [line.strip() for line in f.readlines()]
            modified_urls = parse_query_params(wordlist)
    else:
        parser.error('Input file is missing...')
    
    for url in modified_urls:
        print(url)

if __name__ == '__main__':
     main()
