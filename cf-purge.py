#!/usr/bin/python3

# Script to purge Cloudflare cache for the specified urls
#
# Usage:
# python3 cf-purge --url=url1,url2,... [--bulk]
#
# Requirements:
# python3: tested on python 3.7.10
# lib request: pip3 install requests
# lib colorama: pip3 install colorama

import getopt
import json
import sys

import requests
from colorama import init, Fore, Style

cfZone = ''
cfAuthEmail = ''
cfAuthKey = ''
cfUrl = 'https://api.cloudflare.com/client/v4/zones/' + cfZone + '/purge_cache'


def main(argv):
    help_string = "Usage: python3 cf-purge --url=url1,url2,... [--bulk]"

    # use Colorama to make colors work on Windows too
    init()

    mode = 'single'
    urls = ''

    if cfZone == '' or cfAuthEmail == '' or cfAuthKey == '':
        print(
            Fore.YELLOW + "Please populate cfZone, cfAuthEmail and cfAuthKey variables with your Cloudflare API "
                          "credentials" + Style.RESET_ALL)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "hu:b", ["help", "url=", "bulk"])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_string)
            sys.exit()
        if opt in ("-u", "--url"):
            urls = arg
        elif opt in ("-b", "--bulk"):
            mode = 'bulk'

    if urls == '':
        print(help_string)
        sys.exit(1)

    headers = {'X-Auth-Email': cfAuthEmail, 'X-Auth-Key': cfAuthKey, 'Content-Type': 'application/json'}
    list_urls = urls.split(',')

    if mode == "bulk":
        sub_list_urls = [list_urls[x:x + 30] for x in range(0, len(list_urls), 30)]
        for sub_list_url in sub_list_urls:
            cf_cache_void(headers, sub_list_url)
    else:
        for url in list_urls:
            cf_cache_void(headers, [url])


def cf_cache_void(headers, list_urls):
    urls = {'files': list_urls}

    try:
        response = requests.post(cfUrl, headers=headers, data=json.dumps(urls))
        response.raise_for_status()
        json_response = response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if json_response['success']:
        print(Fore.GREEN + str(list_urls) + Style.RESET_ALL + " - success")
    else:
        print(
            Fore.RED + str(list_urls) + Style.RESET_ALL + " - [" + str(json_response['errors'][0]['code']) + "] " + str(
                json_response['errors'][0]['message']))


if __name__ == "__main__":
    main(sys.argv[1:])
