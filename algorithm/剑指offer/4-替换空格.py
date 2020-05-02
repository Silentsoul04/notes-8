#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"a b c" 替换空格
for 查找空格
    替换成"XXX", 长度不一样，所以要移动后面的字符。复杂度为 o(n^2)

先遍历计算替换后的长度，再建立另一个字符，用空间换取时间

剑指offer的思路是，新旧的都是在，string [] 里面，也就是容量已经是支持新的长度。然后从后面进行遍历，后移动相应的字符。
"""