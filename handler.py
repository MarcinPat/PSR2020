import json
import os
import boto3
import uuid
import pprint
import base64
import smtplib

def detect_faces(photo, bucket, nazwa_pliku_jako_email):

    client=boto3.client('rekognition')
    
    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])
    
    print('Detected faces for ' + photo)    

    try:
        AgeRangeLow = str(response['FaceDetails'][0]['AgeRange']['Low'])
        AgeRangeHigh = str(response['FaceDetails'][0]['AgeRange']['High'])
        AgeRangeMedium = (int(AgeRangeLow) + int(AgeRangeHigh))/2
        body = "Wyczytaliśmy takie liczby : " + str(AgeRangeLow) + str(", ") + str(AgeRangeMedium) + str(" ,") + str(AgeRangeHigh)
    except IndexError:
        body = "ERROR - SYSTEM NIE WYKRYŁ TWARZY"

    ses = boto3.client('ses')

    

    ses.send_email(
        Source='PROSZE_WPISAC_SWOJ_MAIL_Z_SMTP',
        Destination={
            'ToAddresses': [
                nazwa_pliku_jako_email,
            ]
        },
        Message={
            'Subject': {
                'Data': 'SESDEMO TWARZOLICZBY',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': body,
                    'Charset': 'UTF-8'
                }
            }
        }
    )
    
    return len(response['FaceDetails'])

 



def hello(event, context):
    uid = str(uuid.uuid4())
    s3client = boto3.client("s3")
  
    
    #print(event)
    request_body = json.loads(event['body'])

    #print(pprint.pprint(event))
    s3client.put_object(
        Bucket=os.getenv("Bucket"),
        Key=uid,
        Body=base64.b64decode(request_body["file"])
    )
    print("NAZWA oryginalna pliku to {}", request_body["name"])
    
    nazwa_pliku_jako_email = request_body["name"]

    print("File {} save as {}".format(request_body["name"], uid))


    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "uid": uid   #"body": request_body 
    }

    photo=uid
    bucket=os.getenv("Bucket")
    #face_count=detect_faces(photo, bucket)
    detect_faces(photo, bucket, nazwa_pliku_jako_email)
    #print("Faces detected: " + str(face_count))






    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
