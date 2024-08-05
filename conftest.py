import grpc
import pytest
from functions import generate_guid, randomPlayerRole
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


# Фикстура создания одного игрока в клубе
@pytest.fixture(scope="session")
def createPlayer():
    clubGuid = generate_guid()
    playerGuid = generate_guid()
    randomPlayerClubRole = randomPlayerRole()

    # Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)

        # Создание запроса на создание нового игрока клуба
        request = club_player_service_pb2.CreateClubPlayerRequest(
            player=club_player_service_pb2.ClubPlayerRequest(
                player_guid=playerGuid,
                club_guid=clubGuid
            ),
            player_club_role=randomPlayerClubRole
        )

        # Отправка запроса на сервер и получение ответа
        response = stub.CreateClubPlayer(request)
        return response


# Фикстура создающая более 1 игрока в клубе
@pytest.fixture(scope="module")
def createPlayersInClub(grpc_channel):
    club_guid = generate_guid()
    players = []
    for _ in range(2):
        player_guid = generate_guid()
        random_player_club_role = randomPlayerRole()
        request = club_player_service_pb2.CreateClubPlayerRequest(
            player=club_player_service_pb2.ClubPlayerRequest(
                player_guid=player_guid,
                club_guid=club_guid
            ),
            player_club_role=random_player_club_role
        )
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
        response = stub.CreateClubPlayer(request)
        players.append(response)
    return players, club_guid


@pytest.fixture(scope="module")
def get_clubs_player(club_guid):
    # Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)

        # Создание запроса на создание нового игрока клуба
        request = club_player_service_pb2.ClubPlayersRequest(
            club_guid=created_user.club_guid
        )
        try:
            # Отправка запроса на сервер и получение ответа
            response = stub.GetClubPlayers(request)
            return response
        except Exception as execpt:
            print(execpt)
            return 1


@pytest.fixture(scope="module")
def delete_club_player(grpc_channel,createPlayersInClub):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    # Вызов фикстуры создающей несколько игроков в клубе
    created_players = createPlayersInClub[0]
    clubs_guids = []
    players_guids = []

    for i in created_players:
        clubs_guids.append(i.club_guid)
        players_guids.append(i.player_guid)

    request = club_player_service_pb2.ClubPlayerRequest(
        club_guid=clubs_guids[0],
        player_guid=players_guids[0])
    try:
        response = stub.DeleteClubPlayer(request)
        return clubs_guids, players_guids
    except Exception as e:
        print(e)
        return 1


# Фикстура создающая игрока в разных клубах
@pytest.fixture(scope="module")
def create_player_in_different_clubs(grpc_channel):
    player_guid = generate_guid()
    players = []
    for _ in range(2):
        club_guid = generate_guid()
        random_player_club_role = randomPlayerRole()
        request = club_player_service_pb2.CreateClubPlayerRequest(
            player=club_player_service_pb2.ClubPlayerRequest(
                player_guid=player_guid,
                club_guid=club_guid
            ),
            player_club_role=random_player_club_role
        )
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
        response = stub.CreateClubPlayer(request)
        players.append(response)
    return players, club_guid