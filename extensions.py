class APIException(Exception):
    def __init__(self, message="Ошибка при обработке запроса"):
        self.message = message
        super().__init__(self.message)
