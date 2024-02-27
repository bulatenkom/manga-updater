class AppEx(Exception):
    def __init__(self, *args: object, http_status=500) -> None:
        super().__init__(*args)
        self.http_status = http_status