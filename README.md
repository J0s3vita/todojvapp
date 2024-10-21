TODO TOOL APP - HOW TO USE

The TODO Tool App is a Python application designed to help you manage your daily tasks. 
You can add, view, and organize your tasks, mark completed ones, and save everything in a CSV format for easy tracking.
The app is simple to use and provides a quick solution to managing your task flow.

How to use the app:

1. Clone the repository:
    Create a folder to hold the project and open your terminal inside the desired folder.
    Then clone the GitHub repository by running:
   
    git clone https://github.com/J0s3vita/todojvapp.git

3. Navigate to the project folder:
Run the following command to enter the project folder you just cloned:
    cd todojvapp

4. Create a virtual environment:
To isolate the project dependencies, create a new virtual environment:
    python3 -m venv myvenv

5. Activate the virtual environment:
Activate the virtual environment with the command appropriate to your operating system:
    - On macOS/Linux:
        source myvenv/bin/activate
    - On Windows:
        myvenv\Scripts\activate

6. Install the dependencies:
Install the necessary dependencies listed in the `requirements.txt` file:
    pip install -r requirements.txt

   The main libraries used in this project are:
   - **pandas**: For handling CSV file creation and manipulation.
   - **datetime**: To manage and format task deadlines.
   - **os**: To manage file and folder interactions in the system.

7. Run the application:
Now you can run the program to manage your tasks:
    python main.py
