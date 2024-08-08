import grpc
import uuid
import random
import club_player_service_pb2
import club_player_service_pb2_grpc
from global_vars import server


# Генерация GUID
def generate_guid():
    return str(uuid.uuid4())


# Генерация случайного описания player
def generateUserDescription(length):
    # Создаем списки разных типов символов
    lower_chars = 'abcdefghijklmnopqrstuvwxyz'
    upper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyrillic_chars = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    digits = '0123456789'
    special_chars = '!@#$%^&*()_+~`|}{[]:;?><,./-='

    # Создаем список всех доступных символов
    all_chars = lower_chars + upper_chars + digits + special_chars + cyrillic_chars

    # Создаем начальные части строки
    result = random.choice(digits)
    result += random.choice(special_chars)
    result += random.choice(lower_chars)
    result += random.choice(upper_chars)
    result += random.choice(cyrillic_chars)

    # Заполняем оставшуюся часть случайными символами
    while len(result) < length:
        result += random.choice(all_chars)

    # Перемешиваем символы
    return ''.join(random.sample(result, len(result)))


def randomPlayerRole():
    user_roles = ["MANAGER", "OWNER", "NONE", "PLAYER"]
    random_index = random.randint(0, len(user_roles) - 1)

    if random_index == len(user_roles):
        random_role = "ROLE INDEX EQUAL ARRAY LENGTH"
        return random_role
    else:
        random_role = user_roles[random_index]
        return random_role


# Создание указанного количество player
def create_players_in_club(players_count):
    club_guid = generate_guid()
    players = []
    with grpc.insecure_channel(server) as channel:
        stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)
        for _ in range(players_count):
            player_guid = generate_guid()
            random_player_club_role = randomPlayerRole()
            request = club_player_service_pb2.CreateClubPlayerRequest(
                player=club_player_service_pb2.ClubPlayerRequest(
                    player_guid=player_guid,
                    club_guid=club_guid
                ),
                player_club_role=random_player_club_role
            )
            response = stub.CreateClubPlayer(request)
            players.append(response)
    return players, club_guid


def create_player_in_different_clubs():
    player_guid = generate_guid()
    players = []
    for _ in range(2):
        club_guid = generate_guid()
        random_player_club_role = randomPlayerRole()
        with grpc.insecure_channel(server) as channel:
            stub = club_player_service_pb2_grpc.ClubPlayerServiceGrpcStub(channel)
            request = club_player_service_pb2.CreateClubPlayerRequest(
                player=club_player_service_pb2.ClubPlayerRequest(
                    player_guid=player_guid,
                    club_guid=club_guid
                ),
                player_club_role=random_player_club_role
            )
            response = stub.CreateClubPlayer(request)
            players.append(response)
            print(players, club_guid)
    return players, club_guid