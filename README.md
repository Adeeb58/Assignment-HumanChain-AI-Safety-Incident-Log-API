# Assignment-HumanChain-AI-Safety-Incident-Log-API
# AI Safety Incident Log API

A simplified RESTful API service built with Python, Flask, SQLAlchemy, and Marshmallow in a **single file (`app.py`)**. It logs and manages hypothetical AI safety incidents, storing data persistently in a **SQLite database**.

## Features

*   List all incidents (`GET /incidents`)
*   Log a new incident (`POST /incidents`)
*   Retrieve a specific incident (`GET /incidents/{id}`)
*   Delete an incident (`DELETE /incidents/{id}`)
*   Data persistence using **SQLite** (`incident_basic.db`)  file created locally.
*   JSON request/response handling and validation via Marshmallow.
*   Basic error handling.
*   All core logic contained within `app.py`.

## Technology Stack

*   **Language:** Python 3.x
*   **Framework:** Flask
*   **ORM:** SQLAlchemy (with Flask-SQLAlchemy)
*   **Database:** SQLite (file-based, `incident_basic.db`)
*   **Serialization/Validation:** Marshmallow (with Flask-Marshmallow)

## Setup and Installation

**Prerequisites:**
*   Python 3 installed.
*   `pip` (Python package installer) installed.

##  **Clone the Repository:**
    ```bash
    git clone < https://github.com/Adeeb58/Assignment-HumanChain-AI-Safety-Incident-Log-API >
    cd < Assignment-HumanChain-AI-Safety-Incident-Log-API >
    ```
    
## Installing dependenies
pip install -r requirements.txt

## Global Interpreter has been used

  **Database Setup & Configuration:**
    *   The database configuration is **coded** within `app.py` for simplicity:
        ```python
        # This line defines the database file location
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'incident_basic.db')
        ```
    *   **Automatic Creation:** The SQLite database file (`incident_basic.db`) and the necessary table (`incident_basic.db`) will be **automatically created** in the project directory the first time you run the application (`python app.py`) if they do not already exist.

## Running the Application

1.  Make sure you are in the project directory in your terminal/PowerShell.
2.  Run the application script using Python:
    ```bash
    python app.py
    ```
3.  The API server will start, typically listening on `http://127.0.0.1:5000`.
4.  You will see startup messages, including database table creation checks. A file named `incident_basic.db` will appear in the directory.
5.  Keep this terminal window open. The server runs until you stop it (e.g., `Ctrl+C`). Data will persist in the `incident_basic.db` file between runs.

## API Endpoint Examples

Use a separate terminal window/tab to run these commands while the server (`python app.py`) is running. Choose the command appropriate for your terminal environment.

*   **GET /incidents** - Retrieve all incidents
    *   **curl (Linux/macOS/Git Bash):**
        ```bash
        curl http://127.0.0.1:5000/incidents
        ```
    *   **PowerShell:**
        ```powershell
        Invoke-RestMethod -Uri http://127.0.0.1:5000/incidents
        ```

*   **POST /incidents** - Log a new incident
    *   **curl (Linux/macOS/Git Bash):**
        ```bash
        curl -X POST -H "Content-Type: application/json" \
             -d '{"title": "Example Incident", "description": "Details about the incident.", "severity": "High"}' \
             http://127.0.0.1:5000/incidents
        ```
    *   **PowerShell:**
        ```powershell
        Invoke-RestMethod -Uri http://127.0.0.1:5000/incidents -Method Post -ContentType "application/json" -Body '{"title": "Example Incident", "description": "Details about the incident.", "severity": "High"}'
        ```
    *   *(Response: JSON object of the created incident with its assigned `id` and `reported_at`)*

*   **GET /incidents/{id}** - Retrieve a specific incident (Replace `{id}` with an actual ID like `1`)
    *   **curl (Linux/macOS/Git Bash):**
        ```bash
        curl http://127.0.0.1:5000/incidents/1
        ```
    *   **PowerShell:**
        ```powershell
        Invoke-RestMethod -Uri http://127.0.0.1:5000/incidents/1
        ```
    *   *(Response: JSON object of the specified incident, or 404 if not found)*

*   **DELETE /incidents/{id}** - Delete a specific incident (Replace `{id}` with an actual ID like `1`)
    *   **curl (Linux/macOS/Git Bash):**
        ```bash
        curl -X DELETE http://127.0.0.1:5000/incidents/1
        ```
    *   **PowerShell:**
        ```powershell
        Invoke-RestMethod -Uri http://127.0.0.1:5000/incidents/1 -Method Delete
        ```
    *   *(Response: No content on success (204), or 404 if not found. Verify deletion by trying to GET the same ID again.)*

## I have used poweshell to run commands , I used invoke-restmethod -Uri comamnd to execute 

## Design Decisions & Challenges

*   **Structure:** A single `app.py` file was used to contain all application logic (setup, model, schema, routes) for maximum simplicity, meeting the core functional requirements directly. More complex applications would typically separate these into different files/directories using patterns like Application Factories or Blueprints.


## Regarding any queries please feel free to reach out
 **   email: shaikadeeb58@gmail.com**
