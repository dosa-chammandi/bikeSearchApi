# bikeSearchApi
This API provides functionality to search for bikes based on various parameters such as location, distance, stolenness, time frame, and manufacturer.

# Features
- Location: Search either by location or utilize the user's IP location by giving location as "IP".
- Duration: Narrow down bikes based on the time elapsed since they were reported stolen (default setting is 2 month).
- Manufacturer Name: Identify stolen bikes from a particular manufacturer by inputting the manufacturer's name.
- Distance: Fine-tune results within a designated distance range (default setting is 10 kilometers).

## Installation

1. First step is to clone the repo to your local system using git clone.
2. Navigate to the project directory.
3. **Create and Use a Virtual Environment**:

    Create a virtual environment to isolate the dependencies of the project. Navigate to the project directory and execute the following commands:

    ```
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
4. Install the required dependencies by running
    ```
    pip install -r requirements.txt

    ```

5. Run the FastAPI server by executing the following command:
  ```
    python main.py

  ```

## Docker Deployment
1. Open a terminal window.
2. Navigate to the directory containing the Dockerfile.
3. Run the following command to build the Docker image:
 ```
    docker build -t {image_name} .

  ```
4. Once the Docker image is built, you can run a container based on that image by running,
 ```
    docker run -p 8080:8080 {image_name}

   ```

## Endpoints

- **POST /search_bikes**: Perform a search for bikes based on specified parameters.
- **GET /health**: Check the health of the server.

## Request Parameters

The `/search_bikes` endpoint accepts the following parameters:

- **page** (optional): Page number for pagination (default: 1).
- **per_page** (optional): Number of items per page (default: 100).
- **location** (required): Location to search for bikes.
- **distance** (optional): Distance range for the search (default: 100).
- **stolenness** (optional): Stolenness parameter for search (default: "proximity").
- **time_frame** (optional): Time frame for the search (default: "0").
- **manufacturer** (required): Manufacturer of the bike.
- **base_64_img_encoding** (optional): Flag to indicate whether to encode bike images (default: "False").





