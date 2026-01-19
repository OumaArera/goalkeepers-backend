from rest_framework.response import Response

class ApiResponse:
    @staticmethod
    def success(data=None, message="Success", status=200, meta=None):
        payload = {
            "success": True,
            "message": message,
            "data": data,
        }
        if meta:
            payload["meta"] = meta
        return Response(payload, status=status)

    @staticmethod
    def error(message="Error", errors=None, status=400):
        payload = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return Response(payload, status=status)
