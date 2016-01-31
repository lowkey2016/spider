#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bs4
from bs4 import BeautifulSoup
import re

# html = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# <p class="story">...</p>
# """
# soup = BeautifulSoup(html, "lxml")
soup = BeautifulSoup(open('bs_index.html'), "lxml")
# print soup.prettify()


## 五、四大对象种类 ##

# 1. Tag
# 获取标签对象
# print soup.title
# print soup.head
# print soup.a
# print soup.p
# print type(soup.a)
# 获取标签的name
# print soup.name
# print soup.head.name
# print soup.p.name

# 获取标签的attrs
# print soup.p.attrs
# print soup.p['class']
# print soup.p.get('class')
# soup.p['class'] = "newClass"
# print soup.p
# del soup.p['class']
# print soup.p

# 2. NavigableString
# print soup.p.string
# print type(soup.p.string)

# 3. BeautifulSoup
# print type(soup.name)
# print soup.name
# print soup.attrs

# 4. Comment
# print soup.a
# print soup.a.string
# print type(soup.a.string)
# if type(soup.a.string) == bs4.element.Comment:
# 	print '<!--' + soup.a.string + '-->'


## 六、遍历文档树 ##

# 1. .contents
# print soup.body.contents
# print soup.body.contents[0]

# 2. .children
# print soup.body.children
# for child in soup.body.children:
# 	print child

# 3. .descendants
# for child in soup.descendants:
# 	print child

# 4. .string
# print soup.head.string
# print soup.title.string
# print soup.body.string

# 5. .strings
# for string in soup.head.strings:
# 	print(repr(string))
# for string in soup.strings:
# 	print(repr(string))

# 6. .stripped_strings
# for string in soup.stripped_strings:
# 	print repr(string)

# 7. .parent
# p = soup.p
# print p.parent.name
# content = soup.head.title.string
# print content.parent.name

# 8. .parents
# content = soup.head.title.string
# for parent in content.parents:
# 	print parent.name


## 七、搜索文档树 ##

# print soup.find_all('a')

# for tag in soup.find_all(re.compile('^b')):
# 	print tag.name

# print soup.find_all(['a', 'b'])

# for tag in soup.find_all(True):
# 	print tag.name

# def has_class_but_no_id(tag):
#     return tag.has_attr('class') and not tag.has_attr('id')
# print soup.find_all(has_class_but_no_id)

# print soup.find_all(id = 'link2')
# print soup.find_all(href = re.compile('elsie'))
# print soup.find_all(id = 'link1', href = re.compile('elsie'))
# print soup.find_all('a', class_ = 'sister')
# print soup.find_all(attrs = {"class" : "sister"})

# print soup.find_all(text="Elsie")
# print soup.find_all(text=["Tillie", "Elsie", "Lacie"]) 
# print soup.find_all(text=re.compile("Dormouse"))
# print soup.find_all("a", limit=2)
# print soup.html.find_all("title")
# print soup.html.find_all("title", recursive=False)


## 八、CSS选择器 ##

# # 标签名
# print soup.select('title') 

# # 标签的类名
# print soup.select('.sister')

# # 标签的id名
# print soup.select('#link1')

# # 组合
# print soup.select('p #link1')

# # 子标签
# print soup.select("head > title")

# # 标签的属性
# print soup.select('a[href="http://example.com/elsie"]')
# print soup.select('p a[href="http://example.com/elsie"]')
