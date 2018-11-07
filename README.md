# Sort-images-by-character
Sort images by character  
按照人物分类来区分图片
## 图片自动按人分文件夹
#### 原理
	+ 1. tx的人脸识别 , 需要联网
	+ 2. 基于python
	+ 3. 多人识别暂未写
#### 使用方法
	拖入文件夹到控制台, 回车, 会自动在 "原目录class" 文件夹中生成目录和
#### 使用注意	
	1. 如果想要独立的识别库, 使用前请自己开通人脸识别下的所有项目(https://console.cloud.tencent.com/ai/facialrecognition/analysis)并申请appid, secret_id, secret_key(https://console.cloud.tencent.com/cam/capi)并填入到config.conf中
	2. 如果不自己申请, 多人同时操作是可能导致识别错误
	3. 默认多次识别并需要保留识别库, 如果要清除识别库-> 请输入"cp"
	4. 相似度默认设置为 70 以上算是一个人, 这个自己在config.conf中调节, 改完需要重启软件+
####图片示例
	![图片示例](http://thyrsi.com/t6/413/1541567225x-1404817712.jpg)
	
	链接: https://pan.baidu.com/s/1WpsMySOvi3nN-4uYBW9Y6Q 提取码: exje 
