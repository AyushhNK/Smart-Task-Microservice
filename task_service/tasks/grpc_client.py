import grpc
from tasks import auth_pb2, auth_pb2_grpc
def validate_user(token):
    channel = grpc.insecure_channel('localhost:50051')
    stub = auth_pb2_grpc.AuthServiceStub(channel)
    return stub.ValidateToken(auth_pb2.TokenRequest(token=token))