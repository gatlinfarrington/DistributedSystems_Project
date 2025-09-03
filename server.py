from concurrent import futures
import grpc
import argparse

import raft_pb2 as pb
import raft_pb2_grpc as pb_grpc

class KeyValueStoreService(pb_grpc.KeyValueStoreServicer):
    def ping(self, request, context):
        return pb.GenericResponse(success=True)
    
    def GetState(self, request, context):
        return pb.State(term=0, isLeader=False)

def serve():
    server_id, port = parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreService(), server)
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    print(f"[server {server_id}] listening on 127.0.0.1:{port}", flush=True)
    server.wait_for_termination()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_id', type=int, default=None, help='Port to listen on')
    args = parser.parse_args()

    server_id = args.server_id
    if server_id < 0 or server_id > 4:
        raise ValueError("server_id must be between 0 and 4")
    
    port = 9001 + args.server_id

    if port < 1 or port > 65535:
        raise ValueError(f"Port out of range: {port}")
    if args.server_id < 0:
        raise ValueError("server_id must be >= 0")

    return server_id, port

if __name__ == "__main__":
    serve()