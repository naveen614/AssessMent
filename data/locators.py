from selenium.webdriver.common.by import By


class NSEPageLocators:
    TABLE_HEAD = (By.ID, "optionChainTable-indices")
    TABLE_BODY = (By.TAG_NAME,"tbody")
    TABLE_ROWS = (By.TAG_NAME,"tr")
