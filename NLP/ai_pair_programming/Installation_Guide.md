# Installation Guide:
1. For Windows Users: Download the Windows executable file (.exe) from the Google Drive Repository:
https://drive.google.com/drive/u/1/folders/1TFnrdLVGB2Tbu-Se2PGxvMB-rmBOuPFa
2.	For Mac/Linux users, you can download the python source code from the associated GitHub repository and build an executable for the GUI locally as described below.
3.	Advanced Users (Windows/Linux/MacOS): Download the two python source files from the GitHub Repository:
    - Link: https://github.com/meeshawn18/ai_pair_programming 
    - Make sure you are running Python version 3.9 and above.
    - (Optional) Create and activate a Virtual Python Environment using Anaconda. For more information, please visit: https://www.anaconda.com/download
    - Install Dependencies: Install the following Python Packages within your python environment:
        + pip install google-generativeai
        + pip install google-api-core
        + pip install customtkinter
        + pip install pillow
        + pip install pyinstaller
    -	Execute the following command to render the AI Pair Programming Assistant GUI within your python environment:
                                  python aipp_gui.py
    -	(Additional) Build an executable using the following command within your python environment:
            pyinstaller --onefile --add-data "icons;icons" aipp_gui.py.py

NOTE:
1.	The GUI application requires an internet connection for API key validation (explained in scenario walkthrough).
2.	Running the executable takes some time to load initially. Please be patient while it loads. Once loaded, the operations on the GUI are carried out smoothly, assuming the hardware and software requirements mentioned above have been met.
