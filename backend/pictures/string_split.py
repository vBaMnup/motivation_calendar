"""todo
- максимальный размер одной строки 45 символов
- разделение по пробелу
"""
import json
from settings.config import HOROSCOPE_IMG_DIR


# def get_key_by_dict(d: dict, value: str) -> str:
#     for k, v in d.items():
#         if v == value:
#             return k
#     return None


def get_key_by_dict(d: dict, value: str) -> str:
    return d.get(value, None)


def get_text_from_json(zodiac_sign: str) -> str:
    with open(f"{HOROSCOPE_IMG_DIR}short_horoscope.json", "r", encoding="utf-8") as f:
        horoscope_data = json.load(f)
    return horoscope_data.get(zodiac_sign, {}).get("horo", "Гороскоп не найден")


def make_strings_from_text(text: str) -> list:
    strings: list[str] = []
    while text:
        if len(text) > 45:
            index = text[:45].rfind(" ")
            if index != -1:
                strings.append(text[:index])
                text = text[index + 1 :]
            else:
                strings.append(text[:45])
                text = text[:45]
        else:
            strings.append(text)
            break
    return strings


if __name__ == "__main__":
    # text: str = (
    #     'Ох, уж, эти Водолеи. Весь месяц в кураже и внимании. Как же не '
    #     'упустить из виду нечто действительно важное, например, здоровье?')
    text = get_text_from_json("Овен")
    print(make_strings_from_text(text))
