# FHIR_App
Electronic health records (EHRs) contain patient-level data collected during a medical visit and consists of multi-modal data insluding demographics, medical history, diagnosis, vital signs, lab measurments, medications, procedures, radioilogy reports. Many machine learning models have been built to predict patient future diagnosis using EHR data. However, due to lack of standard protocol for EHR data these models are difficult to integrate into existing EHR systems and lack interoperability to different EHR systems. Also the output of the clinical prediction models is not easily accessible due to lack of UI that can be integrated to the existing EHR systems.

In this work, we build an API for pediatric patient care leveraging FHIR from Health-Level-7. The objective is to create an API that 1) maps EHR data to FHIR resources, 2) build a clinical prediction model using FHIR resources, and 3) display EHR data and output from prediction model to user-freindly UI.
The clinical predictuon model reads data in FHIR format and gives output in FHIR format. This makes our model interoperable to different EHR syatems provided thaty have an interface to map their EHR data to standard FHIR reources. UI part the complete framework also reads data in FHIR format and can be easily integrated to the clincial prediction model which gives output in FHIR format.

## Table of Contents:
- [Repository Structure](#Repository-Structure)
- [Instructions to run the app](#Instructions-to-run-the-app)



## Repository Structure:

1. The FHIR_App mainly consists of 3 folders and an app.py file.

    a. 'static' folder : contains logo and background images along with 2 css files: mystyle.css and tables.css
    
    b. 'templates' folder : contains html files for different routes.
    
    c. 'data' folder : which contains the data in the csv files. The data folder is not pushed. 
    
    d. 'app.py' file : main python file which creates all the routes and has the code for processing the data.
    
2. The app shows the BMI trend of a patient (both historical and prediction trends) generated using the data.

3. It also displays an EHR table: age (in months) vs medications given along with other EHR variables. 

4. The last table is the rank features table which ranks/sorts the EHR variables/medications by importance. 


## Instructions to run the app: 

1. First we need a virtual environment. Follow the commands to create a virtual environment for your project. These are the commands for windows.

  **python -m virtualenv venv**

  **venv/Scripts/Activate**

2. Pip install the required packages.

  **pip install flask** 

3. Other libraries can be also installed the same way: pip install matplotlib, pip install seaborn etc

4. Once you are done with installing the libraries, do '**flask run**' to run the app
