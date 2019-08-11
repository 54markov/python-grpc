#! /usr/bin/python

import grpc
import data_model_pb2
import data_model_pb2_grpc


def generate_request_stream(string):
    for i in range(0, 3):
        yield data_model_pb2.Request(request_data="%s %d" % (string, i))


def generate_request(string):
    return data_model_pb2.Request(request_data="%s" % string)


def test_simple_rpc(stub):
    request = generate_request("Simple RPC testing")
    responce = stub.SimpleRpc(request)
    # TODO: what about error checking?
    print responce


def test_responce_stream_rpc(stub):
    request = generate_request("Simple Responce RPC testing")
    stream_responce = stub.ResponseStreamRpc(request)
    # TODO: what about error checking?
    for responce in stream_responce:
        print responce


def test_request_stream_rpc(stub):
    stream_request = generate_request_stream("Simple Request RPC testing")
    responce = stub.RequestStreamRpc(stream_request)
    # TODO: what about error checking?
    print responce


def test_bidirectional_stream_rpc(stub):
    stream_request = generate_request_stream("Simple Bidirectional RPC testing")
    stream_responce = stub.BidirectionalStream(stream_request)
    # TODO: what about error checking?
    for responce in stream_responce:
        print responce


def main():
    print "Starting test rpc clinet..."
    # Creates an insecure @channel to a server.
    # The returned @channel is thread-safe.
    with grpc.insecure_channel("localhost:6061") as channel:
        stub = data_model_pb2_grpc.TestRpcStub(channel)
        test_simple_rpc(stub)
        test_responce_stream_rpc(stub)
        test_request_stream_rpc(stub)
        test_bidirectional_stream_rpc(stub)


if __name__ == '__main__':
    main()
