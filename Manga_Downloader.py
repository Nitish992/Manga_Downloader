from selenium import webdriver
from PIL import Image
import os
import requests
from bs4 import BeautifulSoup

#Link of the manga 
#Only support https://readmanganato.com
URL = 'https://readmanganato.com/manga-to970571'
page = requests.get(URL)

#Soup object
soup = BeautifulSoup(page.content, 'html.parser')

#Getting the container which contains all the chapters
chapters_panel = soup.find("ul", class_="row-content-chapter")

#Title of the manga
manga_title = soup.find("div", class_="story-info-right")
title= manga_title.find("h1").get_text()

#Getting all the chapters links
chapter_link = []
for i in chapters_panel.find_all("a"):
    chapter_link.append(i.get("href"))

#Function to donwload the manga
def downloader(link):
    #Extracting chapter no. from the link
    temp=link.split('-')
    chap = temp[-1]

    #Headless 
    options = webdriver.ChromeOptions()
    options.headless = True

    #Deploying chrome
    driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe",chrome_options=options)
    driver.get(link)

    #Finding the container which contain the chapter
    element = driver.find_element_by_class_name("container-chapter-reader")
    #Location of the element and size which will help to crop the image
    location = element.location
    size = element.size

    #Screenshot of the full page
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height'))
    driver.find_element_by_tag_name('body').screenshot('fullpage.png')

    #Croping the full page screenshot
    x = location['x']
    y = location['y']
    width = location['x']+size['width']
    height = location['y']+size['height']
    im = Image.open('fullpage.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    
    #Filename and saving the file
    temp_filename= chap.replace(".","_")
    filename = "Chapter_"+temp_filename+".png"
    print(filename)
    im.save(path+'\\'+ filename, 'png')

    #removing the full page screenshot
    os.remove('fullpage.png')
    driver.quit()

    print(f'Finished Downloading Chapter: {chap}')

#Function to iterate all the chapters and downloading them
def main():
    for index in chapter_link:
        downloader(index)
    print("Finished Downloading.")

#Getting the current directory
current_path = os.getcwd()
#New directory name as the manga
directory = title
path = os.path.join(current_path, directory)

#Checking if the directory exist if not creating it
if not os.path.exists(path):
    os.mkdir(path)
    main()
else:
    main()
