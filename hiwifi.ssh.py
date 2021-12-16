"""
    # hiwifi.openssh

    Script to open HiWiFi ssh

    when I ssh to my HiWiFi, get a refused:
    ```
    ssh: connect to host 192.168.41.1 port 22: Connection refused
    ```
    I write this script to open ssh for lazy man like me...

    very very thanks http://www.hiwifi.wtf/

    Note I only testing it in my HiWiFi, the system version is **HC5661A - 1.4.10.20837s**

    ```
    pip install requests
    python hiwifi.ssh.py -H {host_ip}
    ```

    open ssh success like this:

    ```
    ╰─ python hiwifi.ssh.py -H 192.168.41.1
    [+] uuid: 12345678-1234-5678-1234-123456789012
    [+] local token: RDRFRTA3NEE123456789NzaCwxNTY0MjE3MT123456789/i2a1hZBWqmA123456789
    [+] cloud token: yaELY8i123456789n9QXOtYw=
    [+] Success: ssh port is 22
    ```
"""

import argparse
import requests
import re


def print_color(info):
    if '[-]' in info:
        print('\033[1;31m{}\033[0m'.format(info))
    elif '[+]' in info:
        print('\033[1;32m{}\033[0m'.format(info))
    elif '[!]' in info:
        print('\033[1;33m{}\033[0m'.format(info))
    else:
        print('\033[0;37m{}\033[0m'.format(info))


def check_host(host: str):
    req = requests.get(url=f'http://{host}', timeout=3)
    req.raise_for_status()



def get_local_token(host: str):
    """
        API: http://192.168.199.1/local-ssh/api?method=get
        extract the api from page http://192.168.199.1/local-ssh
    """
    req = requests.get(
        url=f'http://{host}/local-ssh/api',
        params={'method': 'get'}
    )
    req.raise_for_status()
    return req.json().get('data')


def get_uuid(host: str):
    req = requests.get(
        url=f'http://{host}/cgi-bin/turbo/proxy/router_info'
    )
    req.raise_for_status()
    return req.json().get('data').get('uuid')


def get_cloud_token(local_token: str, uuid: str):
    """
        http://www.hiwifi.wtf/
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '128',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.hiwifi.wtf',
        'Origin': 'http://www.hiwifi.wtf',
        'Referer': 'http://www.hiwifi.wtf/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    req = requests.post(
        url='http://www.hiwifi.wtf/',
        data={'local_token': local_token, 'uuid': uuid},
        headers=headers
    )
    req.raise_for_status()
    
    find_block = None
    for line in req.iter_lines():
        dec_str = line.decode('utf-8')
        if 'cloud_token' in dec_str:
            find_block = dec_str
            break

    if not find_block:
        print_color('[-] cloud_token not found!')
        return None

    matched = re.search(r'cloud_token\S\s*(\S+?)<', find_block)
    if not matched:
        print_color(f'[-] regex match cloud_token failed in content: {find_block}')
        return None

    return matched.group(1).strip()


def valid_token(host: str, cloud_token: str):
    """
        {"data": "Success: ssh port is 22", "code": 0}
        {"data": "Error: valid token error", "code": 1}
    """
    req = requests.get(
        url=f'http://{host}/local-ssh/api',
        params={'method': 'valid', 'data': cloud_token}
    )
    req.raise_for_status()

    info = req.json()
    return info.get('code'), info.get('data')


def open_ssh(host: str):
    check_host(host)

    uuid = get_uuid(host)
    if not uuid:
        print_color('[-] uuid not found!')
        return False
    print_color(f'[+] uuid: {uuid}')

    local_token = get_local_token(host)
    if not local_token:
        print_color('[-] local token not found!')
        return False
    print_color(f'[+] local token: {local_token}')
    
    cloud_token = get_cloud_token(local_token, uuid)
    if not cloud_token:
        print_color('[-] cloud token not found!')
        return False
    print_color(f'[+] cloud token: {cloud_token}')

    code, msg = valid_token(host, cloud_token)
    fmt = '[-]' if code else '[+]'
    print_color(f'{fmt} {msg}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host', dest='host', 
        required=False, default='192.168.199.1',
        help='Hiwifi Host IP.'
    )
    args = parser.parse_args()
    open_ssh(args.host)
