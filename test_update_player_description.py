import grpc
import pytest
import club_player_service_pb2
import club_player_service_pb2_grpc
from functions import generate_guid, generateUserDescription
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
