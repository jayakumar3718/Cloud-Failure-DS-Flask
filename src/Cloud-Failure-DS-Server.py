from glob import glob
from PIL import Image
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
import os
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
matplotlib.use('Agg')



app = Flask(__name__)
app.secret_key = "MySecret"
ctx = app.app_context()
ctx.push()

with ctx:
    pass
user_id = ""
emailid = ""

message = ""
msgType = ""
uploaded_file_name = ""


def initialize():
    global message, msgType
    message = ""
    msgType = ""


@app.route("/")
def index():
    global user_id, emailid
    return render_template("Login.html")


@app.route("/processLogin", methods=["POST"])
def processLogin():
    global user_id, emailid
    emailid = request.form["emailid"]
    password = request.form["password"]
    sdf = pd.read_csv("static/System.csv")
    print(sdf, "XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    for k, v in sdf.iterrows():
        if v['emailid'] == emailid and str(v['password']) == password:
            return render_template("Dashboard.html")
    return render_template("Login.html", processResult="Invalid UserID and Password")


@app.route("/ChangePassword")
def changePassword():
    global user_id, emailid
    return render_template("ChangePassword.html")


@app.route("/ProcessChangePassword", methods=["POST"])
def processChangePassword():
    global user_id, emailid
    oldPassword = request.form["oldPassword"]
    newPassword = request.form["newPassword"]

    return render_template("ChangePassword.html", msg="Password Changed Successfully")


@app.route("/Dashboard")
def Dashboard():
    global user_id, emailid
    return render_template("Dashboard.html")


@app.route("/Information")
def Information():
    global message, msgType
    return render_template("Information.html", msgType=msgType, message=message)


def get_datasets():
    file_list = os.listdir("static/Dataset")
    print(file_list)
    return file_list


fault_severity_df = None
event_type_df = None
severity_type_df = None
log_feature_df = None
resource_type_df = None
data_dir = 'static/Cloud-Failure-Dataset'




def load_dataset():
    global fault_severity_df, event_type_df, severity_type_df, log_feature_df, resource_type_df
    if fault_severity_df is None:
        fault_severity_df = pd.read_csv(f'{data_dir}/train.csv')
    if event_type_df is None:
        event_type_df = pd.read_csv(f'{data_dir}/event_type.csv')
    if severity_type_df is None:
        severity_type_df = pd.read_csv(f'{data_dir}/severity_type.csv')
    if log_feature_df is None:
        log_feature_df = pd.read_csv(f'{data_dir}/log_feature.csv')
    if resource_type_df is None:
        resource_type_df = pd.read_csv(f'{data_dir}/resource_type.csv')


load_dataset()


@app.route("/FaultSeverityDatasetInfo")
def FaultSeverityDatasetInfo():
    return render_template("FaultSeverityDatasetInfo.html", displayResult=False)


@app.route("/ProcessFaultSeverityDatasetInfo", methods=['POST'])
def process_FaultSeverityDatasetInfo():
    global fault_severity_df

    no_of_rows = len(fault_severity_df.index)
    no_of_unique_locations = len(fault_severity_df.location.unique())
    no_of_unique_fault_severity = len(fault_severity_df.fault_severity.unique())
    return render_template("FaultSeverityDatasetInfo.html", displayResult=True, fault_severity_df=fault_severity_df,  no_of_rows=no_of_rows, no_of_unique_locations=no_of_unique_locations, no_of_unique_fault_severity = no_of_unique_fault_severity)

@app.route("/EventTypeDatasetInfo")
def EventTypeDatasetInfo():
    return render_template("EventTypeDatasetInfo.html", displayResult=False,)


@app.route("/ProcessEventTypeDatasetInfo", methods=['POST'])
def process_EventTypeDatasetInfo():
    no_of_rows = len(event_type_df.index)
    return render_template("EventTypeDatasetInfo.html", displayResult=True, event_type_df=event_type_df,
                           no_of_rows=no_of_rows)


@app.route("/ResourceTypeDatasetInfo")
def ResourceTypeDatasetInfo():
    return render_template("ResourceTypeDatasetInfo.html", displayResult=False)


@app.route("/ProcessResourceTypeDatasetInfo", methods=['POST'])
def process_ResourceTypeDatasetInfo():
    no_of_rows = len(resource_type_df.index)

    return render_template("ResourceTypeDatasetInfo.html", displayResult=True, resource_type_df=resource_type_df,
                           no_of_rows=no_of_rows)


@app.route("/SeverityTypeDatasetInfo")
def SeverityTypeDatasetInfo():
    return render_template("SeverityTypeDatasetInfo.html", displayResult=False)


@app.route("/ProcessSeverityTypeDatasetInfo", methods=['POST'])
def process_SeverityTypeDatasetInfo():
    no_of_rows = len(severity_type_df.index)

    return render_template("SeverityTypeDatasetInfo.html", displayResult=True, severity_type_df=severity_type_df,
                           no_of_rows=no_of_rows)

@app.route("/FeatureDatasetInfo")
def FeatureDatasetInfo():
    return render_template("FeatureDatasetInfo.html", displayResult=False)
@app.route("/ProcessFeatureDatasetInfo", methods=['POST'])
def process_FeatureDatasetInfo():
    no_of_rows = len(log_feature_df.index)
    return render_template("FeatureDatasetInfo.html", displayResult=True, log_feature_df=log_feature_df,
                           no_of_rows=no_of_rows)
@app.route("/FaultClassCount")
def FaultClassCount():
    return render_template("FaultClassCount.html", displayResult=False)
@app.route("/ProcessFaultClassCount", methods=['POST'])
def process_FaultClassCount():
    fs_vc = fault_severity_df["fault_severity"].value_counts()
    plt.Figure(figsize=(12,12))
    plt.bar(x=fs_vc.index, height=fs_vc.values, width=0.5, color="orange")
    plt.title("Fault Severity")
    plt.xlabel("Fault Severity")
    plt.ylabel("Fault Severity Class wise Count")
    plt.savefig("static/Output/FaultClassCount.png")
    return render_template("FaultClassCount.html", displayResult=True)
@app.route("/ResourceTypeClassCount")
def ResourceTypeClassCount():
    return render_template("ResourceTypeClassCount.html", displayResult=False)
@app.route("/ProcessResourceTypeClassCount", methods=['POST'])
def process_ResourceTypeClassCount():
    resource_type_vc = resource_type_df["resource_type"].value_counts().head(7)
    plt.Figure(figsize=(18,18))
    pie = plt.pie(x = resource_type_vc.values, labels=resource_type_vc.index, autopct='%1.1f%%', textprops={"fontsize":14},
            colors=sns.color_palette("Set1"), shadow=True)
    plt.title('Resource Type wise Count')
    plt.legend(pie[0], labels=resource_type_vc.index, loc="best")
    plt.savefig("static/Output/ResourceTypeClassCount.png")
    return render_template("ResourceTypeClassCount.html", displayResult=True)
@app.route("/Prediction")
def Prediction():
    return render_template("Prediction.html", displayResult=False)
@app.route("/ProcessPrediction", methods=['POST'])
def process_Prediction():
    eventtype1 = request.form["eventtype1"]
    eventtype2 = request.form["eventtype2"]
    eventtype3 = request.form["eventtype3"]
    eventtype4 = request.form["eventtype4"]
    eventtype5 = request.form["eventtype5"]
    eventtype6 = request.form["eventtype6"]
    eventtype7 = request.form["eventtype7"]
    eventtype8 = request.form["eventtype8"]
    fault_severity_1_list = [['1','0','0','0','0','0','0','0'], ['0','1','0','0','0','0','1','0'], ['1','1','1','0','0','0','0','0'], ['0','1','1','0','0','1','0','0'], ['0','0','0','0','0','0','1','0'], ['0','1','0','1','0','0','0','0']]
    fault_severity_2_list = [['0', '1', '0', '0', '0', '0', '0', '0'], ['1', '0', '0', '1', '1', '0', '1', '0'],
                             ['1', '0', '0', '1', '0', '0', '1', '0'], ['1', '1', '1', '1', '0', '1', '0', '0'],
                             ['1', '1', '0', '0', '0', '0', '1', '0'], ['1', '1', '1', '1', '0', '0', '0', '0']]
    fault_severity_3_list = [['0', '0', '1', '0', '0', '0', '0', '0'], ['0', '0', '0', '1', '1', '1', '1', '0'],
                             ['-', '0', '1', '0', '1', '0', '1', '1'], ['0', '1', '1', '0', '0', '1', '1', '1'],
                             ['1', '1', '0', '1', '1', '0', '1', '1'], ['1', '1', '1', '1', '0', '0', '1', '1']]
    fault_message = ""
    input_list = [eventtype1,eventtype2, eventtype3, eventtype4, eventtype5, eventtype6, eventtype7, eventtype8]
    print(input_list)
    if input_list in fault_severity_1_list:
        fault_message =  "Fault Severity 1"
    elif input_list in fault_severity_2_list:
        fault_message =  "Fault Severity 2"
    elif input_list in fault_severity_3_list:
        fault_message =  "Fault Severity 3"
    else:
        fault_message = "No Fault"
    return render_template("Prediction.html", displayResult=True, eventtype1=eventtype1, eventtype2=eventtype2, eventtype3=eventtype3, eventtype4=eventtype4, eventtype5=eventtype5, eventtype6=eventtype6, eventtype7=eventtype7, eventtype8=eventtype8, fault_message=fault_message)
if __name__ == "__main__":
    app.run()