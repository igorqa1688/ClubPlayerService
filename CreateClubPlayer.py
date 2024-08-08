import grpc
import club_player_service_pb2
import club_player_service_pb2_grpc
from functions import generate_guid, randomPlayerRole
from global_vars import server


def grpc_channel():
    #Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        yield channel


def create_club_player_none():
    playerGuid = generate_guid()
    clubGuid = generate_guid()
    # Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)

        # Создание запроса на создание нового игрока клуба
        request = club_player_service_pb2.CreateClubPlayerRequest(
            player=club_player_service_pb2.ClubPlayerRequest(
                player_guid=playerGuid,
                club_guid=clubGuid
            ),
            player_club_role=0
        )

        try:
            # Отправка запроса на сервер и получение ответа
            response = stub.CreateClubPlayer(request)
            print(response.player_club_role)
            return response
        except Exception as execpt:
            print(execpt)
            return 1


def create_club_player():
    playerGuid = generate_guid()
    clubGuid = generate_guid()
    # Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)

        # Создание запроса на создание нового игрока клуба
        request = club_player_service_pb2.CreateClubPlayerRequest(
            player=club_player_service_pb2.ClubPlayerRequest(
                player_guid=playerGuid,
                club_guid=clubGuid
            ),
            player_club_role=1
        )

        try:
            # Отправка запроса на сервер и получение ответа
            response = stub.CreateClubPlayer(request)
            print(response.player_club_role)
            return response
        except Exception as execpt:
            print(execpt)
            return 1


def get_clubs_player():
    try:
        created_user = create_club_player()
    except Exception as e:
        print(e)
        return 1
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


