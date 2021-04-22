# Cloudflare Purge
Script to purge Cloudflare cache for the specified urls

## Requirements
- python3: tested on python 3.7.10
- lib request: pip3 install requests
- lib colorama: pip3 install colorama

## API key
Create your API token here: https://dash.cloudflare.com/profile/api-tokens  
then assign the correct values for `cfZone`, `cfAuthEmail` and `cfAuthKey` variables in the python script  

## USAGE
```bash
python3 cf-purge --url=url1,url2,... [--bulk]
```
The default behaviour is to make one `POST` call for every url specified; with the `--bulk` option, the script makes only one call to the Cloudflare API.
The bulk requests are limited to 30 urls, so if you specify more than 30 urls the script makes multiple `POST` calls of max 30 urls.
