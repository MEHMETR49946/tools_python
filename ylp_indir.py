from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from ylp_UserInfo import username,password, save_path_cm
import urllib.request
import os
import sys
import easygui


class Ylp:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.five_courses = []
        self.chrome = "C:\\Python37\\selenium_drivers\\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
                                                    "download.default_directory": save_path_cm , #Change default directory for downloads
                                                    "download.prompt_for_download": False, #To auto download the file
                                                    "download.directory_upgrade": True,
                                                    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
                                                    })
        self.browser = webdriver.Chrome(self.chrome, options=options)#, options=chrome_options)
    def login(self):
        login_f1 = "http://yukseklisans.online/"
        login_buton = '/html/body/div[1]/div[2]/header/div/nav/ul[1]/li/a/span'
        self.browser.get(login_f1)
        time.sleep(3)
        self.browser.find_element_by_xpath(login_buton).click()
        ### -----------
        time.sleep(2)
        self.browser.find_element_by_css_selector("input[name=username]").send_keys(self.username)
        self.browser.find_element_by_tag_name("input[name=password]").send_keys(self.password)
        self.browser.find_element_by_tag_name("input[name=password]").send_keys(Keys.ENTER)
    def getCourses(self):
        time.sleep(2)
        courses = self.browser.find_elements_by_css_selector("div[class=tc_content]")
        
        for course in courses:
            self.five_courses.append(course.text)
        self.five_courses = self.five_courses[-5:]
        self.courses_list = []
        syc = 1
        for i in self.five_courses:
            print(f"{syc}- "+i.split("\n")[-1])
            self.courses_list.append(i.split("\n")[-1])
            syc+=1
        
    def previewCourse(self):
        time.sleep(2)
        self.course_index = 0
        self.course_index = int(input("Kurs Seçiniz: "))
        buton = self.browser.find_element_by_xpath(f"//*[text()='{self.courses_list[self.course_index-1]}']")
        buton.click()


    def ders_kayitlarini_indir(self):
        try:
            self.browser.find_element_by_xpath(f"//*[text()='CANLI DERS ']").click()
        except :
            self.browser.find_element_by_xpath(f"//*[text()='CANLI DERS']").click()
        time.sleep(0.2)
        try:
            self.browser.find_element_by_css_selector("[div[class=activityinstance]").click()
        except:
            self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[5]/div[3]/div[2]/div/div/div/div/div/div/div/div[2]/div/li[2]/div/div/div[2]/div/div[3]/ul/li/div/div/div[2]/div[1]/a').click()
        time.sleep(3)
        presentations = self.browser.find_elements_by_xpath(f"//*[text()='Presentation']") # sunum tuşlarını getir
        time.sleep(2)
        ders_ids = []
        for presentation in presentations: # derlerin id'lerini getir
            ders_id = presentation.get_attribute("id")
            ders_id = ders_id.split("-")[-2:]
            ders_id = ders_id[0]+"-"+ders_id[1]
            ders_ids.append(ders_id)

        # kaç ders var başka bir yoldan da bak çaprazlama
        kac_ders_kaydı = self.browser.find_element_by_css_selector("tbody[class=yui3-datatable-data]")
        kac_ders_kaydı = kac_ders_kaydı.find_elements_by_css_selector("tr")

        if len(kac_ders_kaydı) == 0:
            print("ders kaydı bulunmuyor.")
            return
                
        print(f"{len(kac_ders_kaydı)} adet ders kaydı bulundu. Tarihleri:")
        video_names = []

        # derslerin kaydedilecek isimlerini oluştur
        for i in range(len(kac_ders_kaydı)):
            dd = kac_ders_kaydı[i].find_elements_by_css_selector("td")
            date = dd[-2].text
            print(f"{i+1} --> "+date)
            video_names.append( (self.current_ders_adi.replace(" ", "_")+ "_" +date.replace(" ", "_")))
 
        choice_lesson = int(input("İndirilecek olan dersi seçiniz: "))
        lesson_number = choice_lesson-1
        ders_ids = ders_ids[lesson_number] #1 = 0, 2 = 1 ...
        if choice_lesson == 0:
            return
        syc = 0
        while True:
            if syc == 1:
                return
            video = f"https://netkampus.site/presentation/{ders_ids}/deskshare/deskshare.webm"
            audio = f"https://netkampus.site/presentation/{ders_ids}/video/webcams.webm"
            time.sleep(0.5)
            # self.browser.get(video)
            # time.sleep(0.5)
            save_path = easygui.diropenbox()
            os.chdir(save_path)
            print(save_path)
            print(f"{lesson_number+1} indiriliyor...")
            try:
                urllib.request.urlretrieve(video, "video.webm")
            except:
                print("video indirilemiyor :(")
                break

            time.sleep(0.5)
            urllib.request.urlretrieve(audio, "audio.webm")
            print(os.getcwd())
            print(video_names[lesson_number])
            print(f"ffmpeg -i audio.webm -i video.webm {video_names[lesson_number]}.mp4")
            os.system(f"ffmpeg -i audio.webm -i video.webm {video_names[lesson_number]}.mp4")
            syc += 1


    def calisma_notlarini_indir(self):
        self.browser.find_element_by_css_selector("li[id=section-2]").click()
        ders_notlari = self.browser.find_element_by_css_selector("div[id=panel-2]")
        ders_notlari = ders_notlari.find_element_by_css_selector("ul")
        ders_notlari = ders_notlari.find_elements_by_css_selector("li")
        for li in ders_notlari:
            li.find_element_by_css_selector("span[class=instancename]").click()
        
    def calisma_sorularini_indir(self):
        self.browser.find_element_by_css_selector("li[id=section-3]").click()
        ders_notlari = self.browser.find_element_by_css_selector("div[id=panel-3]")
        ders_notlari = ders_notlari.find_element_by_css_selector("ul")
        ders_notlari = ders_notlari.find_elements_by_css_selector("li")
        for li in ders_notlari:
            file_d = li.find_element_by_css_selector("span[class=instancename]")
            print(file_d.text)
            file_d.click()
    def indir(self):
        self.current_ders_adi = self.courses_list[self.course_index-1]
        os.system("cls")
        print(self.current_ders_adi+" dersi seçildi.")

        while True:
            print("""
1- Ders Kayıtlarını indir
2- Calışma Notlarını indir
3- Çalışma Sorularını indir""")
            scn = 123
            scn = int(input(": "))
            # Fonksiyonlar FALSE döndürmedikçe işlemleri bitince geri çıkmış oluyorlar.
            if scn == 1:
                self.ders_kayitlarini_indir()
                self.browser.back()
                time.sleep(2)
                os.system("cls")
            elif scn == 2:
                self.calisma_notlarini_indir()
                os.system("cls")
                print(f"dosyalar {save_path_cm} konumuna indirildi.")
            elif scn == 3:
                self.calisma_sorularini_indir()
                os.system("cls")
                print(f"dosyalar {save_path_cm} konumuna indirildi.")
            else:
                if scn == 0:
                    self.browser.back()
                    os.system("cls")
                    syc = 1
                    for course in self.courses_list:
                        print(f"{syc}- {course}")
                        syc+=1
                    self.previewCourse()
                else:
                    print("girdiğiniz değeri kontrol ediniz")
                    continue


ylp = Ylp(username, password)
ylp.login()
ylp.getCourses()
ylp.previewCourse()
ylp.indir()

