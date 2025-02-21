# cat_chatbot

## Prerequisites

Ensure you have the following installed on your machine:
- [Node.js](https://nodejs.org/) (version 14.x or higher)
- [npm](https://www.npmjs.com/) (version 6.x or higher)
- [Python](https://www.python.org/) (version 3.8 or higher)
- [pip](https://pip.pypa.io/en/stable/)

## Backend Setup

1. **Navigate to the backend directory:**
    ```sh
    cd backend
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**
    - Copy the example environment file:
        ```sh
        cp example.env .env
        ```
    - Edit the `.env` file to include your specific environment variables.

6. **Run the backend server:**
    ```sh
    python main.py
    ```

## Frontend Setup

1. **Navigate to the frontend directory:**
    ```sh
    cd ../frontend
    ```

2. **Install the required Node.js packages:**
    ```sh
    npm install
    ```

3. **Set up environment variables:**
    - Copy the example environment file:
        ```sh
        cp .env.local.example .env.local
        ```
    - Edit the `.env.local` file to include your specific environment variables.

4. **Run the frontend development server:**
    ```sh
    npm run dev
    ```

## Running the Application

1. **Ensure both the backend and frontend servers are running:**
    - Backend server should be running on the specified port (e.g., `http://localhost:8000`).
    - Frontend server should be running on the specified port (e.g., `http://localhost:3000`).

2. **Open your browser and navigate to the frontend server URL:**
    ```sh
    http://localhost:3000
    ```

You should now see the `cat_chatbot` application running.

## Additional Notes

- To deactivate the Python virtual environment, simply run:
    ```sh
    deactivate
    ```

- For production deployment, ensure to set the appropriate environment variables and use a production-ready server setup.

- Refer to the respective documentation for [Node.js](https://nodejs.org/), [npm](https://www.npmjs.com/), [Python](https://www.python.org/), and [pip](https://pip.pypa.io/en/stable/) for more details on installation and usage.

Feel free to reach out if you encounter any issues or have any questions regarding the setup process.