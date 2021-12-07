import azure.cognitiveservices.speech as speechsdk


class SpeechTranslator:
    def __init__(self, audio_lang: str, target_lang: str, subscription_key: str, region: str):
        self.audio_lang = audio_lang
        self.target_lang = target_lang
        self.config = speechsdk.translation.SpeechTranslationConfig(
            subscription=subscription_key,
            region=region,
            speech_recognition_language=self.audio_lang,
            target_languages=(self.target_lang,),
        )

    def translate_audio(self, filename: str):
        audio_config = speechsdk.AudioConfig(filename=filename)

        recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=self.config,
            audio_config=audio_config,
        )

        result = recognizer.recognize_once()
        translated_text = self._get_result_text(
            reason=result.reason,
            result=result,
        )

        return translated_text

    def _get_result_text(
        self,
        reason: speechsdk.ResultReason,
        result: speechsdk.translation.TranslationRecognitionResult,
    ) -> str:
        reason_format = {
            speechsdk.ResultReason.TranslatedSpeech: f"{result.translations[self.target_lang]}",
            speechsdk.ResultReason.RecognizedSpeech: f'Recognized: "{result.text}"',
            speechsdk.ResultReason.NoMatch: f"No speech could be recognized: {result.no_match_details}",
            speechsdk.ResultReason.Canceled: f"Speech Recognition canceled: {result.cancellation_details}",
        }
        return reason_format.get(reason, "Unable to recognize speech")
