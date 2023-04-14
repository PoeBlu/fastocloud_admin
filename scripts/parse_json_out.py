#!/usr/bin/env python3
import json

if __name__ == '__main__':
    with open("out.m3u", "w") as f:
        f.write('#EXTM3U\n')
        with open('test.json') as json_file:
            data = json.load(json_file)
            for idx, p in enumerate(data):
                name = p['name']
                icon = p['icon']
                group = p['group']
                sid = p['input']['urls'][0]['id']
                input = p['input']['urls'][0]['uri']
                f.write('#EXTINF:{0} tvg-id="{1}" tvg-name="" tvg-logo="{3}" group-title="{4}",{2}\n{5}\n'.format(
                    idx,
                    sid,
                    name,
                    icon,
                    group,
                    input))
