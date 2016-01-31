#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import thread
import time

# 糗事百科爬虫类
class QSBKSpider:

	# 初始化方法
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
		self.headers = { 'User-Agent' : self.user_agent }
		# 存放段子，一个元素是每一页的一个纯文本段子
		self.stories = []
		self.enable = False

	# 传入页面索引，获取页面代码
	def getPage(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			content = response.read().decode('utf-8')
			return content
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接糗事百科失败，原因：", e.reason
				return None

	# 传入页面索引，获取本页纯文本的段子列表
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "页面加载失败..."
			return None
		pattern = re.compile('<div.*?author.*?">.*?<a.*?<img.*?alt="(.*?)".*?</a>.*?<div.*?content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
		items = re.findall(pattern, pageCode)
		pageStories = []
		for item in items:
			haveImg = re.search("img", item[3])
			if not haveImg:
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR, "\n", item[1])
				# item[0]是一个段子的发布者
				# item[1]是内容
				# item[2]是发布时间
				# item[3]是段子的附图
				# item[4]是点赞数
				pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[4].strip()])
		return pageStories

	# 加载并提取页面内容，加入到列表中
	def loadPage(self):
		# 如果当前未看的页数少于2页，则加载新一页
		if self.enable == True:
			if len(self.stories) < 2:
				# 获取新一页
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	# 每次按回车打印出一个段子
	def getOneStory(self, pageStories, page):
		for story in pageStories:
			# 等待用户的输入
			input = raw_input()
			self.loadPage()
			# 如果输入Q则程序结束
			if input == "q" or input == 'Q':
				self.enable = False
				return
			print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" % (page, story[0], story[2], story[3], story[1])

	# 启动程序
	def start(self):
		print u"正在读取糗事百科，按回车查看新段子，Q退出"
		self.enable = True
		# 先加载一页内容
		self.loadPage()
		curPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				curPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, curPage)

# 开始爬啦
spider = QSBKSpider()
spider.start()
