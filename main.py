from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import shutil
from selenium.webdriver.common.keys import Keys
import random
from playsound import playsound
# import app


class GroupPage:
    def __init__(self, groupID):
        self.driver = webdriver.Chrome()
        self.userGroup = groupID

    def go_to_Facebook(self):
        self.driver.get("https://mbasic.facebook.com")

    def go_to_GroupPage(self):
        self.driver.get("https://www.facebook.com/groups/" + self.userGroup + "/media/photos")

    def select_cookies(self):
        wait = WebDriverWait(self.driver, 10)
        cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Decline optional cookies']")))
        cookie_button.click()

    def access_First_Image(self):
        mediaTable = 'x78zum5 x1q0g3np x1a02dak'
        mediaPhotos = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div/a/img')
        mediaPhotos.click()

    def getImageURL(self):
        wait = WebDriverWait(self.driver, 60)
        image = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'x1bwycvy.x193iq5w.x4fas0m.x19kjcj4')))
        try:
            imageURL = image.get_attribute('src')
        except:
            playsound('alarma.mp3')
            time.sleep(500)
            print("An exception occurred")
        return imageURL

    def nextImagePage(self):
        arrowRightButton = self.driver.find_element(By.TAG_NAME , 'body')
        arrowRightButton.send_keys(Keys.ARROW_RIGHT)

    def getPageURL(self):
        return self.driver.current_url

    def checkIfPhoto(self, currentLink):
        link = currentLink[:30]
        words = link.split('/')
        print(words)
        return words[-1] == "photo" + str(imageNo)

class FileManager:
    def __init__(self,folderNo):
        self.projectDir = './imagesFolder'
        self.folderNo = folderNo
        self.current_dir = os.getcwd()

    def makeDIR(self, groupID):
        if not self.folderNo:
            if not os.path.exists(self.projectDir):
                print("empty")
                os.makedirs(os.path.join(self.current_dir, self.projectDir, f"1_{grupID}"))
                numberWeShouldUse = 1
                print(f'created dir no: {numberWeShouldUse}')
                return os.path.join(self.current_dir, self.projectDir, f"1_{grupID}")
            else:
                dir_list = os.listdir(self.projectDir)
                dir_list.sort(key=lambda x: os.stat(os.path.join(self.projectDir, x)).st_mtime)
                dirNumber = len(dir_list)
                numberWeShouldUse = dirNumber + 1
                os.makedirs(os.path.join(self.projectDir, str(numberWeShouldUse) + "_" + groupID))
                print(f'created dir no: {numberWeShouldUse}')
                return os.path.join(self.projectDir, str(numberWeShouldUse) + "_" + groupID)

    def downloadImage(self, URL, location, numberImage):
                imageTrueName = "/img" + str(numberImage) + ".png"
                # Open the url image, set stream to True, this will return the stream content.
                r = requests.get(URL, stream=True)
                # Check if the image was retrieved successfully
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True
                    # Open a local file with wb ( write binary ) permission.
                    with open(location + imageTrueName, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    print('Image sucessfully Downloaded: ', location + imageTrueName)
                else:
                    print('Image Couldn\'t be retreived')


class LoginPage:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def go_to_login_page(self):
        self.driver.get("https://mbasic.facebook.com/")

    def select_cookies(self):
        cookie_button = self.driver.find_element(By.XPATH, '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div')
        cookie_button.click()
    def enter_email(self, email):
        username_field = self.driver.find_element(By.ID, "m_login_email")
        username_field.send_keys(email)

    def enter_password(self, password):
        password_field = self.driver.find_element(By.XPATH, '//*[@id="password_input_with_placeholder"]/input')
        password_field.send_keys(password)

    def press_submit(self):
        button = self.driver.find_element(By.XPATH, '//*[@id="login_form"]/ul/li[3]/input')
        button.click()


lastURL = ''

if __name__ == '__main__':
    folderNo = ''

    grupID = str(input("Group ID"))

    directory = FileManager(folderNo)
    location = directory.makeDIR(grupID)

    scrapPage = GroupPage(grupID)

    scrapPage.go_to_GroupPage()
    scrapPage.select_cookies()
    time.sleep(1)
    scrapPage.access_First_Image()
    time.sleep(1)
    imageNo = 0
    pageURL = scrapPage.getPageURL()
    loopEndURL = ''
    current_url = ''

    # use current driver url to check if current accesed file is video/picture, if not->skip.

    def loopThroughGroupPhotos(currentPage):
        #ad condition to wait until link has changed from line 152
        url = ''
        global lastURL
        if scrapPage.checkIfPhoto(str(currentPage)):
            url = scrapPage.getImageURL()
            if url == lastURL:
                return ''
            lastURL = url
            if url == loopEndURL and url:
                return 'loopCompleted'
            print(url)
            directory.downloadImage(url, location, imageNo)
        time.sleep(random.choice([.1, .2, .5, .7, .9]))
        scrapPage.nextImagePage()
        time.sleep(random.choice([.1, .2, .5, .7, .9]))
        return url


    while not loopEndURL:
        pageURL = scrapPage.getPageURL()
        loopEndURL =  loopThroughGroupPhotos(pageURL)
        imageNo += 1

    while current_url != 'loopCompleted':
        pageURL = scrapPage.getPageURL()
        current_url = loopThroughGroupPhotos(pageURL)
        if current_url == '':
            continue
        imageNo +=1
        # LAST UPDATE 

# use mbasic version headless to see how many img are in the group and download images until target is met





