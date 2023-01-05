## 以下是学习通账号的基本信息
USER = 'xxxx'    # 账号
PASSWORD = 'xxxx'   # 密码

## 以下是一些基本链接
SION_IN_URL = 'http://passport2.chaoxing.com/login?fid=&newversion=true&refer=http://i.chaoxing.com'

# 这些是课程链接（手抓包）
CURRICULUMS = [
    'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?courseid=227761709&clazzid=61522343&cpi=198484053&ut=s&t=1672895932213',
    'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?courseid=227803841&clazzid=61701235&cpi=198484053&ut=s&t=1672891716288',
    'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?courseid=227362167&clazzid=60553366&cpi=198484053&ut=s&t=1672896319870',
]

## 以下是一些XPATH语句

XPATH_SION_IN_URL = '//div[@class="lg-item icon-tel margin-btm24"]/input[@id="phone"]'
XPATH_SION_IN_PASSWORD = '//div[@class="lg-item item-pwd icon-pwd"]/input[@id="pwd"]'
XPATH_SION_IN_BUTTON = '//div[@class="btns-box"]/button[@id="loginBtn"]'
XPATH_CURRICULUM = '//div[@class="catalog_title"]'
XPATH_TITLE = '//div[@class="catalog_level"]/ul/li/div[@class="chapter_item"]'

## 以下时一些基础属性
SLEEP_TIME = 0.5  # 网页延时等待实现
IMPLICITLY_WAIT = 10    # 隐式等待时间
