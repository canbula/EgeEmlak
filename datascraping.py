import os
import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class DataScraping:
    def __init__(self, link, csv_file, update_interval, headless=True):
        self.link = link
        self.csv_file = csv_file
        self.update_interval = update_interval
        self.headless = headless
        self.service = Service(ChromeDriverManager().install())
        self.options = Options()
        if self.headless:
            self.options.add_argument("--headless")
        self.options.add_argument(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        # self.driver.get(self.link)
        # self.driver.implicitly_wait(10)
        self.data = []

    def get_data(self):
        data = []
        next_page = True
        while next_page:
            self.driver.get(self.link)
            self.driver.implicitly_wait(20)
            time.sleep(20 + random.random())
            try:
                houses = self.driver.find_elements(
                    by=By.CSS_SELECTOR, value=".searchResultsItem"
                )
            except Exception as e:
                print(e)
                houses = []
            for house in houses:
                if house.get_attribute("data-id") is None:
                    continue
                info = house.find_elements(
                    by=By.CSS_SELECTOR, value=".searchResultsAttributeValue"
                )
                price = house.find_elements(
                    by=By.CSS_SELECTOR, value=".searchResultsPriceValue"
                )
                location = house.find_elements(
                    by=By.CSS_SELECTOR, value=".searchResultsLocationValue"
                )
                try:
                    data.append(
                        {
                            "id": house.get_attribute("data-id"),
                            "m2": int(info[0].text),
                            "rooms": int(info[1].text.split("+")[0]),
                            "living_rooms": int(info[1].text.split("+")[1]),
                            "price": int(
                                price[0].text.replace(".", "").replace("TL", "")
                            ),
                            "location": location[0].text.replace("\n", " "),
                        }
                    )
                except Exception as e:
                    print(e)
                    continue
            time.sleep(2 + random.random())
            next_page_link = self.browser.find_elements(
                by=By.CSS_SELECTOR, value=".prevNextBut"
            )
            next_page = False if len(next_page_link) == 0 else True
            for n in next_page_link:
                if n.get_attribute("title") == "Sonraki":
                    link = n.get_attribute("href")
                    next_page = True
                else:
                    next_page = False
        # self.driver.close()
        self.driver.quit()
        return data

    def save_data(self):
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def load_data(self):
        with open(self.csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # row["id"] = row["id"]
                    row["m2"] = int(row["m2"])
                    row["rooms"] = int(row["rooms"])
                    row["living_rooms"] = int(row["living_rooms"])
                    row["price"] = int(row["price"])
                    # row["location"] = row["location"]
                    self.data.append(row)
                except Exception as e:
                    print(e)
                    continue

    def delete_data(self):
        try:
            os.remove(self.csv_file)
        except Exception as e:
            print(e)
            pass

    def run(self):
        if not os.path.exists(self.csv_file) or (
            time.time() - os.path.getmtime(self.csv_file) > self.update_interval
        ):
            self.data = self.get_data()
            self.save_data()
        else:
            self.load_data()
        return self.data


if __name__ == "__main__":
    link = "https://www.sahibinden.com/kiralik/izmir?pagingSize=50"
    csv_file = f"{os.getcwd()}/izmir.csv"
    update_interval = 3600
    headless = False
    data_scraping = DataScraping(link, csv_file, update_interval, headless)
    data = data_scraping.run()
    print(data)
