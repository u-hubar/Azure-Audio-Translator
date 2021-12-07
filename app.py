from flask import Flask, render_template, request, redirect
from audio.speech_translator import SpeechTranslator
from azure.storage.blob import BlobServiceClient
from utils.config import (
    CS_SUBSCRIPTION_KEY,
    CS_REGION,
    STORAGE_CONNECTION_STRING,
    STORAGE_CONTAINER,
)


speech_translator = SpeechTranslator(
    subscription_key=CS_SUBSCRIPTION_KEY, region=CS_REGION
)
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(STORAGE_CONTAINER)
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""

    if request.method == "POST":
        audio_lang, target_lang = request.form.get('language_from'), request.form.get('language_to') 

        file = request.files.get("file", None)

        if file is None:
            return redirect(request.url)
        elif file.filename == "":
            return redirect(request.url)

        blob_client = blob_service_client.get_blob_client(
            container=STORAGE_CONTAINER, blob=file.filename
        )
        blob_client.upload_blob(file)

        blob_client = container_client.get_blob_client(file.filename)
        with open(file.filename, "wb") as f:
            data = blob_client.download_blob()
            data.readinto(f)

        transcript = speech_translator.translate_audio(file.filename, audio_lang, target_lang)

    return render_template("index.html", transcript=transcript)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
