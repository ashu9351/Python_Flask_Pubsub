import sqlite3
import sys
import json
import os
 
# append the path of the
# parent directory
sys.path.append(".")
import api.client




from flask import Flask, render_template


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pubsub.db')
    conn.row_factory = sqlite3.Row
    return conn

def main_api():
   api.client.call_api()

@app.route('/')
def index():
    conn = get_db_connection()
    main_api()
    all_customers = conn.execute('SELECT * FROM Customers').fetchall()
    conn.close()
    return render_template('index.html',customers=all_customers)





def reflect_account(json_customer):
    HTML_AS_TEXT = """<p>hello world</p>"""
    print('>>> update account called')
    data = json.loads(json_customer)
    event_type = data['ChangeEventHeader']['changeType']

    print('>>>>>In app' , event_type)
    if event_type == 'UPDATE':
        conn = get_db_connection()
        all_customers = conn.execute('SELECT * FROM Customers').fetchall()
        conn.close()
        print('>>>>>>>>>>>>>>>>>>>>>END')
        return render_template('index.html')

    '''{
    "ChangeEventHeader":{
        "entityName":"Account",
        "recordIds":[
            "00128000004ffFXAAY"
        ],
        "changeType":"UPDATE",
        "changeOrigin":"com/salesforce/api/rest/56.0",
        "transactionKey":"000178e4-4a6a-e712-1dfb-22d1264a1ecd",
        "sequenceNumber":1,
        "commitTimestamp":1674484229000,
        "commitNumber":11441167072821,
        "commitUser":"00528000000TIgmAAG",
        "nulledFields":[
            
        ],
        "diffFields":[
            
        ],
        "changedFields":[
            "0x400100"
        ]
    },
    "Name":null,
    "Type":null,
    "ParentId":null,
    "BillingAddress":null,
    "ShippingAddress":null,
    "Phone":null,
    "Fax":null,
    "AccountNumber":"TestDone3",
    "Website":null,
    "Sic":null,
    "Industry":null,
    "AnnualRevenue":null,
    "NumberOfEmployees":null,
    "Ownership":null,
    "TickerSymbol":null,
    "Description":null,
    "Rating":null,
    "Site":null,
    "OwnerId":null,
    "CreatedDate":null,
    "CreatedById":null,
    "LastModifiedDate":1674484229000,
    "LastModifiedById":null,
    "Jigsaw":null,
    "JigsawCompanyId":null,
    "CleanStatus":null,
    "AccountSource":null,
    "DunsNumber":null,
    "Tradestyle":null,
    "NaicsCode":null,
    "NaicsDesc":null,
    "YearStarted":null,
    "SicDesc":null,
    "DandbCompanyId":null,
    "CustomerPriority__c":null,
    "SLA__c":null,
    "Active__c":null,
    "NumberofLocations__c":null,
    "UpsellOpportunity__c":null,
    "SLASerialNumber__c":null,
    "SLAExpirationDate__c":null,
    "Subcategories__c":null,
    "Rating__c":null,
    "Opportunity_Total__c":null,
    "Max_Opportunity__c":null,
    "Test_Cond__c":null,
    "Account_Acceptence_Date__c":null,
    "Test_Picklist__c":null,
    "Potential_Value__c":null,
    "Onboarding_Status__c":null


    }
    #{"ChangeEventHeader": {"entityName": "Account", "recordIds": ["00128000004ffFXAAY"], "changeType": "UPDATE", "changeOrigin": "com/salesforce/api/rest/56.0", "transactionKey": "000178e4-4a6a-e712-1dfb-22d1264a1ecd", "sequenceNumber": 1, "commitTimestamp": 1674484229000, "commitNumber": 11441167072821, "commitUser": "00528000000TIgmAAG", "nulledFields": [], "diffFields": [], "changedFields": ["0x400100"]}, "Name": null, "Type": null, "ParentId": null, "BillingAddress": null, "ShippingAddress": null, "Phone": null, "Fax": null, "AccountNumber": "TestDone3", "Website": null, "Sic": null, "Industry": null, "AnnualRevenue": null, "NumberOfEmployees": null, "Ownership": null, "TickerSymbol": null, "Description": null, "Rating": null, "Site": null, "OwnerId": null, "CreatedDate": null, "CreatedById": null, "LastModifiedDate": 1674484229000, "LastModifiedById": null, "Jigsaw": null, "JigsawCompanyId": null, "CleanStatus": null, "AccountSource": null, "DunsNumber": null, "Tradestyle": null, "NaicsCode": null, "NaicsDesc": null, "YearStarted": null, "SicDesc": null, "DandbCompanyId": null, "CustomerPriority__c": null, "SLA__c": null, "Active__c": null, "NumberofLocations__c": null, "UpsellOpportunity__c": null, "SLASerialNumber__c": null, "SLAExpirationDate__c": null, "Subcategories__c": null, "Rating__c": null, "Opportunity_Total__c": null, "Max_Opportunity__c": null, "Test_Cond__c": null, "Account_Acceptence_Date__c": null, "Test_Picklist__c": null, "Potential_Value__c": null, "Onboarding_Status__c": null}
    conn = get_db_connection()
    all_customers = conn.execute('SELECT * FROM Customers').fetchall()
    conn.close()
    return render_template('index.html',customers=all_customers)'''

