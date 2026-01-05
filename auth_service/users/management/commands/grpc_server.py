import grpc
from concurrent import futures
from django.core.management.base import BaseCommand
# Ensure this import is correct based on your previous fix
from users import auth_pb2_grpc
from users.grpc import AuthService 

class Command(BaseCommand):  # <--- This MUST be named Command
    help = 'Runs the gRPC server'

    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
        # Add your service to the server
        auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
        
        server.add_insecure_port('[::]:50051')
        self.stdout.write(self.style.SUCCESS('gRPC Server started on port 50051'))
        
        server.start()
        server.wait_for_termination()