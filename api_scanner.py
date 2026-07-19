import requests

# In ra giao diện tool
def banner(url):
    print("=" * 30)
    print("          API SCANNER         ")
    print("=" * 30)
    print(f"URL           : {url}")

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
    print("Total object  :", len(data))

# In ra màn hình kết quả sau khi scan
def result_scan(response):
    print(f"Status code   : {response.status_code}")
    print(f"Response Time : {response.elapsed}")

    content_type = response.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        return "JSON: No"
    
    print(f"Content-Type  : {content_type}")
    
    server = response.headers.get("Server", "Unknown")
    print(f"Server        : {server}")
    print(f"JSON type     : {type(response.json()).__name__}")

# Tìm ra người dùng đầu tiên trong dữ liệu
def first_user(data):
    #for user in data:
    #    if user['id'] == 1:
    #        print(f"First username: {user['username']}")
    if len(data) > 0:
        print("First username:", data[0]['username'])

# Chạy và đề phòng các lỗi xảy ra
try:
    url = input("URL: ")
    banner(url)

    response = get_request(url)

    # Tạo lỗi khi status code không phải là 200
    response.raise_for_status()
    
    json_data = response.json()
    
    result_scan(response)
    
    count_object(json_data)
    
    first_user(json_data) 

except requests.exceptions.MissingSchema:
    print("Invalid URL")

except requests.exceptions.ConnectionError:
    print("Cannot connect to target")

except requests.exceptions.Timeout:
    print("Time out connection")

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error {e}")

except requests.exceptions.JSONDecodeError:
    print("JSON Decoder Error")

except KeyboardInterrupt:
    print()

except requests.exceptions.RequestException as e:
    print(f"Failed: {e}")

finally:
    print("Connection closed")