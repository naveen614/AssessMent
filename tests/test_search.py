# coding=utf-8
import time

import pytest
from pages.NSEPage import NsePage
from tests.base_test import BaseTest


class TestSearch(BaseTest):

    @pytest.fixture
    def load_pages(self):
        self.page = NsePage(self.driver, self.wait)
        self.page.go_to_nsePage()


    '''
    Execute this before deployement.
    Data will stare in beforeDeployment.xlsx and saves in test folder
    '''
    # def test_beforeDeployement(self, load_pages):
    #     time.sleep(4)
    #     self.page.tableDataBeforeDeployment(deployment=False)

    '''
    Execute this after deployment.
    This will create afterDeployment.xlsx and store in testFolder
    Comparision will happen each data cell and prints the list on of differences on console
    '''
    def test_afterDeployement(self, load_pages):
        time.sleep(4)
        self.page.tableDataBeforeDeployment(deployment=True)
        self.page.comparisionOfData()



