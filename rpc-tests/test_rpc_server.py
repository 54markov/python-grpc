#! /usr/bin/python

import time
from concurrent import futures

import grpc
import data_model_pb2
import data_model_pb2_grpc


class TestRpcServer(data_model_pb2_grpc.TestRpcServicer):
    def SimpleRpc(self, request, context):
        print("Invoked: SimpleRpc - {}".format(request.request_data))
        return data_model_pb2.Responce(responce_data="{} -> OK!".format(request.request_data))


    def ResponseStreamRpc(self, request, context):
        print("Invoked: ResponseStreamRpc - {}".format(request.request_data))
        for i in range(0, 3):
            yield data_model_pb2.Responce(responce_data="{} -> {} OK!".format(request.request_data, i))


    def RequestStreamRpc(self, request_iterator, context):
        print("Invoked: RequestStreamRpc - ")
        for request in request_iterator:
            print("\t{}".format(request.request_data))

        return data_model_pb2.Responce(responce_data="RequestStreamRpc -> OK!")


    def BidirectionalStream(self, request_iterator, context):
        print("Invoked: BidirectionalStream - ")
        requests = []
        for request in request_iterator:
            requests.append(request)
            print("\t{}".format(request.request_data))

        for i, request in enumerate(requests):
            yield data_model_pb2.Responce(responce_data="{} -> {} OK!".format(request.request_data, i))


def main():
    # Creates a @server with which RPCs can be serviced
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_model_pb2_grpc.add_TestRpcServicer_to_server(TestRpcServer(), server)

    print("Starting server on port 6061...")
    # Opens an insecure port for accepting RPCs
    server.add_insecure_port('[::]:6061')
    server.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("Closing server on port 6061...")
        server.stop(0)


if __name__ == '__main__':
    main()
