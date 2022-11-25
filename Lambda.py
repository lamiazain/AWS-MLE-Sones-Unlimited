import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['key']          ## =ProjectUnit2/test/bicycle_s_000513.png
    bucket = 'sagemaker-us-east-1-777358657826'              ## TODO: fill in

    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket,key,'/tmp/image.png')


    # We read the data from a file
    with open("/tmp/image.png", 'rb') as f:
        image_data = base64.b64encode(f.read())
        print(image_data)

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
##################################################
import json
import boto3
import base64
#from sagemaker.serializers import IdentitySerializer
#import sagemaker.session as session

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2022-11-25-00-24-07-438'  ## TODO: fill in
#session= session.Session()
runtime = boto3.Session().client('sagemaker-runtime')


def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])
    
    # Instantiate a Predictor
   #predictor = sagemaker.predictor.Predictor(endpoint_name=ENDPOINT, sagemaker_session=session) ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    #predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    #inferences  = predictor.predict(image)## TODO: Process the payload with your predictor## TODO: fill in
    
    image_data = event['body']['image_data']
    response = runtime.invoke_endpoint(EndpointName = ENDPOINT, ContentType = 'image/png',Body = image)
    predictions = json.loads(response['Body'].read().decode())
    # We return the data back to the Step Function #Create a new key to the event named   "inferences"  
    event['body']["inferences"] = predictions
    #print(json.dumps(event))
    
    return {
        'statusCode': 200,
        'body': event

        }
######################################################
import json


THRESHOLD = 0.7


def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = event['body']['body']['inferences']## TODO: fill in

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = [True if x>=THRESHOLD else False for x in inferences ] ## TODO: fill in

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if any(meets_threshold):
        pass
    else:
        raise ValueError ("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
