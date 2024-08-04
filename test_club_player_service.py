import club_player_service_pb2
import club_player_service_pb2_grpc
from conftest import grpc_stub, generateClubGuid, createPlayer, createPlayersInClub, delete_club_player
from functions import generate_guid, generateUserDescription


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


def test_delete_club_player(grpc_channel,createPlayersInClub):
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
        print(response)
    except Exception as e:
        print(e)
        return 1

    assert response.value == True


# Получение игроков в клубе после удаления игрока
def test_get_club_players_after_delete(grpc_channel, delete_club_player):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    created_players_in_club = delete_club_player
    clubs_guids = created_players_in_club[0]
    player_guid = created_players_in_club[1]
    request = club_player_service_pb2.ClubPlayersRequest(
        club_guid=clubs_guids[0]
    )

    # Отправка запроса на сервер и получение ответа
    response = stub.GetClubPlayers(request)

    assert len(response.players) == 1


# Получение игрока состоящего в одном клубе
def test_get_player_clubs(grpc_channel, createPlayer):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    created_player = createPlayer
    player_guid = created_player.player_guid
    request = club_player_service_pb2.ClubPlayerRequest(
        player_guid=player_guid
    )

    # Отправка запроса на сервер и получение ответа
    response = stub.GetPlayerClubs(request)
    print(response.player_clubs[0].player_guid)
    for i in range(len(response.player_clubs)):
        assert len(response.player_clubs[i].guid) == 36
        assert len(response.player_clubs[i].player_guid) == 36
        assert len(response.player_clubs[i].club_guid) == 36
        assert response.player_clubs[i].allow_play == False
        assert len(response.player_clubs[i].club_guid) == 36
        assert len(response.player_clubs[i].description) == 0
        assert len(response.player_clubs[i].tags_guids) == 0
        assert response.player_clubs[i].player_club_role != None


def test_create_club_player(grpc_channel,generatePlayerGuid,generateClubGuid):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = generatePlayerGuid
    club_guid = generateClubGuid
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
    assert response.allow_play == False
    assert len(response.description) == 0
    assert len(response.tags_guids) == 0


def test_update_player_allow_play_to_true(grpc_channel,createPlayer):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = createPlayer.player_guid
    club_guid = createPlayer.club_guid
    request = club_player_service_pb2.UpdatePlayerAllowPlayRequest(
        player=club_player_service_pb2.ClubPlayerRequest(
            player_guid=player_guid,
            club_guid=club_guid
        ),
        allow_play=True
    )

    try:
        response = stub.UpdatePlayerAllowPlay(request)
        print(response)
    except Exception as e:
        print(e)
        return 1

    assert response.player_guid == player_guid
    assert response.club_guid == club_guid
    assert response.allow_play == True
    assert len(response.description) == 0
    assert len(response.tags_guids) == 0


def test_update_player_allow_play_to_false(grpc_channel,createPlayer):
    stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(grpc_channel)
    player_guid = createPlayer.player_guid
    club_guid = createPlayer.club_guid
    player_data = {"club_guid": club_guid, "player_guid": player_guid}
    # Запрос меняет allow_play на True
    request_to_true = club_player_service_pb2.UpdatePlayerAllowPlayRequest(
        allow_play=True, player=player_data)
    # Запрос меняет allow_play на False
    request_to_false = club_player_service_pb2.UpdatePlayerAllowPlayRequest(
        allow_play=False, player=player_data)
    try:
        response_to_true = stub.UpdatePlayerAllowPlay(request_to_true)
        response_to_false = stub.UpdatePlayerAllowPlay(request_to_false)
    except Exception as e:
        print(e)
        return 1

    assert response_to_false.player_guid == player_guid
    assert response_to_false.club_guid == club_guid
    assert response_to_false.allow_play == False
    assert len(response_to_false.description) == 0
    assert len(response_to_false.tags_guids) == 0


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


def test_update_player_description(grpc_stub, createPlayer):
    # Выполнение фикстуры создающей player
    createdPlayer = createPlayer
    # Получение player_guid созданного player
    playerGuid = createdPlayer.player_guid
    # Получение club_guid созданного player
    clubGuid = createdPlayer.club_guid
    # Объявление переменной для хранения сгенерированного описания
    descriptionLen = 50
    genDescription = generateUserDescription(descriptionLen)
    # Формирование данных для передачи в запрос
    playerData = {"club_guid": clubGuid, "player_guid": playerGuid}

    # Выполнение запроса
    request = club_player_service_pb2.UpdatePlayerDescriptionRequest(description=genDescription, player=playerData)
    # Получение ответа
    response = grpc_stub.UpdatePlayerDescription(request)
    # Получение описания player из ответа на запрос
    responsePlayerDescription = response.description

    # Тест проверяющий что обновлен тестируемый игрок
    assert response.player_guid == playerGuid
    assert response.club_guid == clubGuid
    # Тест проверяющий что длина описания из ответа равна длине описания из переменной
    assert len(responsePlayerDescription) == descriptionLen
    # Тест проверяющий что описание из ответа совпадает с сгенерированным описанием
    assert response.description == genDescription


# Тест проверяет что в запись более одного уникального тэга возможна
def test_update_player_tags_unique_tags(grpc_stub,createPlayer):
    # Выполнение фикстуры создающей player
    created_player = createPlayer
    # Получение player_guid созданного player
    player_guid = created_player.player_guid
    # Получение club_guid созданного player
    club_guid = created_player.club_guid
    # Объявление списка для хранения tag_guid'ов
    new_tags = []
    # Добавление в список new_tags сгенерированный tag_guid более 1 раза
    for i in range(2):
        new_tags.append(generate_guid())
        i += 1
    print(new_tags)
    # Формирование данных для передачи в запрос
    player_data = {"club_guid": club_guid, "player_guid": player_guid}
    tags_guids = new_tags
    # Выполнение запроса
    request = club_player_service_pb2.UpdatePlayerTagsRequest(player=player_data, tags_guids=tags_guids)
    # Получение ответа
    response = grpc_stub.UpdatePlayerTags(request)
    # Получение количества элементов в tags_guids из ответа на запрос
    tags_count = len(response.tags_guids)
    # Тест проверяющий что обновлен тестируемый игрок
    assert response.player_guid == player_guid
    assert response.club_guid == club_guid
    # Тест проверяющий что в tags_guids не записан дубль и записан только один tag_guid
    assert tags_count == 2
    # Тест проверяющий что в player записаны те tag_guid которые были сгенерированы
    assert sorted(tags_guids) == sorted(response.tags_guids)


# Тест проверяет что запись более одного не уникального тэга возможна
def test_update_player_tags_non_unique_tags(grpc_stub,createPlayer):
    # Выполнение фикстуры создающей player
    createdPlayer = createPlayer
    # Получение player_guid созданного player
    playerGuid = createdPlayer.player_guid
    # Получение club_guid созданного player
    clubGuid = createdPlayer.club_guid
    # Объявление списка для хранения tag_guid'ов
    new_tags = []
    # Генерация одного tag_guid
    new_tag = generate_guid()
    # Добавление в список new_tags сгенерированный tag_guid более 1 раза
    for i in range(0, 2):
        new_tags.append(new_tag)
        i += 1
    # Формирование данных для передачи в запрос
    playerData = {"club_guid": clubGuid, "player_guid": playerGuid}
    tags_guids = new_tags
    # Выполнение запроса
    request = club_player_service_pb2.UpdatePlayerTagsRequest(player=playerData, tags_guids=tags_guids)
    # Получение ответа
    response = grpc_stub.UpdatePlayerTags(request)
    # Получение количества элементов в tags_guids из ответа на запрос
    tagsCount = len(response.tags_guids)
    # Тест проверяющий что обновлен тестируемый игрок
    assert response.player_guid == playerGuid
    assert response.club_guid == clubGuid
    # Тест проверяющий что в tags_guids не записан дубль и записан только один tag_guid
    assert tagsCount == 1