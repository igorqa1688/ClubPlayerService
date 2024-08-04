import uuid
import random
import string

# Генерация GUID
def generate_guid():
    return str(uuid.uuid4())


# Генерация случайного описания player
def generateUserDescription(length):
    # Создаем списки разных типов символов
    lower_chars = string.ascii_lowercase
    upper_chars = string.ascii_uppercase
    cyrillic_chars = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    digits = string.digits
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
    else:
        random_role = user_roles[random_index]
    return random_role