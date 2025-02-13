class OpenAIEmptyResponseError(Exception):
    pass


class LanguageCodeNotRecognizedError(Exception):
    def __init__(self, language_code: str):
        self.language_code = language_code

    def __str__(self):
        return f"The language code {self.language_code} is not recognized. Make sure to enter a valid ISO 639-3 code. For example, `eng` for English"
