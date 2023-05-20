from flask import Flask, request
from tempfile import NamedTemporaryFile
import whisper
import torch

# Check if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)

@app.route("/")
def index():
    return "Whisper running!"


@app.route('/whisper', methods=['POST'])
def whisper():
    if not request.files:
        return "Falta el archivo a traducir", 400

    # For each file, let's store the results in a list of dictionaries.
    results = []

    # Loop over every file that the user submitted.
    for handle in request.files.items():
        # Create a temporary file.
        # The location of the temporary file is available in `temp.name`.
        temp = NamedTemporaryFile()
        # Write the user's uploaded file to the temporary file.
        # The file will get deleted when it drops out of scope.
        handle.save(temp)
        # Let's get the transcript of the temporary file.
        result = model.transcribe(temp.name)
        # Now we can store the result object for this file.
        results.append({
            'transcript': result['text'],
        })

    # This will be automatically converted to JSON.
    return {'results': results}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)