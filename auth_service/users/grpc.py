from users import auth_pb2, auth_pb2_grpc
from .services import validate_token


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def ValidateToken(self, request, context):
        user = validate_token(request.token)
        if not user:
            return auth_pb2.UserResponse(is_active=False)
        return auth_pb2.UserResponse(
            user_id=user.id,
            email=user.email,
            is_active=user.is_active
            )