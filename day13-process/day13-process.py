#join函数是等待主进程结束，之后的代码不会再继续乡下执行了，p1和p2是两个子进程，已经创建过了，会继续

#多进程使用使用multiprocessing模块中的Queue类 进程间通信

#线程之间共享进程的内存空间，但是多个进程访问数据会导致数据临界，访问是对数据加锁
#初始函数里新建一个Lock（）
#在对加锁数据进行访问的时候，先self._lock.acquire()，self._lock.release()

# from time import sleep
# from threading import Thread,Lock
#
#
# class Account(object):
#
#     def __init__(self):
#         self._balance = 0
#         self._lock = Lock()
#
#     def deposit(self, money):
#         # 计算存款后的余额
#         self._lock.acquire()
#         new_balance = self._balance + money
#         # 模拟受理存款业务需要0.01秒的时间
#         sleep(0.01)
#         # 修改账户余额
#         self._balance = new_balance
#         self._lock.release()
#
#     @property
#     def balance(self):
#         return self._balance
#
#
# class AddMoneyThread(Thread):
#
#     def __init__(self, account, money):
#         super().__init__()
#         self._account = account
#         self._money = money
#
#     def run(self):
#         self._account.deposit(self._money)
#
#
# def main():
#     account = Account()
#     threads = []
#     # 创建100个存款的线程向同一个账户中存钱
#     for _ in range(100):
#         t = AddMoneyThread(account, 1)
#         threads.append(t)
#         # sleep(0.1)
#         t.start()
#     # 等所有存款的线程都执行完毕
#     for t in threads:
#         t.join()
#     print('账户余额为: ￥%d元' % account.balance)
#
#
# if __name__ == '__main__':
#     main()


from time import time


def main():
    total = 0
    number_list = [x for x in range(1, 10000000)]
    start = time()
    for number in number_list:
        total += number
    print(total)
    end = time()
    print('Execution time: %.3fs' % (end - start))


if __name__ == '__main__':
    main()