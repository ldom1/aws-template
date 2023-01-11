import json
import pickle
import numpy as np


def lambda_handler(event, context):
    """
    Input:
        event: List of features
        Example: 
            [5.2, 4.1, 1.5, 0.1]
            [5.8, 2.7, 5.1, 1.9]
    Steps:
        - Load model
        - Get POST body
        - Compute the predictions
        - Return the predictions

    Output:

    {
        'statusCode': 200,
        'body': '{
            "predictions": [
                {"input_data": [5.2, 4.1, 1.5, 0.1], "class_predicted": 0, "label_predicted": "setosa"},
                {"input_data": [5.8, 2.7, 5.1, 1.9], "class_predicted": 2, "label_predicted": "virginica"}
            ]
        }'
    }

    """
    print('Event:', event)

    # Retrieve the data to predict
    body = event['body']
    data_to_predict = json.loads(body)['data_to_predict']
    labels = ['setosa', 'versicolor', 'virginica']

    # Load the model
    model = pickle.load(open('svm_best_model.pkl', 'rb'))

    body = {
        "predictions": [
            {
                "input_data": y,
                "class_predicted": int(model.predict(np.array(y).reshape(1, -1))),
                "label_predicted": labels[int(model.predict(np.array(y).reshape(1, -1)))],
            }
            for y in data_to_predict
        ]
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body),
    }
