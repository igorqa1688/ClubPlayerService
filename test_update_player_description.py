from functions import generateUserDescription
import club_player_service_pb2
from conftest import grpc_stub, createPlayer


def test_update_player_tags(grpc_stub, createPlayer):
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
