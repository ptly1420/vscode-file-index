import random
import string
import pymysql
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# 数据库连接配置
config = {
    'host': 'rm-3nsp52wa21da228e7co.mysql.rds.aliyuncs.com',
    'user': 'rambo',
    'password': 'Tianying12345$',
    'db': 'testdb_new'
}

# 生成随机字符串函数
def random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# 修改插入数据函数中的生成随机字符串调用


# 插入数据函数
def insert_data():
    try:
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            # 生成随机数据
            text = random_string(100)
            uname = random_string(10)
            update_time = datetime.now()
            
            # 打印即将插入的数据
            print(f"Preparing to insert: text={text}, uname={uname}, update_time={update_time}")
            
            # 执行SQL语句
            sql = "INSERT INTO `tt` (`text`, `uname`, `update_time`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (text, uname, update_time))
            connection.commit()  # 提交事务移到这里，确保每次插入都提交
            
            print(f"Successfully inserted: text={text}, uname={uname}, update_time={update_time}")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
    finally:
        if connection:
            connection.close()

# 使用多线程插入数据
def main():
    num_threads = 10  # 线程数可以根据实际情况调整
    total_inserts = 100000  # 总共要插入的数据行数

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(total_inserts):
            executor.submit(insert_data)

if __name__ == "__main__":
    main()