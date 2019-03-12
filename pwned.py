#!/usr/bin/env python3

import hashlib
import urllib.request
import sys

sha = hashlib.sha1()

pass_to_check = sys.argv[1]

sha.update(pass_to_check.encode('utf-8'))

hashed_text = sha.hexdigest().upper()
hashed_beg = hashed_text[:5]
hashed_end = hashed_text[5:]

# api requires 5 first chars of hash
url = "https://api.pwnedpasswords.com/range/" + hashed_beg + '/'
user_agent = 'Pwnage-Checker-For-iOS'

# Url requires to use user agent
hdr = {'User-Agent': user_agent, }

# using Request class because user agent header is mandatory
req = urllib.request.Request(url, headers=hdr)

url_downloaded = urllib.request.urlopen(req)
url_downloaded = url_downloaded.read().decode('utf-8').split('\r\n')

pass_found = False

# downloaded data is in format of hash:occurances so to compare
# them split is necessary
#
# downloaded hashes are without beggining which we provided into url
for item in url_downloaded:
    splitted = item.split(':')
    if hashed_end == splitted[0]:
        occur = int(splitted[1])
        print('password {} was found as {}\n{} times'.format(pass_to_check,
                                                             hashed_text,
                                                             occur))
        pass_found = True
        break

if not pass_found:
    print('{} not found'.format(pass_to_check))
