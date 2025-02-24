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
json库可以通过dump()函数将Python字典转写入JSON文件
也可以通过dumps()函数将Python字典转换为JSON字符串
"""
import json

book_data = { }
# --------- start function define ----------
def register_book(book_name: str, book_author: str, book_price: float) -> int:
    # 如果书名已经存在
    if book_name in book_data:
        # 返回错误信息
        return 1 # 书名已存在
    # 如果书名不存在
    else:
        # 添加书名
        book_data[book_name] = {
            "author": book_author,
            "price": book_price
        }
        # 返回成功信息
        return 0 # 注册成功

def delete_book(book_name: str) -> int:
    # 如果书名不存在
    if book_name not in book_data:
        # 返回错误信息
        return 1 # 书名不存在
    # 如果书名存在
    else:
        # 删除书名
        book_data.pop(book_name)
        # 返回成功信息
        return 0 # 删除成功

def search_book(book_name: str) -> dict:
    # 如果书名不存在
    if book_name not in book_data:
        # 返回错误信息
        return {
            "error": 1 # 书名不存在
        }
    # 如果书名存在
    else:
        # 返回书名信息
        return {
            "author": book_data[book_name]["author"],
            "price": book_data[book_name]["price"],
            "error": 0 # 无错误
        }

def save_books() -> int:
    # 打开文件
    file = open("book_data.json", "w")
    # 将数据写入文件
    # 为保持数据可读性 在参数中添加indent=4
    json.dump(book_data, file, indent=4)
    # 关闭文件
    file.close()
    # 返回成功信息
    return 0


def load_books() -> dict:
    # 如果文件不存在
    if not os.path.exists("book_data.json"):
        # 返回空字典
        return { }
    
    # 打开文件
    file = open("book_data.json", "r")
    # 读取文件
    book_data = json.load(file)
    # 关闭文件
    file.close()
    # 返回数据
    return book_data
    
# --------- end function define ----------

# 读取数据
book_data = load_books()

# 循环 让用户进行操作
while True:
    # 分割线
    print("-" * 80)
    # 输出提示信息
    print("1. 注册书籍")
    print("2. 删除书籍")
    print("3. 查询书籍")
    print("4. 退出")
    # 输入用户选择
    choice = input("请选择操作: ")
    # 如果用户选择1
    if choice == "1":
        # 输入书名
        book_name = input("请输入书名: ")
        # 输入作者
        book_author = input("请输入作者: ")
        # 输入价格
        book_price = float(input("请输入价格: "))
        # 调用函数
        result = register_book(book_name, book_author, book_price)
        # 如果注册成功
        if result == 0 and save_books() == 0:
            print("注册成功")
        # 如果注册失败
        else:
            print("注册失败")
    # 如果用户选择2
    elif choice == "2":
        # 输入书名
        book_name = input("请输入书名: ")
        # 调用函数
        result = delete_book(book_name)
        # 如果删除成功
        if result == 0 and save_books() == 0:
            print("删除成功")
        # 如果删除失败
        else:
            print("书籍删除失败")
    # 如果用户选择3
    elif choice == "3":
        # 输入书名
        book_name = input("请输入书名: ")
        # 调用函数
        result = search_book(book_name)
        # 如果书名不存在
        if result["error"] == 1:
            print("书名不存在")
        # 如果书名存在
        else:
            print("-" * 80)
            print("查询结果:")
            print("书名:", book_name)
            print("作者:", result["author"])
            print("价格:", result["price"])
    # 如果用户选择4
    elif choice == "4":
        # 退出循环
        break
    # 如果用户选择错误
    else:
        print("选择错误")
