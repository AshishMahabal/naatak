# naatak  
मराठी नाटकांचा डेटाबेस

## Overview

The **naatak** app is a Streamlit-based interface for managing a database of Marathi plays. It allows users to:

- **Display Plays:** View detailed information for each play, update fields (such as Title, Author, Genre, Property, etc.), and save changes securely using a passphrase stored in Streamlit secrets.
- **Add a New Play:** Use a form with various widgets (text inputs, radio buttons, checkboxes) to add a new play to the database.
- **Export Data:** Download the current CSV data for offline use or further processing.

## Features

- **Interactive Data Display:** Plays are displayed as a table, with the ability to click on a play’s index or select via a dropdown to load its full details.
- **Field-Specific Inputs:**  
  - Property and Number of Acts use horizontally arranged radio buttons.
  - Genre and Availability fields use checkboxes (with special logic, e.g. “NULL” being exclusive).
- **Secure Updates:** Changes can only be saved if the user supplies the correct passphrase from the secrets, ensuring no sensitive info is hardcoded.
- **CSV Persistence:** All changes are written back to a CSV file so that the data persists between sessions.
- **Easy Customization:** The app uses Streamlit’s session_state alongside interactive widgets to manage state across reruns.

## Setup & Installation

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt```
3. **Configure Secrets:**
Create a .streamlit folder at the root of the project and add a secrets.toml file. For example:
   ```toml
   [credentials]
   passphrase = "your_secure_passphrase"
   ```
4. **Run the Application:**
```streamlit run streamlit_app.py```
5. **How to Update the App:**
When making changes or adding new features, follow these guidelines:

***Code Changes:***
- Update the relevant sections for user input, state management, and CSV file persistence.
- When adding or modifying input fields, ensure adjustments are made in both the “Add a New Play” form and the “Display Plays” update section.
- Use Streamlit’s session_state to ensure data persists across interactions.
***Secrets Management:***
- Keep sensitive information, such as the passphrase, out of the code by using the .streamlit/secrets.toml file.
- Update the secrets file as needed and ensure it is excluded from version control (e.g., by using .gitignore).
***Testing and Validation:***
- Thoroughly test the app on your local machine using various inputs.
- Confirm that CSV updates and state management function correctly.
- Validate updates using Streamlit’s error messages and interactive debugging.
***Documentation:***
- Update this README and inline code comments to reflect new changes.
- Communicate changes with the team via pull requests and code reviews.
***Deployment:***
- If deploying on Streamlit Cloud or another platform, ensure that the environment’s secrets are properly configured.
- Verify that the deployment version works correctly and that all new features are functional before pushing updates to production.
