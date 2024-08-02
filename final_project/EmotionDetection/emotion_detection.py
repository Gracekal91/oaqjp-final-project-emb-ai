import requests


def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {
        "raw_document": {
            "text": "I love this technology"
        }
    }
    response = requests.post(url, headers=headers, json=input_json)
    response.raise_for_status()
    response_data = response.json()
    print(type(response_data))
    return response_data.get('text', '')


text_to_analyse = {"text": "I ma very happy"}
emotion_detector(text_to_analyse)
