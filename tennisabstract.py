import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json


class TennisAbstract:

    def __init__(self, url, filename):
        self.__chrome_driver = webdriver.Chrome("C:\\Users\\pcost\\chromedriver_win32\\chromedriver.exe")
        self.__delay = 3
        self.__url = url
        self.__filename = filename
        self.__data = {}

        self.YEAR_INDEX = 0
        self.ELO_INDEX = 4
        self.HELO_INDEX = 6
        self.CELO_INDEX = 8
        self.GELO_INDEX = 10

    def close(self):
        self.__chrome_driver.close()

    def save(self):
        with open(self.__filename, "w") as f:
            # indent - pretty json
            json.dump(self.__data, f, indent=4)

    def scrap_ratings(self):
        # players_dict = {}
        self.__chrome_driver.get(self.__url)

        try:
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.ID, 'reportable')))
        except TimeoutException:
            print("Loading page took too much time!")

        soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, 'html.parser')

        players_table = soup.find(id="reportable").find("tbody")
        players_table_size = len(players_table.find_all("tr"))

        count = 0

        for tr in players_table.find_all("tr"):
            count += 1
            player_a = tr.find("a", href=True)
            player_url = player_a["href"]
            player_name = str(player_a.text).replace("\u00a0", " ")
            percentage = (count / players_table_size) * 100
            print("[{:.2f}%] {}".format(percentage, player_name))
            years_stats = self.scrap_player_year_end_rankings(player_url)
            self.__data[player_name] = years_stats

    def scrap_player_year_end_rankings(self, url):
        years_dict = {}
        self.__chrome_driver.get(url)

        try:
            myElem = WebDriverWait(self.__chrome_driver, self.__delay).until(EC.presence_of_element_located((By.ID, 'year-end-rankings')))
        except TimeoutException:
            print("Loading page took too much time!")

        soup = bs4.BeautifulSoup(self.__chrome_driver.page_source, 'html.parser')

        # table do not exists
        if soup.find(id="year-end-rankings") is None:
            return {}

        year_end_rankings_table = soup.find(id="year-end-rankings").find("tbody")

        current_year_row = True

        for tr in year_end_rankings_table.find_all("tr"):

            # tr cannot be the current year
            if current_year_row:
                current_year_row = False
                continue

            year, stats = self.__scrap_player_year_end_ranking_tr(tr)
            years_dict[year] = stats

        return years_dict

    def __scrap_player_year_end_ranking_tr(self, tr):
        stats = {}

        td_list = tr.find_all("td")

        year = int(td_list[self.YEAR_INDEX].text)

        stats["Elo"] = int(td_list[self.ELO_INDEX].text) if td_list[self.ELO_INDEX].text != "" else 0
        stats["hElo"] = int(td_list[self.HELO_INDEX].text) if td_list[self.HELO_INDEX].text != "" else 0
        stats["cElo"] = int(td_list[self.CELO_INDEX].text) if td_list[self.CELO_INDEX].text != "" else 0
        stats["gElo"] = int(td_list[self.GELO_INDEX].text) if td_list[self.GELO_INDEX].text != "" else 0

        return year, stats
