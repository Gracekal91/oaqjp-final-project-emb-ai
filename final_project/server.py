"""
server.py

A Flask application that provides an endpoint to analyze emotions from a given statement.
The application includes error handling to manage invalid inputs and unexpected errors.

Endpoints:
    - POST /emotionDetector: Receives a JSON body with a 'statement' key, processes the
      statement using the emotion_detector function, and returns the result.

Error Handling:
    - Handles blank or invalid inputs by returning a response with None values.
    - Catches specific exceptions to provide more informative error messages.
"""

from flask import Flask, request, jsonify
import requests
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/emotionDetector', methods=["POST"])
def emotion_detector_route():
    """
    Endpoint to analyze the emotion of a given statement.

    - **POST**: Receives a JSON body with a 'statement' key.
      Processes the statement using the emotion_detector function and returns the result.

    Returns:
        JSON response with the statement, dominant emotion, and emotion scores.
        If the input is invalid or processing fails, returns an error message.
    """
    try:
        data = request.get_json()
        if not data or 'statement' not in data or not data['statement'].strip():
            # Return response with None values for all keys if input is invalid
            return jsonify({
                "statement": None,
                "dominant_emotion": None,
                "emotions": {
                    "anger": None,
                    "disgust": None,
                    "fear": None,
                    "joy": None,
                    "sadness": None
                }
            }), 400

        statement = data['statement']
        result = emotion_detector(statement)

        if result['dominant_emotion'] is None:
            return jsonify({
                "message": "Invalid text! Please try again!",
                "statement": statement,
                "dominant_emotion": result['dominant_emotion'],
                "emotions": result['emotions']
            }), 400

        response = {
            "statement": statement,
            "dominant_emotion": result['dominant_emotion'],
            "emotions": result['emotions']
        }

        return jsonify(response)

    except (KeyError, TypeError, ValueError) as e:
        # Catch specific exceptions for improved error handling
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except requests.RequestException as e:
        # Catch exceptions related to the requests library
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    # Removing the broad exception handling block
    # except Exception as e:
    #     # Catch any other unexpected errors
    #     return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


if __name__ == "__main__":
    app.run(debug=True)
