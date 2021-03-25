import requests
from time import sleep
from enum import Enum
from bs4 import BeautifulSoup

URL = 'https://context.reverso.net/translation/'


class Languages(Enum):
    Arabic = 1
    German = 2
    English = 3
    Spanish = 4
    French = 5
    Hebrew = 6
    Japanese = 7
    Dutch = 8
    Polish = 9
    Portuguese = 10
    Romanian = 11
    Russian = 12
    Turkish = 13


def main() -> None:
    print("'Hello, you're welcome to the translator. Translator supports:'")
    print('\n'.join(f'{i}. {x.name}' for i, x in enumerate(Languages)))
    orig_lang = int(input('Type the number of your language:\n'))
    target_lang = int(input('Type the number of language you want to translate to:\n'))
    word = input('Type the word you want to translate:\n')
    translate(orig_lang, target_lang, word)


def translate(orig_lang: int, target_lang: int, word: str) -> None:
    orig_name, target_name = Languages(orig_lang).name, Languages(target_lang).name
    translate_direction = f"{orig_name}-{target_name}/".lower()

    req = connect(translate_direction, word)
    soup = BeautifulSoup(req.content, 'lxml')

    translations = [x.text.strip() for x in soup.select("#translations-content > .translation")]
    examples = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]

    print('\n', target_name, 'Translations:')
    print(*translations[:5], sep='\n')
    print('\n', target_name, 'Examples:')
    print('\n'.join(f'{x}\n{y}\n' for x, y in zip(examples[:10:2], examples[1:11:2])))


def connect(translate_direction: str, word: str) -> requests.Response:
    headers = {'User-Agent': 'Mozilla/5.0'}
    conn, req = False, None

    while not conn:
        req = requests.get(f'{URL}{translate_direction}{word}', headers=headers)
        conn = True if req else False
        sleep(1)
        print(req.status_code, req.reason)
    return req


if __name__ == '__main__':
    main()
