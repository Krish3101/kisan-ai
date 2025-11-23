To manually test the application, please follow these steps:

1.  **Open two separate terminal windows.**

2.  **Start the Backend Server** in the first terminal:
    *   Navigate to your project's root directory: `cd C:\Users\krish\OneDrive\Documents\Desktop\kisan-ai`
    *   Run the command: `.\start.bat` (This will start both backend and frontend, if the frontend is already started, this will just launch the backend)
    *   Alternatively, to start only the backend: `.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000` (Make sure your terminal's current directory is the project root)

3.  **Start the Frontend Development Server** in the second terminal:
    *   Navigate to the frontend directory: `cd C:\Users\krish\OneDrive\Documents\Desktop\kisan-ai\frontend`
    *   Run the command: `npm run dev`

4.  **Access the Application:** Once both servers are running, open your web browser and go to `http://localhost:3000`.

**Basic Smoke Test Steps:**

*   **Login:** Try to log in with the demo credentials:
    *   **Username:** `demo`
    *   **Password:** `demo123`
*   **Navigate:** After logging in, navigate through the different sections of the dashboard (Weather, Crops, Finances, Prices, Soil, Chat).
*   **Interact:**
    *   Try adding a new crop in the "Crops" section.
    *   Add an expense or income in the "Finances" section.
    *   Check the AI insights in the Dashboard.
    *   Try the chatbot.
*   **Observe:** Look for any errors in the browser console, network requests, or server terminal output.

**Stopping the Servers:**

*   You can close the terminal windows manually, or run the `stop.bat` file in your project's root directory: `.\stop.bat`

Please let me know if you encounter any issues during this manual testing.