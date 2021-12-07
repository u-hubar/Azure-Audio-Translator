import azure.cognitiveservices.speech as speechsdk


class SpeechTranslator:
    def __init__(self, subscription_key: str, region: str):
        self.config = speechsdk.translation.SpeechTranslationConfig(
            subscription=subscription_key,
            region=region,
        )

    def translate_audio(self, filename: str, audio_lang: str, target_lang: str) -> str:
        self.audio_lang = audio_lang
        self.target_lang = target_lang

        self.config.speech_recognition_language = self.audio_lang
        if self.target_lang not in self.config.target_languages:
            self.config.add_target_language(self.target_lang)

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
            speechsdk.ResultReason.TranslatedSpeech: result.translations[self.target_lang] if self.target_lang in result.translations.keys() else "Target language is not available for this audio",
            speechsdk.ResultReason.RecognizedSpeech: f'Recognized: "{result.text}"',
            speechsdk.ResultReason.NoMatch: f"No speech could be recognized: {result.no_match_details}",
            speechsdk.ResultReason.Canceled: f"Speech Recognition canceled: {result.cancellation_details}",
        }
        return reason_format.get(reason, "Unable to recognize speech")
