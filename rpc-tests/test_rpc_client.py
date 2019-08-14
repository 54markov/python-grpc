#! /usr/bin/python

import grpc

import data_model_pb2
import data_model_pb2_grpc


def generate_request_stream(string):
    for i in range(0, 3):
        yield data_model_pb2.Request(request_data="{} {}".format(string, i))


def generate_request(string):
    return data_model_pb2.Request(request_data="{}".format(string))


def test_simple_rpc(stub):
    request = generate_request("Simple RPC testing")
    try:
        responce = stub.SimpleRpc(request)
    except grpc.RpcError as rpc_error:
        print("{0}: {1}".format(rpc_error.code(), rpc_error.details()))
    else:
        print("{}".format(responce))


def test_responce_stream_rpc(stub):
    request = generate_request("Simple Responce RPC testing")
    try:
        stream_responce = stub.ResponseStreamRpc(request)
    except grpc.RpcError as rpc_error:
        print("{0}: {1}".format(rpc_error.code(), rpc_error.details()))
    else:
        for responce in stream_responce:
            print responce


def test_request_stream_rpc(stub):
    stream_request = generate_request_stream("Simple Request RPC testing")
    try:
        responce = stub.RequestStreamRpc(stream_request)
    except grpc.RpcError as rpc_error:
        print("{0}: {1}".format(rpc_error.code(), rpc_error.details()))
    else:
        print(responce)


def test_bidirectional_stream_rpc(stub):
    stream_request = generate_request_stream("Simple Bidirectional RPC testing")
    try:
        stream_responce = stub.BidirectionalStream(stream_request)
    except grpc.RpcError as rpc_error:
        print("{0}: {1}".format(rpc_error.code(), rpc_error.details()))
    else:    
        for responce in stream_responce:
            print responce


def main():
    print ("Starting test rpc clinet...")
    # Creates an insecure @channel to a server.
    # The returned @channel is thread-safe.
    with grpc.insecure_channel("localhost:6061") as channel:
        stub = data_model_pb2_grpc.TestRpcStub(channel)
        test_simple_rpc(stub)
        test_responce_stream_rpc(stub)
        test_request_stream_rpc(stub)
        test_bidirectional_stream_rpc(stub)
    print("Closing test rpc clinet...")


if __name__ == '__main__':
    main()
