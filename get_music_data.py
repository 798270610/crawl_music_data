from selenium import webdriver
import csv


# 网易云音乐歌单第一页的url
url = 'https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'
# 用PhantomJS接口创建一个Selenium的WebDriver，参数是phantomjs下载的路径
driver = webdriver.PhantomJS("C:Users\Administrator\AppData\Local\Programs\Python\Python36\Scripts\phantomjs.exe")
# 准备好存储歌单的csv文件
csv_file = open("playlist.csv", "w", newline="")
writer = csv.writer(csv_file)
writer.writerow(['标题', '播放数', '链接'])

# 解析每一页，直到下一页为空
while url !='javascript:void(0)':
    # 用WebDriver加载页面
    driver.get(url)
    # 切换到内容的iframe
    driver.switch_to.frame("contentFrame")
    # 定位歌单标签
    data = driver.find_element_by_id("m-pl-container"). find_elements_by_tag_name("li")
    # 解析每一页的所有歌单
    for i in range(len(data)):
        # 获取播放数
        nb = data[i].find_element_by_class_name("nb").text
        if '万' in nb and int(nb.split("万")[0]) > 500:
            # 获取播放数大于500万的歌单的封面
            msk = data[i].find_element_by_css_selector("a.msk")
            # 把封面上的标题和链接连同播放数一起写到文件中
            title = msk.get_attribute('title').encode("gbk", 'ignore').decode("gbk", 'ignore')
            print(title)
            music_url = msk.get_attribute("href").encode("gbk", 'ignore').decode("gbk", 'ignore')
            print(music_url)
            writer.writerow([title, nb, music_url])

    # 定位'下一页'的url
    url = driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute("href")
    print("Go to next page....")
print("work done!")
csv_file.close()
