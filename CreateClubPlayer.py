import grpc
import club_player_service_pb2
import club_player_service_pb2_grpc
from functions import generate_guid
from global_vars import server


playerGuid = generate_guid()
clubGuid = generate_guid()


def create_club_player():
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
        try:
            respJson = response.guid
            print(len(respJson))
        except Exception as execpt:
            print(execpt)


def get_clubs_player():
    # Создание gRPC-канала для подключения к серверу
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)

        # Создание запроса на создание нового игрока клуба
        request = club_player_service_pb2.ClubPlayersRequest(
            club_guid=clubGuid
        )
        # Отправка запроса на сервер и получение ответа
        response = stub.GetClubPlayers(request)
        try:
            respJson = response
            print(respJson)
        except Exception as execpt:
            print(execpt)


create_club_player()

get_clubs_player()