from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
import selenium.common.exceptions

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options, executable_path=r"D:\mySoftware\chromedriver.exe")
driver1 = webdriver.Chrome(options=chrome_options, executable_path=r"D:\mySoftware\chromedriver.exe")
neg = 0

url = "https://www.icourse163.org/search.htm?search=%E5%8C%97%E4%BA%AC%E9%82%AE%E7%94%B5%E5%A4%A7%E5%AD%A6#/"

driver.get(url)
context = driver.page_source
soup = BeautifulSoup(context, 'html.parser')
courseLIst = soup.find_all('div', {"id": 'j-courseCardListBox'})
courseList = soup.find_all('div', {"class": 'm-course-list'})
courseList1 = courseList[0].find_all('div', {"class": 'ga-click'})
with open("pos.txt", "a", encoding='utf-8') as f:
    for course in courseList1:
        courseTag = course.get('data-href')
        if courseTag[:16] == "/course/undefine":
            continue
        url1 = "https://www.icourse163.org" + courseTag
        print(url1)
        driver1.get(url1)
        detail = driver1.page_source
        soup1 = BeautifulSoup(detail, 'html.parser')
        ele = driver1.find_element_by_id("review-tag-button")  # 模仿浏览器点击查看课程评价的功能
        ele.click()
        try:
            nextPage = driver1.find_element_by_class_name("ux-pager_btn__next")
        except selenium.common.exceptions.NoSuchElementException as e:
            continue

        detail = driver1.page_source
        soup1 = BeautifulSoup(detail, 'html.parser')
        pageNums = driver1.find_element_by_class_name("ux-pager_itm")
        pageNums = soup1.find_all('li', {"class": "ux-pager_itm"})
        pages = 0
        for pOne in pageNums:
            aa = pOne.find_all('a')
            for a in aa:
                if int(a.text) > pages:
                    pages = int(a.text)
        j = 1
        while j < pages:
            print("课程中的第%d页评论" % j)
            connt = driver1.page_source
            soup1 = BeautifulSoup(connt, 'html.parser')
            comment = soup1.find_all('div',
                                     {
                                         'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'})  # 包含全部评论项目的标签
            stars = soup1.find_all('div',
                                   {'class': 'ux-rating-star'})
            index = 1  # stars[0] is stars of course instead of review
            if j > 1:
                for ctt in comment:
                    ratePart = stars[index].find_all('i',
                                                     {'class': 'ux-icon-custom-rating-favorite'})
                    rate = len(ratePart)

                    aspan = ctt.find_all('span')
                    text = re.sub("\n", "", aspan[0].text)
                    if rate < 3:
                        f.write('0' + text + '\n')
                        neg = neg + 1
                    elif rate > 3:
                        f.write('1' + text + '\n')
                        pos = pos + 1
                    index = index + 1  # used in star num
            nextPage.click()
            j = j + 1
        if neg > 1000:
            break
driver.quit()
driver1.quit()
print(neg)
