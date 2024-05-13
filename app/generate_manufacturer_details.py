import requests
import csv
import time
from gemini import query_gemini


class ManufacturerInfoService:
    def __init__(self):
        self.base_url = "https://bikeindex.org/api/v3/manufacturers"

    def get_all_manufacturers(self):
        manufacturers_list = []
        page = 1
        while True:
            params = {"page": page, "per_page": 100}
            response = requests.get(self.base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                manufacturers = data.get("manufacturers", [])
                if not manufacturers:
                    break

                for manufacturer in manufacturers:
                    name = manufacturer.get("name")
                    manufacturers_list.append(name)

                page += 1
            else:
                print("Failed to fetch data from API")
                break

        return manufacturers_list

    def append_to_csv(self, manufacturer, details, filename='all_company_details.csv'):
        with open(filename, 'a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow([manufacturer, details])

    #calling manufacturer api to get list of all manufacturers
    def fetch_and_append_details(self, manufacturers_list):
        ctr = 0
        map = {}
        for item in manufacturers_list[250:500]:
            ctr += 1
            if ctr == 200:
                time.sleep(10)
            if item not in map:
                details = query_gemini(item)
                map[item] = details
                self.append_to_csv(item, details)


##generating the manufacturer details
manufacturer_info = ManufacturerInfoService()
manufacturers_list = manufacturer_info.get_all_manufacturers()
manufacturer_info.fetch_and_append_details(manufacturers_list)
