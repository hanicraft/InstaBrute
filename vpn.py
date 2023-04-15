import requests
from bs4 import BeautifulSoup
import openvpn.client
import os

LOGIN_URL = 'https://www.vpnbook.com/'
SERVER_LIST_URL = 'https://www.vpnbook.com/freevpn'

def main():
    response = requests.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'}).get('value')

    username = input('Enter your VPNbook username: ')
    password = input('Enter your VPNbook password: ')
    data = {
        'username': username,
        'password': password,
        'csrf_token': csrf_token
    }
    response = requests.post(LOGIN_URL, data=data, allow_redirects=False)
    if response.status_code == 302:
        print('Login successful!')
    else:
        print('Login failed!')
        return

    response = requests.get(SERVER_LIST_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    servers = []
    for li in soup.find_all('li'):
        server = li.get_text().strip()
        if server.startswith('Free '):
            servers.append(server)

    for i, server in enumerate(servers):
        print(f'{i+1}. {server}')
    selected_server_index = int(input('Enter the server number you want to connect to: ')) - 1
    selected_server = servers[selected_server_index]

    config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vpnbook.ovpn')
    with open(config_file_path, 'w') as f:
        f.write(f'<connection>\nremote {selected_server} 443\nauth-user-pass\n</connection>\n')
    vpn = openvpn.client.Client()
    try:
        vpn.connect(config_file=config_file_path)
    except Exception as e:
        print(f'Error: {e}')
        return
    print(f'Connected to {selected_server}!')

if __name__ == '__main__':
    main()
