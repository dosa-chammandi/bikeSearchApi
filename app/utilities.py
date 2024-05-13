import logging
import os,sys
conf_path = os.getcwd()
sys.path.append(conf_path)
import json,csv
import requests
import base64
from datetime import datetime, timedelta
from time import strftime, localtime
from gemini import query_gemini
from app_constants import appConstants

class Utils():

    def csv_to_json(csv_file_path):
        # Open CSV file and initialize empty list to store rows
        with open(csv_file_path, 'r', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            #next(csv_reader)  # Skip the header row
            data = {}
            for row in csv_reader:
                data[row[0]] = row[1]

        # Convert list of dictionaries to JSON format
        #json_data = json.dumps(data)

        return data


    def get_past_dates(interval_type, interval_count):

        interval_count = int(interval_count)
        today = datetime.now().date()
        past_dates = []

        if interval_type == "month":
            interval = interval_count * 30
        elif interval_type == "week":
            interval = interval_count * 7
        elif interval_type == "days":
            interval = interval_count
        else:
            raise ValueError("Invalid interval type. Please choose 'month', 'week', or 'days'.")

        for i in range(0, interval + 1):
            past_dates.append(today - timedelta(days=i))

        past_dates.reverse()
        return past_dates


    
    def epoch_to_date(epoch_date):
        try:
            date = strftime('%Y-%m-%d %H:%M:%S', localtime(epoch_date)).split(" ")[0]
            return date
        except Exception as e:
            logging.error(f"Error in epoch_to_date: {str(e)}")
            return ""

    
    def convert_to_base64(image_content):
        try:
            base64_encoded_image = str(base64.b64encode(image_content).decode('utf-8'))
            #print(base64_encoded_image)
            return base64_encoded_image
        except Exception as e:
            logging.error(f"Error in convert_to_base64: {str(e)}")
            return ""

    
    def process_data(data,bflag):
        try:
            
            for item in data.get('bikes', []):
                ##checking if date_stolen is available, if available actual date is calculated from the epoch time else considering this item doesnt fall under the given timeframe.
                if item.get("date_stolen")!=None:
                    item['actual_date'] = Utils.epoch_to_date(item.get("date_stolen"))
                else:
                    continue

                

            return data
        except Exception as e:
            logging.error(f"Error in process_data: {str(e)}")
            return {}

    
    def filter_data(data, dates):
        try:
            return [bike for bike in data if bike.get('actual_date', '') in dates]
        except Exception as e:
            logging.error(f"Error in filter_data: {str(e)}")
            return []

    
    def process_time_frame(time_frame):
        try:
            if str(time_frame)!= "0" or str(time_frame)!= "":
                value, interval_type = time_frame.split(" ")
                past_dates = Utils.get_past_dates(interval_type, value)
                past_formatted_dates = [date.strftime("%Y-%m-%d") for date in past_dates]
            else:
                return []
        except Exception as e:
            raise ValueError("time_frame parameter is incorrect: Expected formats are 10 days, 1 month, 4 weeks")
        return past_formatted_dates


    def append_to_csv(manufacturer, details, filename='all_company_details.csv'):
        with open(filename, 'a', newline='',encoding="utf-8") as f:
            writer = csv.writer(f,delimiter='|')
            writer.writerow([manufacturer, details])
    def add_img_encoding(data,bflag):
        if bflag:
            for item in data:
                if str(item.get('large_img', '')).startswith("https://"):
                    try:
                        response = requests.get(item['large_img'], stream=True)
                        response.raise_for_status()
                        image_content = response.content
                        base64_encoded_image = Utils.convert_to_base64(image_content)
                        item['base64_encoded_image'] = base64_encoded_image
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Error fetching image: {str(e)}")
                else:
                    pass
            return data
            
        return data

    def add_manufacturer_info(new_data):
        csv_filepath = appConstants.csv_path
        csv_exists = os.path.isfile(csv_filepath)
        if csv_exists:
            company_data = Utils.csv_to_json(csv_filepath)
        else:
            company_data = {}
        for item in new_data:
            if item.get("manufacturer_name")!=None:
                if company_data.get(item.get("manufacturer_name"))!=None:
                    details = company_data[item.get("manufacturer_name")]
                    item["manufacturer_details"] = details

                else:
                    details = query_gemini(item.get("manufacturer_name"))
                    if details!='':
                        Utils.append_to_csv(item.get("manufacturer_name"), details,
                                                              filename='all_company_details.csv')
                        item["manufacturer_details"] = details

            else:
                pass

        return new_data