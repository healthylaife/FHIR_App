# FHIR_App

## Instructions to run the app: 

1. First we need a virtual environment. Follow the commands to create a virtual environment for your project. These are the commands for windows.

  **python -m virtualenv venv**

  **venv/Scripts/Activate**

2. Pip install the required packages.

  **pip install flask** 

3. Other libraries can be also installed the same way: pip install matplotlib, pip install seaborn etc

4. Once you are done with installing the libraries, do '**flask run**' to run the app


## Description of the app:

1. The FHIR_App mainly consists of 3 folders and an app.py file.

    a. 'static' folder : contains logo and background images along with 2 css files: mystyle.css and tables.css
    
    b. 'templates' folder : contains html files for different routes.
    
    c. 'data' folder : which contains the data in the csv files. The data folder is not pushed. 
    
    d. 'app.py' file : main python file which creates all the routes and has the code for processing the data.
    
2. The app shows the BMI trend of a patient (both historical and prediction trends) generated using the data.

3. It also displays an EHR table: age (in months) vs medications given along with other EHR variables. 

4. The last table is the rank features table which ranks/sorts the EHR variables/medications by importance. 
