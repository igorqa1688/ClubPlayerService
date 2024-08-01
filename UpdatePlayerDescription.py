import grpc
from club_player_service_pb2 import UpdatePlayerDescriptionRequest, CreateClubPlayerRequest, ClubPlayerRequest, PlayerClubRole
import club_player_service_pb2_grpc
import club_player_service_pb2
from functions import generate_guid, generateUserDescription
from global_vars import server
from CreateClubPlayer import create_club_player



def updatePlayerDescription() -> bool:
    # Вызов функции создания player
    try:
        createdPlayer = create_club_player()
    except Exception as e:
        print(e)
        return 1

    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)
        playerData = {"club_guid": createdPlayer.club_guid, "player_guid": createdPlayer.player_guid}
        playerDescription = generateUserDescription(50)
        request = UpdatePlayerDescriptionRequest(description=playerDescription,player=playerData)
        response = stub.UpdatePlayerDescription(request)
        return response

