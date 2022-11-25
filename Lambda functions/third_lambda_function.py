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
