#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
1. 通过__new___和hasattr进行判断， 主要语句：cls._instance = super().__new__(cls)
2. 通过装饰器进行实现，设立一个字典，判断是否存在，存在则直接获取
3. 装饰器加上线程锁
"""
# ref: https://blog.csdn.net/qq_33733970/article/details/78792656

#
# class Singleton:
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, '_instance'):
#             cls._instance = super().__new__(cls)
#         return cls._instance
#
#     def __init__(self, a):
#         self.a = a
# s0 = Singleton(a=1)
# s1 = Singleton(a=2)
# print(s0.a)
# print(s1.a)
# print(id(s0))
# print(id(s1))


from functools import wraps


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


@singleton
class Bar:
    pass


b0 = Bar()
b1 = Bar()
print(id(b0))
print(id(b1))

# 线程安全
#  https://stackoverflow.com/a/50567397
#  https://blog.csdn.net/lucky404/article/details/79668131

print('-'*30)
import threading


def synchronized(func):

    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return lock_func


class Singleton(object):
    """
    单例模式
    """
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance
s0 = Singleton(a=1)
s1 = Singleton(a=2)
# print(s0.a)
# print(s1.a)
print(id(s0))
print(id(s1))