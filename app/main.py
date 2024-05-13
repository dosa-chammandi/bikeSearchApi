import logging as lg
import os,sys
from logging.handlers import RotatingFileHandler
from app_constants import appConstants
import requests
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status,Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel,Field
import uvicorn
from utilities import Utils
from fastapi.responses import JSONResponse

# Log configurations
log_folder = appConstants.log_folder
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_app.log"
log_file_path = os.path.join(log_folder, log_file_name)


logging = lg.getLogger(__name__)
logging.setLevel(lg.INFO)
logging_format = '[%(levelname)s] - %(asctime)s - %(filename)s:%(funcName)s - %(message)s'
logger_formatter = lg.Formatter(logging_format)

file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=3)  # This will rotate log files when they reach 1MB
file_handler.setFormatter(logger_formatter)
logging.addHandler(file_handler)

stream_handler = lg.StreamHandler()
stream_handler.setFormatter(logger_formatter)
logging.addHandler(stream_handler)


class BikeSearchParams(BaseModel):
    """
    Model to represent parameters for bike search.
    """

    location: str = Field(...,title="Location name",example="dublin")
    distance: int = Field(default=10, title="Distance",example=10)
    time_frame: str = Field(default="2 month",title="Time Frame",example="2 month")
    manufacturer: str = Field(default='',title="Manufacturer")
    base_64_img_encoding: str = Field(default="False", title="base 64 encoding", example="False")

class BikeSearchService:
    """
    Service class to perform bike search.
    """
    def __init__(self):
        """
        Initializes BikeSearchService.
        """
        self.url = "https://bikeindex.org:443/api/v3/search"
        logging.info("BikeSearchService initialized")

    def fetch_data(self,params):
        page = 1
        all_bikes = []
        # Loop until all pages are fetched
        while True:
            url = "{}?page={}&per_page=100&manufacturer={}&location={}&distance={}&stolenness=proximity".format(
                self.url, page, params.manufacturer, params.location, params.distance)
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_bikes.extend(data.get('bikes', []))
            if (len(data.get('bikes', [])) < 100):
                break
            page += 1
        return all_bikes


    def add_actual_date_from_epoch(self,data):
        try:

            for item in data:
                ##checking if date_stolen is available, if available actual date is calculated from the epoch time else considering this item doesnt fall under the given timeframe.
                if item.get("date_stolen") != None:
                    item['actual_date'] = Utils.epoch_to_date(item.get("date_stolen"))
                else:
                    continue
            return data
        except Exception as e:
            logging.error(f"Error in process_data: {str(e)}")
            return {}

    def search_bikes(self, params: BikeSearchParams):
        """
        Searches for bikes based on given parameters.

        Parameters:
        - params (BikeSearchParams): Parameters for bike search.

        Returns:
        - List: List of bikes matching the search criteria.
        """
        try:
            #getting data from bikeai using pagination
            data = self.fetch_data(params)
            data = self.add_actual_date_from_epoch(data)
            time_frame = dict(params).get("time_frame")

            #if timeframe is 0 or "" no filter is applied else past days are calculated based on the given interval
            if str(time_frame) != "0" and str(time_frame) != "":
                past_dates = Utils.process_time_frame(time_frame)
                data = Utils.filter_data(data, past_dates)

            #if base_64_img_encoding is set to True, bike images are encoded
            base64_flag = dict(params).get("base_64_img_encoding")
            base64_flag = base64_flag.lower() == 'true'
            data = Utils.add_img_encoding(data,base64_flag)

            #adding manufacturer info
            data = Utils.add_manufacturer_info(data)

            if len(data)==0:
                return "No data present for the given parameters"
            else:
                logging.info("Total %d records from the API using given parameters", len(data))
                return data

        except ValueError as e:
            return JSONResponse(status_code=400, content = {"Bad Request": str(e)})
        except Exception as e:
            logging.error(f"Exception: {str(e)}")
            return JSONResponse(status_code=500, content = {"Internal Server Error"})

app = FastAPI(title="Bonafi- Bike Lost and Found Search", version="0.0.1",
              swagger_ui_parameters={"defaultModelsExpandDepth": -1})

bike_search_service = BikeSearchService()

@app.post("/search_bikes", tags=["Search"], summary="Perform Search.")
async def search_bikes(params: BikeSearchParams):
    """
    Searches for bikes based on given parameters.
    Parameters:
    - params (BikeSearchParams): Parameters for bike search.
    Returns:
    - List: List of bikes matching the search criteria.
    """
    logging.info("Search request received")
    result = bike_search_service.search_bikes(params)
    return result


@app.get("/health", tags=["Health Check"], response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK)
def get_health() -> JSONResponse:
    """
    Check the health of the server.
    Returns:
    - JSONResponse: HTTP Status Code 200 (OK).
    """
    response_data = "OK"
    return JSONResponse(content=response_data)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error_str = [f"{error['msg']}: {error['loc'][-1]}" for error in exc.errors()]
    logging.error(f"Bad Request received: {error_str}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"Bad Request": error_str}
    )


if __name__ == "__main__":
    logging.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
