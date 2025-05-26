# modules/login_module.py

import json
import os

# 用户数据文件
USER_FILE = "users.json"

def load_users():
    """
    从 JSON 文件中加载用户信息。
    返回一个字典，键为用户名，值为用户数据（例如密码）。
    """
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    """
    将用户信息保存到 JSON 文件。
    """
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def register():
    print("欢迎注册！")
    users = load_users()
    print("当前用户数据:", users)  # 调试输出
    while True:
        username = input("请输入用户名: ")
        if username in users:
            print("用户名已存在，请选择其他用户名。")
        else:
            break
    password = input("请输入密码: ")
    users[username] = {"password": password}
    print("更新后的用户数据:", users)  # 调试输出
    save_users(users)
    print("注册成功！\n")

def login():
    """
    用户登录函数。
    用户需输入正确的用户名和密码才能登录。
    """
    print("欢迎登录系统！")
    users = load_users()
    for attempt in range(3):
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        if username in users and users[username]["password"] == password:
            print("登录成功！\n")
            return True
        else:
            print("用户名或密码错误，请重试。")
    print("尝试次数过多，退出系统。")
    return False

# 可选：测试代码
if __name__ == "__main__":
    register()
    login()