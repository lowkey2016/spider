#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import thread
import math
import bs4
from bs4 import BeautifulSoup
import os
import shutil
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# http://www.du114.com/

## 114图库女神图集的爬虫类 ##
class Pics114Spider:

	## 初始化方法 ##
	def __init__(self, fav_girl_name, allcols_html_url):
		self.fav_girl_name = fav_girl_name
		self.allcols_html_url = allcols_html_url
		self.pics_delta = 10


	## 获取女神的图集存放的目录 ##
	def get_fav_girl_dir(self, folder_name):
		folder_dir = './%s' % (folder_name)
		if os.path.exists(folder_dir) == False:
			os.mkdir(folder_dir)
		return folder_dir


	## 获取女神某一个图集的目录 ##
	def get_collection_dir(self, folder_name, collection_name):
		root_dir = self.get_fav_girl_dir(folder_name)
		col_dir = '%s/%s' % (root_dir, collection_name)
		if os.path.exists(col_dir) == False:
			os.mkdir(col_dir)
		return col_dir


	## 获取一个网页的 HTML 内容 ##
	def get_html_with_url(self, src_url):
		try:
			request = urllib2.Request(src_url)
			response = urllib2.urlopen(request)
			data = response.read()
			return data
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"打开 %s 失败，原因：%s" % (src_url, e.reason)
				return None


	## 下载网络的文件到磁盘 ##
	def save_file_with_url(self, src_url, des_path):
		# 如果文件已经存在并且文件大小大于 10KB ，就假定其已经下载好
		if os.path.exists(des_path) and os.path.getsize(des_path) > 10000:
			# 已经下载好的不再重复下载
			print 'save %s to %s succ' % (src_url, des_path)
			return True
		else:
			try:
				request = urllib2.Request(src_url)
				response = urllib2.urlopen(request)
				data = response.read()
				if data:
					f = open(des_path, 'wb')
					f.write(data)
					f.close()
					print 'save %s to %s succ' % (src_url, des_path)
					return True
				else:
					print 'save %s to %s fail' % (src_url, des_path)
					return False
			except urllib2.URLError, e:
				if hasattr(e, "reason"):
					print u"打开 %s 失败，原因：%s" % (src_url, e.reason)
					return False


	## 保存女神的封面 ##
	def save_fav_girl_cover(self, fav_girl_name, cover_url):
		if cover_url.endswith('.png'):
			cover_name = 'cover.png'
		else:
			cover_name = 'cover.jpg'
		des_path = '%s/%s' % (self.get_fav_girl_dir(fav_girl_name), cover_name)
		request = urllib2.Request(cover_url)
		response = urllib2.urlopen(request)
		data = response.read()
		if data:
			f = open(des_path, 'wb')
			f.write(data)
			f.close()
			print 'save %s succ' % des_path
		else:
			print 'save %s fail' % des_path


	## 保存女神的资料 ##
	def save_fav_girl_profile(self, fav_girl_name, profile_str):
		des_path = '%s/profile.txt' % (self.get_fav_girl_dir(fav_girl_name))
		if profile_str:
			f = open(des_path, 'wb')
			f.write(profile_str.encode('utf-8'))
			f.close()
			print 'save %s succ' % des_path
		else:
			print 'save %s fail' % des_path


	## 爬取每一个网页里的女神图片 ##
	def get_content_pic_of_url(self, html_url, page_index, collection_dir):
		# 获取 Base URL
		last_comp = html_url.split('/')[-1]
		baseurl = html_url.replace(last_comp, '')
		html = self.get_html_with_url(html_url)
		if last_comp.endswith('.html'):
			last_comp = last_comp.replace('.html', '')
		col_id = last_comp.split('_')[0]

		# 获取下一页的链接
		# 获取本页的图片内容
		pattern = re.compile('<div class="articleBody" id="picBody">.*?<a href=\'(.*?)\'><img alt=.*?src="(.*?)".*?</div>', re.S)
		items = re.findall(pattern, html)
		for item in items:
			next_url_ref = item[0]
			pic_url = item[1]
			break

		# 下载图片，然后跳到下一页
		des_name = '%d.jpg' % page_index
		des_path = '%s/%s' % (collection_dir, des_name)
		self.save_file_with_url(pic_url, des_path)

		next_url = os.path.join(baseurl, next_url_ref)
		if next_url_ref and next_url_ref.startswith(col_id):
			self.get_content_pic_of_url(next_url, (page_index + 1), collection_dir)


	## 爬取一个集合里的所有图片 ##
	def get_pics_of_collection(self, root_name, html_url):
		collection_name = ''
		collection_dir = ''
		collection_pages = 0

		# 读取html
		try:
			html_req = urllib2.Request(html_url)
			html_resp = urllib2.urlopen(html_req)
			html_content = html_resp.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接114图库失败，原因：", e.reason

		# 获取网页标题（用于新建目录）
		soup = BeautifulSoup(html_content, "lxml")
		html_title = soup.title.string
		collection_name = html_title

		# 获取图片页数
		pattern = re.compile('<div class="pages">.*?共(.*?)页:.*?</div>'.decode('utf-8'), re.S)
		items = re.findall(pattern, html_content)
		for item in items:
			collection_pages = int(item)
			# 加1个越界值，因为页数可能显示不完整
			collection_pages += self.pics_delta
			break

		# 获取 jpg 的 base 链接
		img_baseurl = ''
		pattern = re.compile('<div class="articleBody" id="picBody">.*?<img alt.*?src="(.*?)".*?</div>', re.S)
		items = re.findall(pattern, html_content)
		for item in items:
			img_baseurl = item
			last_comp = img_baseurl.split('/')[-1]
			img_baseurl = img_baseurl.replace(last_comp, '')
			break

		# 获取存放图片文件的目录
		collection_dir = self.get_collection_dir(root_name, collection_name)

		# 遍历页数，爬取所有图片
		is_rule_valid = False
		for i in range(1, collection_pages):
			des_name = '%d.jpg' % i
			des_path = '%s/%s' % (collection_dir, des_name)
			src_url = "%s%d.jpg" % (img_baseurl, i)
			save_succ = self.save_file_with_url(src_url, des_path)
			# 只要其中一条规则生效，就假定 BaseURL + i.jpg 这种规则是有效的
			if is_rule_valid == False and save_succ:
				is_rule_valid = True

		# 如果 BaseURL + i.jpg 这种规则失效，就换一种规则爬
		if is_rule_valid == False:
			self.get_content_pic_of_url(html_url, 1, collection_dir)
		# 如果 BaseURL + i.jpg 规则失效，并且还没全部下载好，需要断点续爬
		# 防那种规则不对，但是又还没下载完整的情况
		last_imgname = '%d.jpg' % (collection_pages - self.pics_delta)
		last_imgpath = '%s/%s' % (collection_dir, last_imgname)
		if os.path.exists(last_imgpath) == False:
			self.get_content_pic_of_url(html_url, 1, collection_dir)


	## 根据女神获取其所有集合 ##
	def get_all_collections(self):
		# 读取所有集合的html
		fav_girl_name = self.fav_girl_name
		allcols_html_url = self.allcols_html_url
		try:
			allcols_html_req = urllib2.Request(allcols_html_url)
			allcols_html_resp = urllib2.urlopen(allcols_html_req)
			allcols_html_content = allcols_html_resp.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接女神所有图集网页失败，原因：", e.reason
		
		# 获取封面
		pattern = re.compile('<body style="background:url\((.*?)\) no-repeat.*?px;">', re.S)
		items = re.findall(pattern, allcols_html_content)
		for item in items:
			fav_girl_cover_url = item
			self.save_fav_girl_cover(fav_girl_name, fav_girl_cover_url)
			break

		# 爬取基本资料并写到信息文件中
		pattern = re.compile('<div class="top_content">.*?<p class="sp-icent">(.*?)</p>.*?</div>'.decode('utf-8'), re.S)
		items = re.findall(pattern, allcols_html_content)
		for item in items:
			fav_girl_profile = item
			self.save_fav_girl_profile(fav_girl_name, fav_girl_profile)
			break

		# 获取所有集合的链接
		pattern = re.compile('<div class="listBox" id="imgList">.*?<ul class="liL">(.*?)</ul></div>', re.S)
		items = re.findall(pattern, allcols_html_content)
		for item in items:
			cols_content = item
			break
		pattern = re.compile('<li><a href="(.*?)".*?</a><span.*?<a target=.*?</a></span></li>', re.S)
		items = re.findall(pattern, cols_content)
		for item in items:
			collection_url = item
			self.get_pics_of_collection(fav_girl_name, collection_url)


# 开始爬

# Succ

# 夏沫GiGi
# spider = Pics114Spider('夏沫GiGi', 'http://www.du114.com/tag/1289.html')

# Vian熙芸
# spider = Pics114Spider('Vian熙芸', 'http://www.du114.com/tag/1718.html')

# 陈思琪
# spider = Pics114Spider('陈思琪', 'http://www.du114.com/tag/1554.html')

# 李七喜
# spider = Pics114Spider('李七喜', 'http://www.du114.com/tag/1226.html')

# # 米妮
# spider = Pics114Spider('米妮', 'http://www.du114.com/tag/1301.html')

# 杉原杏璃
# spider = Pics114Spider('杉原杏璃', 'http://www.du114.com/tag/1231.html')

# 夏瑶
# spider = Pics114Spider('夏瑶', 'http://www.du114.com/tag/1290.html')

# 诗朵雅
# spider = Pics114Spider('诗朵雅', 'http://www.du114.com/tag/1230.html')

# 杨晓青儿
# spider = Pics114Spider('杨晓青儿', 'http://www.du114.com/tag/1212.html') 

# 爬取某个女神的所有图集
# spider.get_all_collections()

# 爬取某个图集
# spider = Pics114Spider('', '')
# spider.get_pics_of_collection('张圆圆', 'http://www.du114.com/meinvtupian/nayimeinv/74341.html')
