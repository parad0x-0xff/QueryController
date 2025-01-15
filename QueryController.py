#!/usr/bin/python3

import argparse
from os.path import exists
from urllib.parse import urlparse, parse_qs, urlencode
import sys
import re
parser = argparse.ArgumentParser(description='Modify the values of query parameters in a list of URLs.')
parser.add_argument('-f', '--file', nargs='?',type=argparse.FileType('r'), default=sys.stdin, help='A file containing the list of URLs to modify OR piped stdin.')
parser.add_argument('-q', '--query', help='A file containing the list of parameters to filter.', default=False)
parser.add_argument('-p', '--payload', help='Payload to substitute.', default='W00t')
parser.add_argument('-e', '--extension', help='Extensions file to avoid.',default=False)
args = parser.parse_args()

def extension_parse(ext_file, parsed_url):
    try:
        with open(ext_file) as ext:
            for line in ext.readlines():
                extension = line.strip()
                if not extension: 
                    continue
                pattern = ".*" + re.escape(extension)
                if re.search(pattern, parsed_url.query):
                    return None
            return parsed_url
    except FileNotFoundError:
        parser.error('Extension file not found...')
    except IOError:
        parser.error('Error reading extension file...')
        
def parse_query_params(wordlist):
    modified_url = []
    updated_url = ''
    for url in wordlist:
        parsed_url = urlparse(url)
        if not parsed_url.query:
            continue
        if args.extension != False:
            new_url = extension_parse(args.extension, parsed_url)
            if new_url is None:
                continue
        query_params = parse_qs(parsed_url.query, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)
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

    try:
        with args.file as f:
            wordlist = [line.strip() for line in f.readlines()]
            modified_urls = parse_query_params(wordlist)
    except:
        parser.error('Input file is missing...')

    for url in modified_urls:
        print(url)

if __name__ == '__main__':
     main()
