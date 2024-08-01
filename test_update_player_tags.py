import grpc
import pytest
import club_player_service_pb2
import club_player_service_pb2_grpc
from functions import generate_guid
from global_vars import server


@pytest.fixture(scope="module")
def grpc_channel():
    """Создание gRPC-канала для подключения к серверу"""
    with grpc.insecure_channel(server) as channel:
        yield channel


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    """Создание gRPC-клиентского стаба"""
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


@pytest.fixture(scope="session")
def createPlayer():
    clubGuid = generate_guid()
    playerGuid = generate_guid()
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
        return  response


def test_update_player_tags(grpc_stub,createPlayer):
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
