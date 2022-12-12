from turtle import color
from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def map_age_to_key(dataframe):
    for i in dataframe["Age"].keys():
        if dataframe["Age"][i] == 25:
            dataframe["Age"][i] = 36
        elif dataframe["Age"][i] == 26:
            dataframe["Age"][i] = 48
        elif dataframe["Age"][i] == 27:
            dataframe["Age"][i] = 60
        elif dataframe["Age"][i] == 28:
            dataframe["Age"][i] = 72
        elif dataframe["Age"][i] == 29:
            dataframe["Age"][i] = 84
        elif dataframe["Age"][i] == 30:
            dataframe["Age"][i] = 96
        elif dataframe["Age"][i] == 31:
            dataframe["Age"][i] = 108
        elif dataframe["Age"][i] == 32:
            dataframe["Age"][i] = 120


def bmi_plot_df_helper():
    df = pd.read_csv('data/app_input_data_med.csv')

    df_patient_id = df[df["person_id"] == patientID]
    df_patient_id_with_age_not_zero = df_patient_id[df_patient_id["Age"] != 0]

    for i in df_patient_id_with_age_not_zero["value"].keys():
        if(not(isfloat(df_patient_id_with_age_not_zero["value"][i]))):
            df_patient_id_with_age_not_zero = df_patient_id_with_age_not_zero.drop([i])


    df_patient_id_with_age_not_zero.rename(columns={'value': 'BMI Percentile'}, inplace=True)
    
    df_patient_id_with_age_not_zero = df_patient_id_with_age_not_zero.drop(['feat_dict', 'age_dict', 'person_id'], axis=1)

    df_after_2_years = pd.read_csv('data/dec_output.csv')
    df_after_2_years_with_patient_id = df_after_2_years[df_after_2_years["person_id"] == patientID]
    df_after_2_years_with_patient_id_age_not_zero = df_after_2_years_with_patient_id[df_after_2_years_with_patient_id["Age"] != 0]
    
    df_after_2_years_with_patient_id_age_not_zero = df_after_2_years_with_patient_id_age_not_zero.drop(['person_id', 'label', 'Predicted'], axis=1)
    df_after_2_years_with_patient_id_age_not_zero = df_after_2_years_with_patient_id_age_not_zero[df_after_2_years_with_patient_id_age_not_zero['BMIp'] != 0]
    df_after_2_years_with_patient_id_age_not_zero.rename(columns={'BMIp': 'BMI Percentile'}, inplace=True)
    

    map_age_to_key(df_after_2_years_with_patient_id_age_not_zero)

    frames = [df_patient_id_with_age_not_zero, df_after_2_years_with_patient_id_age_not_zero]
    
    new_df = pd.concat(frames)
    new_df['BMI Percentile'] = new_df['BMI Percentile'].astype('float')

    return new_df, df_patient_id_with_age_not_zero, df_after_2_years_with_patient_id_age_not_zero


@app.route('/')
def hello():
    return render_template('launch.html')

@app.route('/select', methods=["POST", "GET"])
def selectScreen():
    output = request.form.to_dict()
    global patientID
    global str_patientID

    if(output["firstName"] == '' or output["lastName"] == '' or output["patientID"] == ''):
        return render_template('error.html', message="Error! Patient Not Found. Go back to the previous page and check Login Details.")

    if(int( output["patientID"]) < 1 or int( output["patientID"]) > 8):
         return render_template('error.html', message="Patient ID not valid. Go back to the previous page and check Login Details.")

    str_patientID = output["patientID"]
    patientID = float(output["patientID"])
    return render_template('selectScreenPage.html')

@app.route('/bmi_historical', methods=["POST", "GET"])
def bmiHistorical():
    plt.rcParams["figure.figsize"] = [7.50, 4.50]
    plt.rcParams["figure.autolayout"] = True

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    new_df, df_patient_id_with_age_not_zero, df_after_2_years_with_patient_id_age_not_zero = bmi_plot_df_helper()

    axis.plot(new_df["Age"], new_df["BMI Percentile"], color='red', linewidth=2, marker = 'o', markersize=7)
    axis.set_title('BMI Percentile vs Age (in months)', fontsize=15)
    axis.set_xlabel('Age (in months)', fontsize=15)
    axis.set_ylabel('BMI Percentile', fontsize=15)
    axis.set_xticks(np.arange(min(df_patient_id_with_age_not_zero["Age"]), max(df_after_2_years_with_patient_id_age_not_zero["Age"])+3, 3.0), fontsize=12)
    axis.set_yticks(np.arange(0.0, 110.0, 10.0), fontsize=15)
    axis.axhline(y=5, color='b', linestyle = '--')
    axis.axhline(y=85, color='b', linestyle = '--')
    axis.axhline(y=95, color='b', linestyle = '--')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    

@app.route('/bmi_historical_predicted', methods=["POST", "GET"])
def bmiHistoricalPredicted():

    plt.rcParams["figure.figsize"] = [18.50, 7.50]
    plt.rcParams["figure.autolayout"] = True


    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    new_df, df_patient_id_with_age_not_zero, df_after_2_years_with_patient_id_age_not_zero = bmi_plot_df_helper()
    final_age_hist = int(new_df.iloc[-1]["Age"])
    print("final_age_hist", final_age_hist)

    df_predicted = pd.read_csv('data/dec_output.csv')
    df_predicted_with_patient_id = df_predicted[df_predicted["person_id"] == patientID]
    df_predicted_with_patient_id_age_not_zero = df_predicted_with_patient_id[df_predicted_with_patient_id["Age"] != 0]

    map_age_to_key(df_predicted_with_patient_id_age_not_zero)
    
    df_predicted_with_patient_id_age_not_zero = df_predicted_with_patient_id_age_not_zero[df_predicted_with_patient_id_age_not_zero["Age"] >= final_age_hist]
    df_predicted_with_patient_id_age_not_zero = df_predicted_with_patient_id_age_not_zero.drop(['person_id', 'label', 'BMIp'], axis=1)


    axis.plot(new_df["Age"], new_df["BMI Percentile"], color='red', linewidth=2, marker = 'o', markersize=7)
    axis.plot(df_predicted_with_patient_id_age_not_zero["Age"], df_predicted_with_patient_id_age_not_zero["Predicted"], color='green', linewidth=2, marker = 'o', markersize=7)

    axis.set_title('BMI Percentile vs Age (in months)', fontsize=15)
    axis.set_xlabel('Age (in months)', fontsize=15)
    axis.set_ylabel('BMI Percentile', fontsize=15)
    axis.set_xticks(np.arange(min(df_patient_id_with_age_not_zero["Age"]), max(df_predicted_with_patient_id_age_not_zero["Age"])+3, 3.0), fontsize=15)
    axis.set_yticks(np.arange(0.0, 110.0, 10.0), fontsize=15)
    axis.axhline(y=5, color='b', linestyle = '--')
    axis.axhline(y=85, color='b', linestyle = '--')
    axis.axhline(y=95, color='b', linestyle = '--')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/ehr_historical', methods=["POST", "GET"])
def ehrHistorical():

    df = pd.read_csv('data/app_input_data_med.csv')
    df_patient_id = df[df["person_id"] == patientID]
    df_patient_id_with_age_not_zero = df_patient_id[df_patient_id["Age"] != 0]

    for i in df_patient_id_with_age_not_zero["value"].keys():
        if(isfloat(df_patient_id_with_age_not_zero["value"][i])):
            df_patient_id_with_age_not_zero = df_patient_id_with_age_not_zero.drop([i])

    df_patient_id_with_age_not_zero = df_patient_id_with_age_not_zero.drop(columns=['feat_dict', 'age_dict' , 'person_id'], axis=1)

    age_medication_diagnosis_dict = {}
    for i in df_patient_id_with_age_not_zero["value"].keys():
        if df_patient_id_with_age_not_zero["Age"][i] not in age_medication_diagnosis_dict:
            age_medication_diagnosis_list = []
            age_medication_diagnosis_list.append(df_patient_id_with_age_not_zero["value"][i])
            age_medication_diagnosis_dict[df_patient_id_with_age_not_zero["Age"][i]] = age_medication_diagnosis_list
        else:
            age_medication_diagnosis_dict[df_patient_id_with_age_not_zero["Age"][i]].append(df_patient_id_with_age_not_zero["value"][i])
    age_medication_diagnosis_dict

    df_new = pd.read_csv('data/app_dec_input.csv')
    df_patient_id_new = df_new[df_new["person_id"] == patientID]
    df_patient_id_with_age_not_zero_new = df_patient_id_new[df_patient_id_new["Age"] != 0]
    df_patient_id_with_age_not_zero_new.replace(0.0, np.nan, inplace=True)
    df_patient_id_with_age_not_zero_new_non_nan=df_patient_id_with_age_not_zero_new.dropna(axis=1,how='all')
    df_patient_id_with_age_not_zero_new_non_nan = df_patient_id_with_age_not_zero_new_non_nan.drop(columns=['person_id'], axis=1)

    column_list = list(df_patient_id_with_age_not_zero_new_non_nan.columns.values)
    column_list.remove('Age')
    column_list
    for i in df_patient_id_with_age_not_zero_new_non_nan["Age"].keys():
        for j in column_list:
            if(df_patient_id_with_age_not_zero_new_non_nan[j][i] != np.nan):
                if df_patient_id_with_age_not_zero_new_non_nan["Age"][i] not in age_medication_diagnosis_dict:
                    age_medication_diagnosis_list = []
                    age_medication_diagnosis_list.append(j)
                    age_medication_diagnosis_dict[df_patient_id_with_age_not_zero_new_non_nan["Age"][i]] = age_medication_diagnosis_list
                else:
                    age_medication_diagnosis_dict[df_patient_id_with_age_not_zero_new_non_nan["Age"][i]].append(j)
    

    headings = ("Age (in months)", "EHR Variables")

    age_medication_diagnosis_dict_to_tuple = tuple(zip(age_medication_diagnosis_dict.keys(), age_medication_diagnosis_dict.values()))

    return render_template("ehrTable.html", headings=headings, data= age_medication_diagnosis_dict_to_tuple)


@app.route('/rank_features', methods=["POST", "GET"])
def rankFeatures():
    file_initial = 'data/output/full_contri_'
    df = pd.read_csv(file_initial + str_patientID + '_0.csv')
    file_initial = 'data/output/full_contri_' + str_patientID + '_'
    initial_age = 3
    df["Age"] = initial_age
    for i in range(1,8):
        file_name = ''
        file_name = file_initial + str(i) +'.csv' 
        print(file_name)
        df_new = pd.read_csv(file_name)
        df_new["Age"] = initial_age + 1
        index= df_new.index + df.index.stop
        df_new.index= index
        df = pd.concat([df, df_new], axis=0)
        initial_age += 1 

    for i in df['Age'].keys():
        if (isfloat(df['feat'][i])):
            df = df.replace(df['feat'][i], ('bmi_' + df['feat'][i]))

    df_sorted_by_imp = df.sort_values(by =['imp'], ascending=False)
    df_sorted_by_imp = df_sorted_by_imp[df_sorted_by_imp['feat'] != 'bmi_0']

    df_sorted_by_imp = df_sorted_by_imp.drop(columns=['imp'], axis=1)

    age_feat_dict = {}
    for i in df_sorted_by_imp["Age"].keys():
        if (df_sorted_by_imp["Age"][i] not in age_feat_dict):
            feat_list = []
            feat_list.append(df_sorted_by_imp["feat"][i])
            age_feat_dict[df_sorted_by_imp["Age"][i]] = feat_list
        else:
            age_feat_dict[df_sorted_by_imp["Age"][i]].append(df_sorted_by_imp["feat"][i])
    
    sorted_age_feat_dict = {}
    for key in sorted(age_feat_dict.keys()) :
        sorted_age_feat_dict[key] = age_feat_dict[key]

    headings = ("Age (in years)", "Rank Features")


    sorted_age_feat_dict_to_tuple = tuple(zip(sorted_age_feat_dict.keys(), sorted_age_feat_dict.values()))

    return render_template("rankTable.html", headings=headings, data= sorted_age_feat_dict_to_tuple)


if __name__ == "__main__":
    app.run(debug=True)
