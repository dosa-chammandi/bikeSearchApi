# bikeSearchApi
This API provides functionality to search for bikes based on various parameters such as location, distance, stolenness, time frame, and manufacturer.

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





