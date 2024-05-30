from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
def is_valid_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=400)

    if date < timezone.now().date():
        return Response({"message": "The date is in the past."}, status=200)