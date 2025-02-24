# -------- 使得python脚本在当前目录下运行 --------
import os, sys
os.chdir(os.path.dirname(sys.argv[0]))
# --------------------------------------------

# 导入所需库
"""
JSON库介绍
库名称: json
库功能: 用于处理JSON数据
{
    "key1": "value1",
}
json库可以通过loads()函数将JSON字符串转换为Python字典
也可以通过load()函数将JSON文件转换为Python字典
"""
import json

# 定义账号数据
user_account = {}
# 定义用户数据
user_data = {}
# --------- start function define ----------
# 读取用户账号数据函数
def load_user_account() -> dict:
    # 定义将要返回的用户账号数据
    usr_acct = {}
    # 打开database.dat文件
    file = open("database.dat", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()
    # 将文件内容按行分割
    cache = []
    # 遍历文件内容
    for line in content.split("\n"):
        # 如果行不为空
        if line != "":
            # 将行添加到缓存中
            cache.append(line)
        # 如果行为空
        else:
            # 将缓存中的用户名和密码添加到用户账号数据中
            usr_acct[cache[0]] = cache[1]
            # 清空缓存
            cache = []
    # 返回
    return usr_acct
    
# 读取用户数据函数
def load_user_data() -> dict:
    # 定义将要返回的用户账号数据
    usr_dat = {}
    # 打开database.json文件
    file = open("database.json", "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()
    # 将文件内容转换为字典
    usr_dat = json.loads(content)
    # 返回
    return usr_dat

# 登录函数
def login(username: str, password: str) -> int:
    # 判断用户是否存在
    if username not in user_account:
        # 返回1
        return 1
    # 判断密码是否正确
    if user_account[username] != password:
        # 返回2
        return 2
    # 返回0
    return 0


# 获取用户数据函数
def get_user_data(username: str) -> dict:
    # 返回用户数据
    return user_data[username]
    
# --------- end function define ----------

# 使用函数加载用户账号数据
user_account = load_user_account()
# 使用函数加载用户数据
user_data = load_user_data()
# 获取用户输入
username = input("请输入用户名: ")
password = input("请输入密码: ")
# 登录
status = login(username, password)
# 判断登录状态
if status == 0:
    # 获取用户数据
    data = get_user_data(username)
    # 输出用户数据
    print("--- 用户数据 ---")
    print("用户名:", username)
    print("邮箱:", data["email"])
    print("注册时间:", data["registerTime"])
    print("金币:", data["coin"])
    print("admin等级:", data["admin_level"])
# 假设状态不为0
elif status == 1:
    # 输出错误信息
    print("用户不存在")
elif status == 2:
    # 输出错误信息
    print("密码错误")
else:
    # 输出错误信息
    print("未知错误")
    