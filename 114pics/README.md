# 114 女神图库小爬虫

## 使用说明

方式一:

前往[114图库](http://www.du114.com/) ，搜到你喜欢的图集，然后配置下 **114pic.py** ，示例代码：

```
# 爬取某个图集
spider = Pics114Spider('', '')
spider.get_pics_of_collection('美女', 'http://www.du114.com/meinvtupian/rentiyishu/83724.html')
```

方式二:

如果要爬取女神 xiayao 的所有图集，先搜到女神的所有图集页面，配置代码示例：

```
# 夏瑶
# spider = Pics114Spider('夏瑶', 'http://www.du114.com/tag/1290.html')
```

然后运行 **114pic.py** ，爬到的图片会保存在当前目录下。

>
> 注：
> 
> 1. 如果爬虫检测到图片已经下载过，就不会重新下载
> 
> 2. 由于使用了一些规则，所以如果每个图集的图片数为10，那么爬虫会尝试读到19，确保不会漏掉每一张图片，但是如果图片本身不存在，爬虫会显示 save fail 的 log ，这是正常的

最后更新：2016.02.05
