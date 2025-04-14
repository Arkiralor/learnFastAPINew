class NotFoundException(Exception):
    def __init__(self, detail: str = "Resource not found"):
        self.status_code = 404
        self.detail = detail

    def to_dict(self):
        return {
            "error": {
                "code": "not_found",
                "message": self.detail
            }
        }