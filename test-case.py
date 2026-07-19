users = [
    {
        "username": "alice",
        "role": "admin",
        "active": True
    },
    {
        "username": "bob",
        "role": "user",
        "active": False
    },
    {
        "username": "charlie",
        "role": "user",
        "active": True
    }
]

# In tất cả username.
for user in users:
    print(f"Username: {user['username']}")
print("")

# Chỉ in username của những tài khoản đang hoạt động (active == True).
for user in users:
    #if user["active"] == True:
    #    print(f"Username Active: {user['username']}")
    if user["active"]:
        print(f"Username Active: {user['username']}")
print("")

# Đếm xem có bao nhiêu user.
countUserExist = 0
for user in users:
    countUserExist += 1
print(f"Total user: {countUserExist}\n")

# Đếm xem có bao nhiêu admin.
countAdmin = 0
for user in users:
    if "admin" in user["role"]:
        countAdmin += 1
print(f"Total user admin: {countAdmin}")
