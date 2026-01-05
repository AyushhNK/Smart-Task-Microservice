import jwt
from .models import User


SECRET = "5ahp8kseKOVB_w"


def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        return user
    except Exception:
        return None