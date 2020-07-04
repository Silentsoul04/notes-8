---
# web

## [csrf](csrf.md)

- 什么是跨域请求
- 跨域请求的安全问题
- csrf攻击
  - [限制跨域请求](安全.md)
  - 需要注意form表单是安全的，也就导致了form表单的攻击场景
  - 如何防止跨域请求
- django的csrf的源码解析
  - 随机secret和salt hash方式加密生成csrftoken
  - 随机secret和salt hash方式加密生成隐藏csrfmiddlewaretoken字段
  - secret而不是完整的token与cookie值中的secret进行比较
  - 一些问题和解答。
    - 避免重放攻击
    - 前后端分离如何避免。JWT不应该放在cookie里面。引出实际的安全漏洞
    - 可以任意伪造，是否是漏洞
  - 实际项目的使用与漏洞

## [安全](csrf.md)

- xss跨站脚本攻击。输入框文本检测、输出纯文本
- csrf
- 点击劫持

## [JWT](jwt.md)

- 组成部分 Header、claim、signature
- 优势
- 劣势
- 自身项目使用情况
