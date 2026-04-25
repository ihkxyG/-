import json
import os

# 定义图书类（可选功能：面向对象封装）
class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def to_dict(self):#将Book对象转为字典
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "quantity": self.quantity
        }

# 全局变量，存储图书列表
books = []
FILE_NAME = "books.json"#常量，固定数据保存的文件名

# 1. 从文件加载数据
def load_books():#定义加载本地Json文件数据的函数
    global books
    if os.path.exists(FILE_NAME):#判断文件books。json是否存在
        try:#异常捕获开始，防止文件破损，崩溃
            # with open安全打开文件，自动关闭 encoding="utf-8"防止中文乱码，f文件对象别名
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)#转为列表+字典格式
                books = [Book(**item) for item in data]#遍历
            print(" 图书数据加载成功！")
            #读取报错时执行
        except Exception as e:
            print(f"文件读取出错：{e}，已初始化空的图书列表")
            books = []
    else:
        print("未找到数据文件，已初始化空的图书列表")
        books = []

# 2. 保存数据到文件
def save_books():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in books], f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存失败：{e}")
        return False

# 3. 添加图书信息
def add_book():
    print("\n=== 添加图书 ===")
    while True:
        book_id = input("请输入图书编号(ISBN): ").strip()#去掉首尾空格
        # 检查重复编号
        exists = any(book.book_id == book_id for book in books)
        if exists:
            print("该图书编号已存在，请重新输入！")
            continue
        if not book_id:
            print("图书编号不能为空！")
            continue
        break
    title = input("请输入书名: ").strip()
    while not title:
        print("书名不能为空！")
        title = input("请输入书名: ").strip()
    author = input("请输入作者: ").strip()
    while not author:
        print("作者不能为空！")
        author = input("请输入作者: ").strip()
    # 处理数量输入异常
    while True:
        try:
            quantity = int(input("请输入数量(整数): "))
            if quantity < 0:
                print("数量不能为负数！")
                continue
            break
        except ValueError:
            print("输入格式错误，请输入整数！")
    new_book = Book(book_id, title, author, quantity)
    books.append(new_book)
    print("图书添加成功！")

# 4. 查看所有图书
def show_all_books():
    print("\n=== 所有图书列表 ===")
    if not books:
        print("暂无图书信息！")
        return
    print(f"{'编号':<15} {'书名':<20} {'作者':<15} {'数量':<5}")#格式化表头，<15左对齐,固定宽度
    print("-" * 60)#打印分割线
    for book in books:
        print(f"{book.book_id:<15} {book.title:<20} {book.author:<15} {book.quantity:<5}")

# 5. 查询图书（按ISBN或书名）
def search_book():
    print("\n=== 查询图书 ===")
    keyword = input("请输入要查询的图书编号或书名: ").strip()
    if not keyword:
        print("查询关键词不能为空！")
        return
    results = []
    for book in books:
        if keyword in book.book_id or keyword in book.title:
            results.append(book)
    if not results:
        print("未找到匹配的图书！")
        return
    print(f"{'编号':<15} {'书名':<20} {'作者':<15} {'数量':<5}")
    print("-" * 60)
    for book in results:
        print(f"{book.book_id:<15} {book.title:<20} {book.author:<15} {book.quantity:<5}")

# 6. 修改图书数量
def update_book_quantity():
    print("\n=== 修改图书数量 ===")
    book_id = input("请输入要修改的图书编号: ").strip()
    target_book = None
    for book in books:
        if book.book_id == book_id:
            target_book = book
            break
    if not target_book:
        print("未找到该编号的图书！")
        return
    while True:
        try:
            new_quantity = int(input(f"请输入新的数量(当前数量: {target_book.quantity}): "))
            if new_quantity < 0:
                print("数量不能为负数！")
                continue
            break
        except ValueError:
            print("输入格式错误，请输入整数！")
    target_book.quantity = new_quantity
    print("数量修改成功！")

# 7. 删除图书
def delete_book():
    print("\n=== 删除图书 ===")
    book_id = input("请输入要删除的图书编号: ").strip()
    global books
    original_len = len(books)
    books = [book for book in books if book.book_id != book_id]
    if len(books) == original_len:
        print("未找到该编号的图书！")
    else:
        print("图书删除成功！")

# 8. 按书名或作者排序显示（可选功能）
def sort_books():
    print("\n=== 排序显示图书 ===")
    print("1. 按书名升序")
    print("2. 按作者升序")
    choice = input("请选择排序方式(1/2): ").strip()
    if choice == "1":
        sorted_books = sorted(books, key=lambda x: x.title)
    elif choice == "2":
        sorted_books = sorted(books, key=lambda x: x.author)
    else:
        print("无效选择！")
        return
    print(f"{'编号':<15} {'书名':<20} {'作者':<15} {'数量':<5}")
    print("-" * 60)
    for book in sorted_books:
        print(f"{book.book_id:<15} {book.title:<20} {book.author:<15} {book.quantity:<5}")

# 菜单主程序
def main_menu():
    load_books()
    while True:
        print("\n===== 图书管理系统 =====")
        print("1. 添加图书信息")
        print("2. 查看所有图书")
        print("3. 查询图书")
        print("4. 修改图书数量")
        print("5. 删除图书")
        print("6. 排序显示图书")
        print("7. 保存并退出")
        choice = input("请输入你的选择(1-7): ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            update_book_quantity()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            sort_books()
        elif choice == "7":
            if save_books():
                print("数据已保存，程序退出！")
                break
        else:
            print("无效选项，请输入1-7之间的数字！")

if __name__ == "__main__":
    main_menu()