from concurrent import futures
import subprocess
import grpc

import raft_pb2 as pb
import raft_pb2_grpc as pb_grpc

class FrontEndService(pb_grpc.FrontEndServicer):
    def Get(self, request, context):
        return pb.Reply(error="Not implemented", wrongLeader=True)
    
    def Put(self, request, context):
        return pb.Reply(error="Not implemented", wrongLeader=True)
    
    def StartRaft(self, request, context):
        start_raft(request.arg)
        return pb.Reply(value="Started Raft cluster of size {request.arg}")
    
    def StartServer(self, request, context):
        start_server(request.arg)
        return pb.Reply(value=f"Server {request.arg} started")

def start_server(server_id):
    cmd = ["python", "server.py", str(server_id)]
    process = subprocess.Popen(
        ["bash", "-c", f"exec -a raftserver{server_id+1} python server.py {server_id}"]
    )

def start_raft(num_servers):
    for i in range(num_servers):
        process = subprocess.Popen(
            ["bash", "-c", f"exec -a raftserver{i+1} python server.py {i}"]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_FrontEndServicer_to_server(FrontEndService(), server)
    server.add_insecure_port("127.0.0.1:8001")
    server.start()
    print("[frontend] listening on 127.0.0.1:8001", flush=True)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()