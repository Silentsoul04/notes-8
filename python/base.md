# 负数取于问题

```python
print(int(-12/10))
print(-13//10)
print(-13 // -10)
# -1
# -2
# 1
```

“//”是向下取整，“-1.3”会被取成-2，如果想要得到-1，就需要用“/”，然后将结果强制转换为int型。

```python

print(-123%10)
print(-123%-10)

# 7
# -3
```

`-123%10 = -123 - 10 * (-123 // 10) = -123 - 10 * (-13) = 7`

---
# tee

tee没有效果

这是因为python在stdout不是终端时缓冲它。解除缓冲区的最简单方法是使用`python -u`： ？ 没效果

- [tee-does-not-show-output-or-write-to-file](https://stackoverflow.com/questions/27534609/tee-does-not-show-output-or-write-to-file)

---
# pytest

参看覆盖情况： pytest -rA apps/es_sync/uni_advertisement_test.py --cov=apps/es_sync

多个目录： --cov={apps/es_sync,libs}

获取文件： coverage html
获取覆盖率： coverage report --skip-covered | tail -n 3



--------
# pyenv

pyenv versions

pyenv install --list

pyenv install 2.7.6

pyenv-virtualenv

pyenv virtualenvs

制定版本创建virtualenv
pyenv virtualenv 2.7.13 venv27

pyenv virtualenvs

pyenv activate <name>

pyenv deactivate

pyenv uninstall my-virtual-env

pyenv virtualenv-delete my-virtual-env


pyenv global 2.7.3  # 设置全局的 Python 版本，通过将版本号写入 ~/.pyenv/version 文件的方式。

pyenv local 2.7.3  # 设置 Python 本地版本，通过将版本号写入当前目录下的 .python-version 文件的方式。通过这种方式设置的 Python 版本优先级较 global 高。


virtualenv --python=/home/youmi/.pyenv/shims/python venv

---

pip的版本控制:

```
pip install mysqlclient==1.*

# ~=不能控制大版本1。
# 若1.3.14已安装，会进行更新
pip install "mysqlclient~=1.4"

# 安装1.4.6，安装的是1.的最新版本。但1.3.14已安装，不会进行更新
pip install 'mysqlclient~=1.3'

# 安装1.3.14，1.3的最新小版本
pip install 'mysqlclient~=1.3.0'


```

- [how-to-pip-install-a-package-with-min-and-max-version-range](https://stackoverflow.com/questions/8795617/how-to-pip-install-a-package-with-min-and-max-version-range)

卸载yes to all: `pip uninstall -y -r requirements.txt`

---

init-hook="from pylint.config import find_pylintrc; import os, sys; sys.path.append(os.path.dirname(find_pylintrc()))"


# TODO:

- [python下简单实现select和epoll的socket网络编程](http://xiaorui.cc/archives/592)
- [python-threads-synchronization-locks](http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/)
- [《流畅的python》阅读笔记](https://juejin.im/entry/59e4754951882578e27b1e7c)

---
## init new



如果__new__()没有返回cls（即当前类）的实例，那么当前类的__init__()方法是不会被调用的。如果__new__()返回其他类（新式类或经典类均可）的实例，那么只会调用被返回的那个类的构造方法。

通常来说，新式类开始实例化时，__new__()方法会返回cls（cls指代当前类）的实例，然后该类的__init__()方法作为构造方法会接收这个实例（即self）作为自己的第一个参数，**然后依次传入__new__()方法中接收的位置参数和命名参数**

参数是怎么传递的？我能改变传参吗？
You can really only achieve this by writing a metaclass.
The ususal way is to override the __call__ method of the metaclass.

- https://bytes.com/topic/python/answers/751865-modify-arguments-between-__new__-__init__
- https://www.cnblogs.com/ifantastic/p/3175735.html
- [简述 Python 类中的 __init__、__new__、__call__ 方法](https://www.cnblogs.com/bingpan/p/8270487.html)
- [元类](https://www.jianshu.com/p/2e2ee316cfd0)


### 元类
元类的高级编程实现ORM

- [使用元类](https://www.liaoxuefeng.com/wiki/1016959663602400/1017592449371072)


---
### pythonic-way-to-create-a-long-multi-line-string
用括号会好些，用"""""会保留换行符

参考链接:
- [pythonic-way-to-create-a-long-multi-line-string](https://stackoverflow.com/questions/10660435/pythonic-way-to-create-a-long-multi-line-string)

---
### mro
事实上，对于你定义的每一个类，Python 会计算出一个方法解析顺序（Method Resolution Order, MRO）列表，它代表了类继承的顺序。
mro的计算方式是，子类指向父类, 选择入度为0， 从左往右
原因： 单调性问题、只能继承无法重写（override）。具体参考文章《你真的理解Python中MRO算法吗》
mro 先找出入度为0的，也就是不会给其他类继承的，不会给其他类影响，所以可以一直通过这个原则找完。
源代码： https://www.python.org/download/releases/2.3/mro/


- super
super 其实和父类没有实质性的关联。
```
def super(cls, inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]
```
当你使用 super(cls, inst) 时，Python 会在 inst 的 MRO 列表上搜索 cls 的下一个类。

- 多重继承 mixin
将mixin放在多重继承的左边, 然后在mixin的init上通过super去调用下个类的初始化

- init


参考链接：
[你真的理解Python中MRO算法吗？](http://python.jobbole.com/85685/)
[Python: 你不知道的 super](http://python.jobbole.com/86787/)

---
### mysqlclient

3.7.5的python需要安装1.4.0版本的client, 1.3.X版本的会报安装出错
mysqlclient~=1.4.0

https://github.com/django/django/pull/10726
