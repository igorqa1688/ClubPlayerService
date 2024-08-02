import grpc
import pytest
from functions import generate_guid
from global_vars import server
import club_player_service_pb2_grpc
import club_player_service_pb2


@pytest.fixture(scope="module")
def grpc_channel():
    """Создание gRPC-канала для подключения к серверу"""
    with grpc.insecure_channel(server) as channel:
        yield channel


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    return stub


@pytest.fixture(scope="session")
def generatePlayerGuid():
    playerGuid = generate_guid()
    return playerGuid


@pytest.fixture(scope="session")
def generateClubGuid():
    clubGuid = generate_guid()
    return clubGuid


@pytest.fixture(scope="session")
def createPlayer():
    clubGuid = generate_guid()
    playerGuid = generate_guid()
    # Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)

        # Создание запроса на создание нового игрока клуба
        request = club_player_service_pb2.CreateClubPlayerRequest(
            player=club_player_service_pb2.ClubPlayerRequest(
                player_guid=playerGuid,
                club_guid=clubGuid
            ),
            player_club_role=club_player_service_pb2.PlayerClubRole.PLAYER
        )

        # Отправка запроса на сервер и получение ответа
        response = stub.CreateClubPlayer(request)
        return response

