import grpc
from club_player_service_pb2 import UpdatePlayerTagsRequest, CreateClubPlayerRequest, ClubPlayerRequest, PlayerClubRole
import club_player_service_pb2_grpc
import club_player_service_pb2
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



def update_player_tags( player_guid: str, new_tags: list[str]) -> bool:

    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)
        playerData = {"club_guid": clubGuid, "player_guid": playerGuid}
        tags_guids = new_tags
        request = UpdatePlayerTagsRequest(player=playerData, tags_guids=tags_guids)
        response = stub.UpdatePlayerTags(request)
        print(response)
        return response

channel = grpc.insecure_channel(server)
new_tags = [generate_guid()]
create_club_player()
update_success = update_player_tags(playerGuid, new_tags)