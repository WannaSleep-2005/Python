import requests

# In ra giao diện tool
def banner(url):
    print("=" * 30)
    print("          API SCANNER         ")
    print("=" * 30)
    print(f"\n[*] URL           : {url}")

# Tạo request đến target
def get_request(url):
    return requests.get(
        url,
        timeout = 5
    )

# Đếm các object bên trong dữ liệu
def count_object(data):
    #count = 0
    #for item in data:
    #    count += 1
    #print(f"Total Object : {count}")
    print(f"[+] Total object  : {len(data)}.\n")

# In ra màn hình kết quả sau khi scan
def result_scan(response):
    print(f"[*] Status code   : {response.status_code}.")
    print(f"[*] Response Time : {response.elapsed}.")

    content_type = response.headers.get("Content-Type", "")
    
    print(f"[*] Content-Type  : {content_type}.")
    
    server = response.headers.get("Server", "Unknown")
    print(f"[*] Server        : {server}.")
    
    if "application/json" in content_type:
        print(f"[*] JSON type     : {type(response.json()).__name__}.\n")
    else:
        print("[-] JSON type     : Not JSON.\n")

# Tìm ra người dùng đầu tiên trong dữ liệu
def first_user(data):
    #for user in data:
    #    if user['id'] == 1:
    #        print(f"First username: {user['username']}")
    if len(data) > 0 and "username" in data[0]:
        print(f"[+] First username: {data[0]['username']}.\n")

# In ra cookie
def show_cookies(response):
    if not response.cookies:
        print("[-] Cookie in Response: No Cookies.\n")

    for cookie in response.cookies:
        print(f"[+] Cookie in Response {cookie.name} = {cookie.value}.\n")

# Check API JSON
def is_json(response):
    if "application/json" in response.headers.get("Content-Type", "Unknown"):
        print("[+] Check API JSON in Content-Type: JSON API Detected.\n")
    else:
        print("[-] Check API JSON in Content-Type: Not JSON.\n")

# Kiểm tra các header bảo vệ
def security_headers(response):
    headers_security = {
        "X-Frame-Options": "Clickjacking Protection",
        "X-Content-Type-Options": "MIME Nosniff Protection",
        "Content-Security-Policy": "XSS Protection",
        "Strict-Transport-Security": "HTTPS Enforcement"
    }
    
    levels = {
        0: "Critical",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Excellent"
    }

    score = 0

    print("Check Security Header Response:")
    for header, description in headers_security.items():
        if header in response.headers:
            print(f"[+] {header}: {description}.\n")
            score += 1
        else:
            print(f"[-] No found {header} in Header Response.\n")
    
    print("Score Security Header: ")

    """
    match score:
        case 0:
            print("[*] 0/4 Critical\n")
        case 1:
            print("[*] 1/4 Weak\n")
        case 2:
            print("[*] 2/4 Fair\n")
        case 3:
            print("[*] 3/4 Good\n")
        case 4:
            print("[*] 4/4 Excellent\n")
        case _:
            print("Error score\n")
    """

    print(f"{score}/4 {levels.get(score, "Error score")}\n")

# Chạy và đề phòng các lỗi xảy ra
try:
    url = input("URL: ")
    banner(url)

    # Tạo request đến target
    response = get_request(url)

    # Tạo lỗi khi status code không phải là 200
    response.raise_for_status()

    result_scan(response)

    security_headers(response)

    show_cookies(response)

    is_json(response)

    # Thực thi hàm khi dữ liệu là json
    if "application/json" in response.headers.get("Content-Type"):
        json_data = response.json()

        count_object(json_data)
        
        first_user(json_data) 
    
except requests.exceptions.MissingSchema:
    print("[-] Invalid URL")

except requests.exceptions.ConnectionError:
    print("[-] Cannot connect to target")

except requests.exceptions.Timeout:
    print("[-] Time out connection")

except requests.exceptions.HTTPError as e:
    print(f"[-] HTTP Error {e}")

except requests.exceptions.JSONDecodeError:
    print("[-] JSON Decoder Error")

except KeyboardInterrupt:
    print()

except requests.exceptions.RequestException as e:
    print(f"[-] Failed: {e}")

finally:
    print("[*] Connection closed")