import sys
import json

f = open('tag_info.json')
ls=json.load(f)
for tg in ls:
    if tg['Tag']==sys.argv[1]:
        print(tg['Info'])
        sys.stdout.flush()