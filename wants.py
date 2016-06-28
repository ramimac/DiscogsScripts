import requests as req 
import json
import wantsconfig as wc 

headers = {
    'Authorization': 'Discogs token='+wc.token,
}

wantlist = req.get('https://api.discogs.com/users/ramimac/wants', headers=headers)
print wantlist 