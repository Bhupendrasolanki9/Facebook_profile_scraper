import pandas as pd
from facebook_scraper import get_posts
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import requests
import os
import datetime

def facebook_page(driver):
    driver.get("https://www.facebook.com/login")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    driver.maximize_window()

def videosfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/videos")
        time.sleep(3)
        item = []
        wait =WebDriverWait(driver,10)
        video_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="bi6gxh9e"]/div/div/div/div/a')))
        for i in video_links:
            video_link = i.get_attribute('href')
            complete_data={
                "videolink":video_link
            }
            item.append(complete_data)
        print(item)
        return item
    except:
        print("Videos Link Not Found")
        data = []
        return data

def checkinsfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/map")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=map")
        time.sleep(3)
        item =[]
        wait =WebDriverWait(driver,10)
        try:
            checkins_places = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_6s5d _71pn _-kb segoe"]/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')))
            checkin_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[2]/span/div/div[2]')))
            checkins_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[1]/a')))
            for cp,cd,cl in zip(checkins_places,checkin_dates,checkins_links):
                complete_data = {
                    'checkinlinks':cl.get_attribute('href'),
                    'placedetails':cp.text,
                    'date':cd.text}
                item.append(complete_data)
            return item
        except:
            checkins_places = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_6s5d _71pn _-kb segoe"]/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')))
        # checkin_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_q8"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[2]/span/div/div[2]')))
            checkins_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_q8"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[1]/a')))
            for cp,cl in zip(checkins_places,checkins_links):
                complete_data = {
                    'checkinlinks':cl.get_attribute('href'),
                    'placedetails':cp.text,
                }
                item.append(complete_data)
            return item

    except:
        print("Checkins Not Found")
        item = []
        return item

    

def Musicfromprofile(driver,complete_data,facebook_url):
    driver.get(facebook_url+'/music')
    # facebook_url = facebook_url.split('&')[0]
    # facebook_url = facebook_url.split('id=')[1]
    # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=music")
    time.sleep(3)
    wait =WebDriverWait(driver,10)
    item =[]
    try:
        try:
            music_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a')))
            artist_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a/span')))
            music_types = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="bp9cbjyn j83agx80 cbu4d94t d2edcug0"]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div[2]/span/div/div')))

            for ml,an,mt in zip(music_links,artist_names,music_types):
                complete_data={
                    "musiclinks":ml.get_attribute('href'),
                    "artistname":an.text,
                    "musictype":mt.text
                }
                item.append(complete_data)
            print(item)
            return item
        except:
            music_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a')))
            artist_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a/span')))

            for ml,an in zip(music_links,artist_names):
                complete_data={
                    "musiclinks":ml.get_attribute('href'),
                    "artistname":an.text
                }
                item.append(complete_data)
            print(item)
            return item

    except:
        print('Music is not found')
        data =[]
        return data

def workandeducation(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+'/about_work_and_education')
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=about_work_and_education")
        time.sleep(3)
        wait =WebDriverWait(driver,10)

        item=[]
        work_education = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="bp9cbjyn j83agx80 cbu4d94t d2edcug0"]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/a/span/span')))
        for i in work_education:
            # print(i.text)
            complete_data={
                "workandeducation":i.text
            }
            item.append(complete_data)
        return item
    except:
        print("Work Education Not Found")
        data = []
        return data

def placesfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+'/about_places')
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=about_places")
        time.sleep(3)
        wait =WebDriverWait(driver,10)
        item = []
        # place_lived_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="bp9cbjyn j83agx80 cbu4d94t d2edcug0"]/div/div/div/div/div/div/div/div/div/div[4]/a/span'))).click()
        place_lived = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="bp9cbjyn j83agx80 cbu4d94t d2edcug0"]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div/a/span/span')))
        for i in place_lived:
            complete_data={
                "placeslived":i.text
                }
            item.append(complete_data)
        print(item)
        return complete_data
    except:
        print("Place Not Found")
        data = []
        return data

def contactinfofromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+'/about_contact_and_basic_info')
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=about_contact_and_basic_info")
        item =[]
        time.sleep(3)
        wait =WebDriverWait(driver,10)
        try:
            number = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="bp9cbjyn j83agx80 cbu4d94t d2edcug0"]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[1]/span'))).text
            website = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_Gf"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/ul/li/div/div/div[1]/span/a'))).get_attribute('href')
            gender = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div[2]/div/div/div[2]/div/div/div/div/div[1]/span'))).text
            complete_data=[
            {"basicinfo":number},
            {"basicinfo":website},
            {"basicinfo":gender}
            ]
            return complete_data
        except:
            website = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mount_0_0_Gf"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/ul/li/div/div/div[1]/span/a'))).get_attribute('href')
            gender = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div[2]/div/div/div[2]/div/div/div/div/div[1]/span'))).text
            complete_data=[
            {"basicinfo":website},
            {"basicinfo":gender}
            ]
            
            return complete_data
        finally:
            gender = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/div[2]/div/div/div[2]/div/div/div/div/div[1]/span'))).text
        
            complete_data=[
                {"basicinfo":gender}
            ]
            
            return complete_data
    except:
        print("contact info Not Found")
        data = []
        return data

def sportsfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/sports")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=sports")
        item = []
        time.sleep(3)
        wait =WebDriverWait(driver,10)
        athlete_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_Zi"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div/div/a/div/div/div[2]/div/div[1]/span')))
        athlete_img = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_Zi"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div/div/a/div/div/div[1]/div/div/img')))
        for an,ai in zip(athlete_names,athlete_img):
            complete_data={
                "sportsperson":an.text ,
                "sportpersonimage":ai.get_attribute('src'),
            }
            item.append(complete_data)
        print(item)
        return item
    except:
        athlete_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div/div/a/div/div/div[2]/div/div[1]/span')))
        athlete_img = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div/div/a/div/div/div[1]/div/div/img')))
        for an,ai in zip(athlete_names,athlete_img):
            complete_data={
                "sportsteam":an.text ,
                "sportsteamimage":ai.get_attribute('src'),
            }
            item.append(complete_data)
        print(item)
        return item
    finally:
        print("sports Not Found")
        data = []
        return data

def moviebiofromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/movies")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=movies")
        item = []
        wait = WebDriverWait(driver, 3)
        movie_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a')))
        movie_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a/span')))
        # program_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_8u"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[2]/span/div/div')))

        for ml,mn in zip(movie_links,movie_names):
            programe_link = ml.get_attribute('href')
            # programe = pr.text 
            program_name = mn.text
            complete_data={
                "movielink":programe_link,
                # "programme":programe,
                "moviename":program_name
            }
            item.append(complete_data)
        return item
    except:
        print("Movies Not Found")
        data = []
        return data

def tvprogrammebiofromprofile(driver,complete_data,facebook_url):
    try:
        try:
            driver.get(facebook_url+"/tv")
            # facebook_url = facebook_url.split('&')[0]
            # facebook_url = facebook_url.split('id=')[1]
            # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=tv")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            item = []
            wait =WebDriverWait(driver,10)
            channel_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a')))
            programs = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a/span')))
            

            for cl,pn in zip(channel_links,programs):
                programe_link = cl.get_attribute('href')
                programe = pn.text 
                # program_name = pn.text
                complete_data={
                    "programlinks":programe_link,
                    "programme":programe,
                }
                item.append(complete_data)
            print(item)
            return item
        except:
            driver.get(facebook_url+"/video_tv_shows_favorite")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            item = []
            wait =WebDriverWait(driver,10)
            channel_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a')))
            programs = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a/span')))
            program_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_8u"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[2]/span/div/div')))
            for cl,pr,pn in zip(channel_links,programs,program_names):
                programe_link = cl.get_attribute('href')
                programe = pr.text 
                program_name = pn.text
                complete_data={
                    "programlinks":programe_link,
                    "programme":program_name,
                    "programmetype":program_name
                }
                item.append(complete_data)
            print(item)
            return item
    except: 
        print("TV programs Not Found")
        data = []
        return data
def friendsbiofromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/about_family_and_relationships")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=about_family_and_relationships")
        item = []
        time.sleep(3)
        wait = WebDriverWait(driver, 3)
        try:
            person_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[*]/div[2]/div/div/div[2]/div[1]/a/span/span')))
            relationships = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[*]/div[2]/div/div/div[2]/div[2]/div/span/span')))
            relationship_status = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[*]/div/div/div[2]/div')))

            for pn,r,rs in zip(person_names,relationships,relationship_status):
                if 'married' in rs.text:
                    complete_data={
                        "name":pn.text ,
                        "relation":r.text, 
                        "relationshipstatus":rs.text
                    }
                    item.append(complete_data)
                elif 'unmarried' in rs.text:
                    complete_data={
                        "name":pn.text ,
                        "relation":r.text, 
                        "relationshipstatus":rs.text
                    }
                    item.append(complete_data)

                else:
                    complete_data={
                        "name":pn.text ,
                        "relation":r.text, 
                        # "relationshipstatus":rs.text
                    }
                    item.append(complete_data)
                    
            print(item)
            return item
        except:
            person_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[*]/div[2]/div/div/div[2]/div[1]/a/span/span')))
            relationships = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[*]/div[2]/div/div/div[2]/div[2]/div/span/span')))
            # relationship_status = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/div[*]/div/div/div[2]/div')))

            for pn,r in zip(person_names,relationships):
                complete_data={
                    "name":pn.text ,
                    "relation":r.text,
                    # "relationshipstatus":rs
                }
                item.append(complete_data)
            print(item)
            return item
    except:
        print("friends and relationship Not Found")
        data = []
        return data

def booksbiofromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/books")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=books")
        item = []
        wait = WebDriverWait(driver, 3)
        book_urls = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a')))
        book_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div/a/span')))
        # program_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mount_0_0_8u"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div[2]/div[2]/span/div/div')))

        for bu,bn in zip(book_urls,book_names):
            programe_link = bu.get_attribute('href')
            programe = bn.text 
            # program_name = pn.text
            complete_data={
                "booklink":programe_link,
                "bookname":programe,
                # "programmetype":program_name
            }
            item.append(complete_data)
        return item
    except:
        print("Books Not Found")
        data = []
        return data
def gamesbiofromprofile(driver,complete_data,facebook_url):
   
    try:
        driver.get(facebook_url+"/games")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=games")
        item = []
        wait = WebDriverWait(driver, 3)
        game_urls = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div/div/a')))
        game_names = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[*]/div/div/a/div/div/div[2]/div/div[1]/span')))

        for gu,gn in zip(game_urls,game_names):
            programe_link = gu.get_attribute('href')
            programe = gn.text 
            complete_data={
                "appgamelink":programe_link,
                "appgamename":programe,
            }
            item.append(complete_data)
        return item
    except:
        print("Games Not Found")
        data = []
        return data
def aboutbiofromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/about_overview")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=about_overview")
        item = []
        wait = WebDriverWait(driver, 3)
        
        programs = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/a[2]/span/span')))

        for pr in programs:
            programe = pr.text

            complete_data={
                "programme":programe
            }
            item.append(complete_data)
        return item
    
    except:
        print("Nothing found in About")
        data = []
        return data

def liveeventsfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+"/about_life_events")
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=about_life_events")
        item = []
        wait = WebDriverWait(driver, 3)
        try:
            life_events = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[*]/div[2]/div/div[2]/a/div/div/span')))
            years = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="aahdfvyu sej5wr8e"]//span')))
            for le,year in zip(life_events,years):
                event = le.text 
                complete_data={
                    "years":year.text,
                    "eventsdetails":event,
                }
                item.append(complete_data)
            return item
        except:
            life_events = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[*]/div[2]/div/div[2]/a/div/div/span')))
            years = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="aahdfvyu sej5wr8e"]//span')))
            for le in life_events:
                event = le.text 
                complete_data={
                    "eventsdetails":event,
                }
                item.append(complete_data)
            return item            
    except:
        print("Events Not Found")
        data = []
        return data

def followersfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+'/followers')
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=followers")
        time.sleep(3)
        for i in range(0,50):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        wait =WebDriverWait(driver,10)
        item =[]
        follower = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_6s5d _71pn _-kb segoe"]/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')))
        
        for i in follower:
            complete_data={"followers":i.text}
            item.append(complete_data)
        print(item)
        return item

    except:
        print("Followers Not Found")
        data =[]
        return data

def followingsfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+'/following')
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=following")
        wait =WebDriverWait(driver,10)
        item =[]

        time.sleep(3)
        for i in range(0,50):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        following = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_6s5d _71pn _-kb segoe"]/div/div/div/div/div[3]/div/div/div[1]/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')))
        
        for i in following:
            complete_data={"followings":i.text}
            item.append(complete_data)
        return item

    except:
        print("Followings Not Found")
        data =[]
        return data


def photolinksfromprofile(driver,complete_data,facebook_url):
    try:
        driver.get(facebook_url+'/photos')
        # facebook_url = facebook_url.split('&')[0]
        # facebook_url = facebook_url.split('id=')[1]
        # driver.get("https://www.facebook.com/profile.php?id="+facebook_url+"&sk=photos")
        time.sleep(3)
        for i in range(0,50):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        wait =WebDriverWait(driver,10)
        item=[]
        # elements = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'Photos'))).click()
        photos_links = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="j83agx80 btwxx1t3 lhclo0ds"]/div/div/div/a')))
        for i in photos_links:
            # i= i
            # print(i.get_attribute('href'))
            complete_data={"photoslinks":i.get_attribute('href')}
            item.append(complete_data)
        print(item)
        return item
    except:
        print("Photos Link Not Found")
        data = []
        return data


def likesfromprofiles(driver,facebook_url):
    facebook_url = facebook_url.replace('www','m')
    driver.get(facebook_url)
    time.sleep(3)
    # item =[]
    # count =1
    likes_list = []
    shares_list = []
    wait = WebDriverWait(driver,3)
    try:
        try:
            for i in range(0,50):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            likes = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_22rc"]/div/div/a/div/div/div')))
            shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/div[3]/section/article[*]/footer/div/div[1]/a/div/div[2]/span[2]')))

            for like,share in zip(likes,shares):
                likes_list.append(like.text+' like')
                if "share" in share.text:
                    shares_list.append(share.text)
                
                else:
                    continue
            
            # print(likes_list,shares_list)
            return likes_list,shares_list 
        except:
            for i in range(0,50):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            likes = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/div[3]/section/article[*]/footer/div/div[1]/a/div/div[1]/div')))
            shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/div[3]/section/article[*]/footer/div/div[1]/a/div/div[2]/span')))
            
            for like,share in zip(likes,shares):
                likes_list.append(like.text+' like')
                if "share" in share.text:
                    shares_list.append(share.text)
                
                else:
                    continue
            # print(likes_list,shares_list)
            return likes_list,shares_list
    except:
        data1 = []
        data2 = []
        return data1,data2
def commentsfromprofile(driver,facebook_url):
    # facebook_url = facebook_url.replace('www','m')
    # driver.get(facebook_url)
    # time.sleep(3)
    # time.sleep(3)
    item =[]
    count =1
    
    wait = WebDriverWait(driver,3)

    try:
        # for i in range(0,50):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(3)

        comments = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/div[3]/section/article[*]/footer/div/div[1]/a/div/div[2]/span[1]')))

        for comment in comments:
            if "comment" in  comment.text:
                item.append(comment.text)
            else:
                continue
        # print(item)
        return item
    except:
        data=[]
        return data
def descriptionfromtimeline(driver,complete_data,facebook_url):
    # facebook_url = facebook_url.replace('www','m')
    # driver.get(facebook_url)
    item =[]
    wait = WebDriverWait(driver,3)
    try:
        # for i in range(0,50):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(3)
        descriptions = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_5rgt _5nk5 _5msi"]//p')))
        if len(descriptions) > 1:
            for description in descriptions:        
                item.append(description.text)
        else:
            item.append(descriptions.text)
        return item
    except:
        data = []
        return data
            
def timelinefromprofile(driver,facebook_url):
    # try:
    facebook_url = facebook_url.replace('www','m')
    driver.get(facebook_url)
    item =[]
    wait = WebDriverWait(driver,3)
    # for post in get_posts(post_urls=[facebook_url]):
    #     comments = post['comments']
    #     likes = post['likes']
    #     post_text = post['post_text']
    #     shares = post['shares']
    #     username = post['username']
    #     time = post['time']
        
    #     data = {
    #     'title': username,
    #     'date':time,
    #     'desciption': post_text,
    #     'likes': likes,
    #     'commentsandshares': comments+shares
        
    #     }
    #     item.append(data)
    # return item

    for i in range(0,50):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    try:
        try:
            for i in driver.find_element_by_xpath('//*[@class="story_body_container"]'):
                # titles = wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[3]/div[3]/section/article[*]/div/header/div[2]/div/div/div[1]/h3/strong[1]/a')))
                titles = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_4g34"]/h3//strong[1]/a')))
                dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="story_body_container"]/header/div[2]/div/div/div/div/a/abbr')))
                likes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'_1g06')))
                shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_1fnt"]/span[2]')))
                comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'comments-token')))
                descriptions = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_5rgt _5nk5 _5msi"]//p')))
                
                for title,date,like,description,comment,share in zip(titles,dates,likes,descriptions,comments,shares):
                    complete_data = {
                        "title":title.text,
                        "date":date.text,
                        "description":description,
                        "likes":like,
                        "commentsandshares":comment.text+share.text
                        }
                    item.append(complete_data)
                    # print(item)
            return item
        except:
            try:
                titles = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_4g34"]/h3//strong[1]/a')))
                dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="story_body_container"]/header/div[2]/div/div/div/div/a/abbr')))
                likes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'_1g06')))
                # shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_1fnt"]/span[2]')))
                comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'comments-token')))
                descriptions = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_5rgt _5nk5 _5msi"]//p')))
                for title,date,like,description,comment in zip(titles,dates,likes,descriptions,comments):
                    complete_data = {
                        "title":title.text,
                        "date":date.text,
                        "description":description.text,
                        "likes":like.text,
                        "commentsandshares":comment.text
                        }
                    item.append(complete_data)
                return item
            except:
                titles = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_4g34"]/h3//strong[1]/a')))
                dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="story_body_container"]/header/div[2]/div/div/div/div/a/abbr')))
                likes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'_1g06')))
                # shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_1fnt"]/span[2]')))
                # comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'comments-token')))
                descriptions = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_5rgt _5nk5 _5msi"]//p')))
                for title,date,like,description in zip(titles,dates,likes,descriptions):
                    complete_data = {
                        "title":title.text,
                        "date":date.text,
                        "description":description.text,
                        "likes":like.text,
                        }
                    item.append(complete_data)
                return item
                
        
            
        finally:
            try:
                titles = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_4g34"]/h3//strong[1]/a')))
                dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="story_body_container"]/header/div[2]/div/div/div/div/a/abbr')))
                likes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'_1g06')))
                # shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_1fnt"]/span[2]')))
                # comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'comments-token')))
                # descriptions = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_5rgt _5nk5 _5msi"]//p')))
                for title,date,like in zip(titles,dates,likes):
                    complete_data = {
                        "title":title.text,
                        "date":date.text,
                        "likes":like.text,
                        }
                    item.append(complete_data)
                return item
            
            except:
               
                titles = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="_4g34"]/h3//strong[1]/a')))
                dates = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="story_body_container"]/header/div[2]/div/div/div/div/a/abbr')))
                # likes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'_1g06')))
                # shares = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_1fnt"]/span[2]')))
                # comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'comments-token')))
                # descriptions = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="_5rgt _5nk5 _5msi"]//p')))
                for title,date in zip(titles,dates):
                    complete_data = {
                        "title":title.text,
                        "date":date.text,
                        # "description":description,
                        # "likes":like,
                        # "commentsandshares":comment
                        }
                    item.append(complete_data)
                return item
    except:
        print("timelines data not Found")
        data = []
        return data


def data_extraction_for_profile(driver,facebook_url,complete_data,filename,count):
    
    # path = os.getcwd()+"/_Hologic_KOLs_Facebook_Profiles/"
    # folder = "/_Hologic_KOLs_Facebook_Profiles/"
    # mkdir = os.mkdir(folder)
    # path = os.getcwd()+"/_Hologic_KOLs_Facebook_Profiles/"
    
    timeline = timelinefromprofile(driver,facebook_url)
    print(timeline)

    videos =videosfromprofile(driver,complete_data,facebook_url)
    
    checkins =checkinsfromprofile(driver,complete_data,facebook_url)

    sports = sportsfromprofile(driver,complete_data,facebook_url)

    music = Musicfromprofile(driver,complete_data,facebook_url)

    movies =moviebiofromprofile(driver,complete_data,facebook_url)

    tvprogramme = tvprogrammebiofromprofile(driver,complete_data,facebook_url)

    books =booksbiofromprofile(driver,complete_data,facebook_url)

    games =gamesbiofromprofile(driver,complete_data,facebook_url)

    work_education = workandeducation(driver,complete_data,facebook_url)

    places =placesfromprofile(driver,complete_data,facebook_url)

    friendsandrelationships = friendsbiofromprofile(driver,complete_data,facebook_url)

    contactinfo = contactinfofromprofile(driver,complete_data,facebook_url)

    aboutbio = aboutbiofromprofile(driver,complete_data,facebook_url)
    
    liveevents = liveeventsfromprofile(driver,complete_data,facebook_url)

    followers = followersfromprofile(driver,complete_data,facebook_url)

    following = followingsfromprofile(driver,complete_data,facebook_url)

    photos = photolinksfromprofile(driver,complete_data,facebook_url)

    
    

    data={
        "videos":videos,
        "checkin":checkins,
        "sports":sports,
        "music":music,
        "movies":movies,
        "tvprogramme":tvprogramme,
        "books":books,
        "games":games,
        "workandeducation":work_education,
        "places":places,
        "friendsandrelationships":friendsandrelationships,
        "contactinfo":contactinfo,
        "aboutbio":aboutbio,
        "liveevents":liveevents,
        "followers":followers,
        "following":following,
        "photos":photos,
        "timeline":timeline
    }

    if count == 0:
        with open(filename+'.json', 'w+') as df:
            df.write(json.dumps(data,indent=2))
    else:          
        with open(filename+'.json', 'w+') as df:
            df.write(json.dumps(data,indent=2))
    # # 
      
def main_funct():
    
    driver_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/chromedriver.exe"
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    # option.add_argument("--incognito") #OPTIONAL
    # option.add_argument("--headless") # OPTIONAL
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    

    complete_data ={}
    df = pd.read_csv("facebook_profiles_url.csv")
    facebook_urls = df["Facebook Url"]
    # timeline = timelinefromprofile(filename)
    facebook_page(driver)
    count = 0
    for facebook_url in facebook_urls:
        # filename = facebook_url.split('profile.php?id=')[1]   
        # filename = filename.replace('/','')
        filename = facebook_url.split('www.facebook.com/')[1]
        print(filename)
        # userhandle = facebook_url.split('.com/')[1]
        driver.get(facebook_url)
        
        # try:

        # wait = WebDriverWait(driver, 5)
        data_extraction_for_profile(driver,facebook_url,complete_data,filename,count)
        count+=1
        # except:
        #     continue
        
if __name__ == '__main__':
    main_funct()
    # now = datetime.now().time()
    # t = time.localtime()
    # current_time = time.strftime("%H", t)
    # current_day_hours = 24  - int(current_time) 
    # schedule_day_hours = int(current_time) + current_day_hours 

    # today = datetime.date.today().strftime('%d')
    # schedule_date = 30 - int(today) 
    # one_day = schedule_day_hours * schedule_date
    # # print(schedule_date)
    # scheduler = BackgroundScheduler()
    # if current_time == '24':

    #     scheduler.add_job(main_funct, 'interval',hours = one_day,minutes = 900)
    #     scheduler.start()
    #     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        
    #     try:
    #         # This is here to simulate application activity (which keeps the main thread alive).
    #         while True:
    #             time.sleep(2)
    #     except (KeyboardInterrupt, SystemExit):
    #         # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #         scheduler.shutdown()
    # else:
    #     pass