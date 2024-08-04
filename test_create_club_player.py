import club_player_service_pb2
import club_player_service_pb2_grpc
from conftest import grpc_stub, generateClubGuid, createPlayer, createPlayersInClub
from functions import generate_guid


def test_create_club_player_with_role_none(grpc_channel):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = generate_guid()
    club_guid = generate_guid()
    request = club_player_service_pb2.CreateClubPlayerRequest(
        player=club_player_service_pb2.ClubPlayerRequest(
            player_guid=player_guid,
            club_guid=club_guid
        ),
        player_club_role=0
    )

    try:
        response = stub.CreateClubPlayer(request)
    except Exception as e:
        print(e)
        return 1

    assert response.player_guid == player_guid
    assert response.club_guid == club_guid
    assert response.player_club_role == 0
    assert len(response.guid) == 36
    assert response.allow_play == False
    assert len(response.description) == 0
    assert len(response.tags_guids) == 0


def test_create_club_player_with_role_player(grpc_channel):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = generate_guid()
    club_guid = generate_guid()
    request = club_player_service_pb2.CreateClubPlayerRequest(
        player=club_player_service_pb2.ClubPlayerRequest(
            player_guid=player_guid,
            club_guid=club_guid
        ),
        player_club_role="PLAYER"
    )

    try:
        response = stub.CreateClubPlayer(request)
    except Exception as e:
        print(e)
        return 1

    assert response.player_guid == player_guid
    assert response.club_guid == club_guid
    assert response.player_club_role == 1
    assert len(response.guid) == 36
    assert response.allow_play == False
    assert len(response.description) == 0
    assert len(response.tags_guids) == 0


def test_create_club_player_with_role_manager(grpc_channel):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = generate_guid()
    club_guid = generate_guid()
    request = club_player_service_pb2.CreateClubPlayerRequest(
        player=club_player_service_pb2.ClubPlayerRequest(
            player_guid=player_guid,
            club_guid=club_guid
        ),
        player_club_role=2
    )

    try:
        response = stub.CreateClubPlayer(request)
    except Exception as e:
        print(e)
        return 1

    assert response.player_guid == player_guid
    assert response.club_guid == club_guid
    assert response.player_club_role == 2
    assert len(response.guid) == 36
    assert response.allow_play == False
    assert len(response.description) == 0
    assert len(response.tags_guids) == 0


def test_create_club_player_with_role_owner(grpc_channel):

    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = generate_guid()
    club_guid = generate_guid()
    request = club_player_service_pb2.CreateClubPlayerRequest(
        player=club_player_service_pb2.ClubPlayerRequest(
            player_guid=player_guid,
            club_guid=club_guid
        ),
        player_club_role="OWNER"
    )

    try:
        response = stub.CreateClubPlayer(request)
    except Exception as e:
        print(e)
        return 1

    assert response.player_guid == player_guid
    assert response.club_guid == club_guid
    assert response.player_club_role == 3
    assert len(response.guid) == 36
    assert response.allow_play == False
    assert len(response.description) == 0
    assert len(response.tags_guids) == 0


def test_create_many_players_in_club(grpc_channel, createPlayersInClub):
    expected_count = 2
    # Вызов фикстуры создающей несколько игроков в клубе
    created_players = createPlayersInClub[0]
    club_guid = createPlayersInClub[1]

    # Количество игроков в клубе = expected_count
    assert len(created_players) == expected_count

    # club_guid у созданных игроков совпадает
    for player_in_club in created_players:
        assert player_in_club.club_guid == club_guid

    # Создание множества для хранения уникальных guid игроков
    guids = set()
    for i in created_players:
        guids.add(i.guid)

    # guid уникальны
    assert len(guids) == expected_count

    # Создание множества для хранения уникальных player_guid игроков
    player_guids = set()
    for i in created_players:
        player_guids.add(i.player_guid)
    # player_guid игроков в клубе уникальны
    assert len(player_guids) == expected_count


def test_get_clubs_player(grpc_stub,createPlayer):
    created_player_in_club = createPlayer
    club_guid = created_player_in_club.club_guid
    player_guid = created_player_in_club.player_guid
    # Создание запроса на создание нового игрока клуба
    request = club_player_service_pb2.ClubPlayersRequest(
        club_guid=club_guid
    )

    # Отправка запроса на сервер и получение ответа
    response = grpc_stub.GetClubPlayers(request)

    assert response.players[0].player_guid == player_guid
    assert response.players[0].club_guid == club_guid




