from __future__ import print_function
import grpc
import requests
import threading
import io
from api.pubsub_api_pb2 import * 
from api.pubsub_api_pb2_grpc import * 
#import pubsub_api_pb2 as pb2
#import pubsub_api_pb2_grpc as pb2_grpc
import avro.schema
import avro.io
import time
import certifi
import json
import sqlite3
import sys
 
# append the path of the
# parent directory
sys.path.append(".")
import init.app 

def update_ui(payload):
    print('<<<<Payload in update_ui')
    init.app.index()

def call_api():
    semaphore = threading.Semaphore(1)
    latest_replay_id = None
    '''conn = sqlite3.connect('pubsub.db')
    print ('DB IS OPen')
    print('>>>>>>>DB INSERTION Ends>>>>>>>>')

    cursor = conn.execute("SELECT  auth_token, instance_url from Auth")
    for row in cursor:
        print ("Token = ", row[0])
        print ("Url = ", row[1] +"/n")
        token = row[0]
        url = row[1]
        print ("Operation done successfully");
    conn.close()'''
    
    with open(certifi.where(), 'rb') as f:
        creds = grpc.ssl_channel_credentials(f.read())
    with grpc.secure_channel('api.pubsub.salesforce.com:7443', creds) as channel:
        #GRPC_VERBOSITY=debug
        GRPC_TRACE=all
        authurl = 'https://login.salesforce.com/services/oauth2/token'
        payload={
            'grant_type': 'password',
            'client_id': '3MVG9ZL0ppGP5UrAP59A8.dNkSsWx54hRgtkftFHZh1bxEMSGF6kwnRNA8VheLBe2RHROd01KucH2QHHt5ggh',
            'client_secret': '22883FEE07FDBA0FD71F317F8A4821155253D7853C280B4302EA229A30B1DDEF',
            'username': 'ashutoshexams@gmail.com',
            'password': 'ashutosh9351aozWQvXaav1CPDQaHHgtU7pQy',
            'organizationId': '00D28000000dVa8EAE'
        }
        '''payload = {
            'grant_type': 'password',
            'client_id': clientId,
            'client_secret': clientSecret,
            'username': username,
            'password': password,
        }'''
        res = requests.post(authurl, 
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            data=payload)
        token = ''
        url= ''
        if res.status_code == 200:
            response = res.json()

            access_token = response['access_token']
            instance_url = response['instance_url']
            access_token = access_token.encode(encoding="ascii",errors="ignore").decode('utf-8')
            instance_url = instance_url.encode(encoding="ascii",errors="ignore").decode('utf-8')
            print(access_token)
            print(instance_url)
        token = access_token
        url = instance_url
        print("Token is",token);
        print("url is",url); 
        
        authmetadata = (('accesstoken', token),('instanceurl', url),('tenantid', '00D28000000dVa8EAE'))


        #stub = pb2_grpc.PubSubStub(channel)
        stub = PubSubStub(channel)
        def fetchReqStream(topic):
            while True:
                semaphore.acquire()
                #yield pb2.FetchRequest(
                yield FetchRequest(
                    topic_name = topic,
                    #replay_preset = pb2.ReplayPreset.LATEST,
                    replay_preset = ReplayPreset.LATEST,
                    num_requested = 1)

        def decode(schema, payload):
            schema = avro.schema.parse(schema)
            buf = io.BytesIO(payload)
            decoder = avro.io.BinaryDecoder(buf)
            reader = avro.io.DatumReader(schema)
            ret = reader.read(decoder)
            return ret

        mysubtopic = "/data/AccountChangeEvent"
        print('Subscribing to ' + mysubtopic)
        print(authmetadata)
        substream = stub.Subscribe(fetchReqStream(mysubtopic),
                metadata=authmetadata)
        for event in substream:
            if event.events:
                semaphore.release()
                print("Number of events received: ", len(event.events))
                payloadbytes = event.events[0].event.payload
                schemaid = event.events[0].event.schema_id
                schema = stub.GetSchema(
                        #pb2.SchemaRequest(schema_id=schemaid),
                        SchemaRequest(schema_id=schemaid),
                        metadata=authmetadata).schema_json
                decoded = decode(schema, payloadbytes)
                
                print("Got an event!", json.dumps(decoded))
                update_ui(json.dumps(decoded));
            else:
                print("[", time.strftime('%b %d, %Y %l:%M%p %Z'),
                "] The subscription is active.")
                latest_replay_id = event.latest_replay_id 
    print('>>>> MAIN API CAlled')


    

