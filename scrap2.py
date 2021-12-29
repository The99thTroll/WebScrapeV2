from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

startURL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/albrino/WebScrape/chromedriver")
browser.get(startURL)

planetData = []
newPlanetData = []
headers = ["Name", "Light-Years", "Mass", "Magnitude", "Discovery", "Hyperlink", "Planet Type", "Planet Radius", "Oribital Radius", "Orbital Period", "Eccentricity"]
finalPlanetData = []

time.sleep(10)

def scrape():
    for i in range(0, 430):
        while True:
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            currentPageNum = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            #print("page ", currentPageNum)
            #print("i ", i)
            if currentPageNum - 1 < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentPageNum - 1 > i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul in soup.find_all("ul", attrs={"class", "exoplanet"}):
            liTags = ul.find_all("li")
            tempList = []
            for index, liTag in enumerate(liTags):
                if index == 0:
                    tempList.append(liTag.find_all("a")[0].contents[0])
                else:
                    try:
                        tempList.append(liTag.contents[0])
                    except:
                        tempList.append("")
            hyperlinkLiTag = liTags[0] 
            tempList.append("https://exoplanets.nasa.gov/exoplanet-catalog/" + hyperlinkLiTag.find_all("a", href=True)[0]["href"])
            planetData.append(tempList)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print("Page: " + str(i))
      
def scrapeMoreData(hyperlink):
    data = []      
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        for tr in soup.find_all("tr", attrs={"class", "fact_row"}):
            for td in tr.find_all("td"):
                try:
                    data.append(td.find_all("div", attrs={"class", "value"})[0].contents[0])
                except:
                    data.append("")
        newPlanetData.append(data)
    except:
        time.sleep(1)
        scrapeMoreData(hyperlink)
        
scrape()
for index, data in enumerate(planetData):
    scrapeMoreData(data[5])
    print(str(index + 1) + " page done 2")
for index, data in enumerate(planetData):
    newPlanetDataElement = newPlanetData[index]
    newPlanetDataElement = [elem.replace("\n", "") for elem in newPlanetDataElement]
    newPlanetDataElement = newPlanetDataElement[:7]
    finalPlanetData.append(data + newPlanetDataElement)
with open("scraper3.csv", "w") as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(headers)
        csvWriter.writerows(finalPlanetData)