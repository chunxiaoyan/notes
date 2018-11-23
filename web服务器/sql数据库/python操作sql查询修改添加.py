from pymysql import connect
import  datetime


class ExSQL(object):

    def __init__(self):
        self.conn = connect(host='localhost', port=3306, user='root', password='111111', database='jing_dong', charset='utf8')
        self.cursor = self.conn.cursor()
        self.login_state = False
        self.user_id = None
        self.user_name = None
        self.name = None

    def __del__(self):
        self.cursor.close()
        self.conn.close()


    @staticmethod
    def print_menu():
        print("-------京东-------")
        print("1.所有的商品")
        print("2.所有商品的分类")
        print("3.所有的商品品牌分类")
        print("4.添加一个商品分类")
        print("5.根据名字查询一个商品")
        print("6.注册")
        print("7.登录")
        print("8.下订单")
        return input("请输入功能的序号： ")

    def show_data(self):
        sql = "select * from goods;"
        self.execute_sql(sql)

    def show_cate(self):
        sql = "select * from goods_cates;"
        self.execute_sql(sql)

    def show_brand(self):
        sql = "select * from goods_brands;"
        self.execute_sql(sql)

    def show_orders(self):
        sql = "select * from orders;"
        self.execute_sql(sql)

    def show_customers(self):
        sql = "select * from customers;"
        self.execute_sql(sql)

    def show_order_detail(self):
        sql = "select * from order_detail;"
        self.execute_sql(sql)

    def search_item(self):
        find_name = input("请输入商品名： ")
        sql = 'select * from goods where name=%s'
        self.cursor.execute(sql, [find_name])
        for info in self.cursor.fetchall():
            print(info)

    def add_cate(self):
        add_name = input("请输入商品类名： ")
        sql = "insert into goods_cates values(0,%s)"
        self.cursor.execute(sql, [add_name])
        self.show_cate()
        self.conn.commit()

    def execute_sql(self,sql):
        self.cursor.execute(sql)
        for data in self.cursor.fetchall():
            print(data)

    def register(self):
        print("-----------欢迎注册--------------")
        name = input("请输入姓名： ")
        user_name = input("请输入用户名： ")
        pwd = input("请输入密码： ")
        sql = "insert into customers values(0,%s,%s,%s)"
        self.cursor.execute(sql, [name, user_name, pwd])
        self.show_customers()
        self.conn.commit()

    def login(self):
        print("-----------欢迎登录--------------")
        user_name = input("请输入用户名： ")
        pwd = input("请输入密码： ")
        self.cursor.execute("select * from customers")
        for id, name, usrname, pw in self.cursor.fetchall():
                if user_name == usrname and pwd == str(pw):
                    print("登录成功")
                    return id, name, usrname
        else:
            print("登录失败")
            return False

    def add_order(self):
        time = datetime.datetime.now().strftime("%Y-%m-%d %X")
        sql = "insert into orders values(0,%s,%s)"
        self.cursor.execute(sql, [time, self.user_id])
        self.conn.commit()
        # self.show_orders()
        # 拿出刚添加的id值
        self.cursor.execute("select @@identity")
        order_id = self.cursor.fetchone()[0]
        return order_id

    def add_detail_order(self, good_id, quantity, order_id):
        sql = "insert into order_detail values(0,%s,%s,%s) "
        self.cursor.execute(sql, [order_id, good_id, quantity])
        self.conn.commit()
        # self.show_orders()

    def order(self):
        if self.login_state:
            while True:
                good_id = input("请输入商品id")
                quantity = input("请输入数量（每次订单最多订购5件同样的商品）")
                if int(quantity) >= 5:
                    print("订单失败，最多订购数目为4")
                else:
                    order_id = self.add_order()
                    self.add_detail_order(good_id, quantity, order_id)
                    print("订单成功，订购商品id： %s 数目 %s" % (good_id, quantity))
                if input("添加订单 按1 任意键结束") == 1:
                    pass
                else:
                    break

    def run(self):
        while True:
            num = self.print_menu()
            if num == "1":
                self.show_data()
            elif num == "2":
                self.show_cate()

            elif num == "3":
                self.show_brand()

            elif num == "4":
                self.add_cate()

            elif num == "5":
                self.search_item()

            elif num == "6":
                self.register()

            elif num == "7":
                login_info = self.login()
                if login_info:
                    self.login_state = True
                    self.user_id, self.name, self.user_name = login_info
                    print("你好， %s" % self.name)

            elif num == "8":
                self.order()
            else:
                break


def main():
    session = ExSQL()
    session.run()


if __name__ == '__main__':
    main()
