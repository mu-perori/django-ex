# backendApi.jsのPython版
# url = "https://api.us.apiconnect.ibmcloud.com/spbodieusibmcom-kenishia/sb/"

# getPatientInfo
def get_patient_info(url, patient_id):
    patient_info = {
        "name": patient_id,
        "age": 38,
        "gender": "male",
        "street": "34 Main Street",
        "city": "Toronto",
        "zipcode": "M5H 1T1"
    }
    return patient_info


# getPatientMedications


# getPatientAppointments



# getPatientMeasurements



# patientLogin
def patient_login(url, username, password):
    return username


# getAge（getPatientInfoで使用）

