from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from data.locators import NSEPageLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
import openpyxl
from openpyxl.styles import PatternFill
import numpy as np
from selenium import webdriver
import time


class NsePage(BasePage):


    def __init__(self, driver, wait):
        self.url = "https://www.nseindia.com/option-chain"
        self.locator = NSEPageLocators
        super().__init__(driver, wait)

    def go_to_nsePage(self):
        self.go_to_page(self.url)

    def check_title(self, title):
        self.wait.until(EC.title_contains(title))
        # time.sleep(4)
        # self.driver.refresh()
        # time.sleep(4)
        # table = self.driver.find_element(*self.locator.TABLE_HEAD)
        # tableBody = table.find_element(*self.locator.TABLE_BODY)
        #
        # tableBody.find_elements(*self.locator.TABLE_ROWS)

    def tableRows(self):
        time.sleep(5)
        table=self.driver.find_element(*self.locator.TABLE_HEAD)
        tableBody=table.find_element(*self.locator.TABLE_BODY)

        return tableBody.find_elements(*self.locator.TABLE_ROWS)

    def tableHeadingList(self):
        count = 0;
        heading = []
        content = self.driver.page_source
        soup = BeautifulSoup(content)
        for a in soup.findAll('thead'):
            name = a.find('tr')
            for thead in soup.findAll('th'):
                count = count + 1
                if (count > 4):
                    heading.append(thead.text)


        return heading

    def tableDataBeforeDeployment(self,deployment):
        tablerows=self.tableRows()
        MyList = [[] for row in tablerows]
        for i in range(1, len(tablerows[0].find_elements(By.TAG_NAME, 'td'))):
            for j in range(0, len(tablerows)):
                MyList[j].append(tablerows[j].find_elements(By.TAG_NAME, 'td')[i].text)

        heading=self.tableHeadingList()

        '''
        Adding data to dataframe for processing
        '''
        df = pd.DataFrame([MyList[1]], columns=heading)
        '''
        Adding data to xlsx and future reference
        '''
        kkk = 0
        for k in MyList:
            kkk += 1
            if (kkk == len(MyList)):
                break
            df.loc[len(df.index)] = MyList[kkk]
        if(deployment):
            df.to_excel('afterDeployment.xlsx', sheet_name='new_sheet_name')
        else:
            df.to_excel('beforeDeployment.xlsx', sheet_name='new_sheet_name')
            self.comparisionOfData()


    def comparisionOfData(self):
        listOfAfter = []
        listOfBefore = []
        headings=self.tableHeadingList()
        beforeDeployment = pd.read_excel('beforeDeployment.xlsx')
        afterDeployment = pd.read_excel('afterDeployment.xlsx')

        for index, row in afterDeployment.iterrows():
            listOfAfter.append(row.to_list())

        for index, row in beforeDeployment.iterrows():
            listOfBefore.append(row.to_list())

        arr1 = np.array(listOfAfter[21])
        arr2 = np.array(listOfBefore[21])

        difference = []
        # Using numpy's built-in functions to find the mismatch
        Output = np.where(arr1 != arr2)[0]
        # print(np.array(Output))

        for valuesOf in np.array(Output):
            print("Column Name: " + headings[valuesOf])
            print("beforeValues: " + listOfAfter[21][valuesOf], "after values: " + listOfBefore[21][valuesOf])
