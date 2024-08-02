import club_player_service_pb2
from conftest import grpc_stub, generatePlayerGuid, generateClubGuid


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




