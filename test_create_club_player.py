import grpc
import pytest
import club_player_service_pb2
import club_player_service_pb2_grpc
from functions import generate_guid
from global_vars import server


@pytest.fixture(scope="module")
def grpc_channel():
    """Создание gRPC-канала для подключения к серверу"""
    with grpc.insecure_channel(server) as channel:
        yield channel


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    """Создание gRPC-клиентского стаба"""
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


def test_create_club_player(grpc_stub,generatePlayerGuid,generateClubGuid):

    request = club_player_service_pb2.CreateClubPlayerRequest(
        player=club_player_service_pb2.ClubPlayerRequest(
            player_guid=generatePlayerGuid,
            club_guid=generateClubGuid
        ),
        player_club_role=club_player_service_pb2.PlayerClubRole.PLAYER
    )

    # Act
    response = grpc_stub.CreateClubPlayer(request)

# Assert
    assert response.player_guid == generatePlayerGuid
    assert response.club_guid == generateClubGuid
    assert len(response.guid) == 36


def test_get_clubs_player(grpc_stub,generatePlayerGuid,generateClubGuid):
    # Создание запроса на создание нового игрока клуба
    request = club_player_service_pb2.ClubPlayersRequest(
        club_guid=generateClubGuid
    )

    # Отправка запроса на сервер и получение ответа
    response = grpc_stub.GetClubPlayers(request)
    # Assert
    assert response.players[0].player_guid == generatePlayerGuid
    assert response.players[0].club_guid == generateClubGuid




