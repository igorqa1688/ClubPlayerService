import club_player_service_pb2
from functions import generate_guid
from conftest import grpc_stub, createPlayer


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


# Тест проверяет что в запись более одного не уникального тэга возможна
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
