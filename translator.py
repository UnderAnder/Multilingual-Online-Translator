from enum import Enum
from sys import argv

import requests
from bs4 import BeautifulSoup

URL = 'https://context.reverso.net/translation/'
SESSION = requests.Session()


class Languages(Enum):
    All = 0
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
    if len(argv) == 4:
        orig_lang, target_lang, word = argv[1:]
        try:
            orig_lang, target_lang = Languages[orig_lang.capitalize()], Languages[target_lang.capitalize()]
        except KeyError:
            print("Sorry, the program doesn't support", target_lang)
            exit()
    elif len(argv) == 1:
        print("Hello, you're welcome to the translator. Translator supports:")
        print('\n'.join(f'{i}. {x.name}' for i, x in enumerate(Languages)))
        orig_lang = int(input('Type the number of your language:\n'))
        target_lang = int(input('Type the number of a language you want to translate to or "0" to translate to all languages:\n'))
        word = input('Type the word you want to translate:\n')
    else:
        print('Error: wrong arguments number')
        exit()
        
    start(orig_lang, target_lang, word)
    with open(f'{word}.txt', 'r', encoding='utf-8') as f:
        print(f.read())


def start(orig_lang: int, target_lang: int, word: str) -> None:
    orig_name = Languages(orig_lang).name
    target_name = Languages(target_lang).name
    if target_name == 'All':
        for target in Languages:
            if target.name == 'All' or target.name == orig_name:
                continue
            translate(orig_name, target.name, word, 1)
    else:
        translate(orig_name, target_name, word, 1)


def translate(orig_name: str, target_name: str, word: str, result_num: int) -> None:
    translate_direction = f"{orig_name}-{target_name}/".lower()
    req = connect(translate_direction, word)
    soup = BeautifulSoup(req.content, 'lxml')
    translations = [x.text.strip() for x in soup.select("#translations-content > .translation")]
    examples = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]
    translate_header = f"{target_name} Translations:"
    example_header = f"{target_name} Examples:"
    translate_result = translations[:result_num]
    example_result = '\n'.join(f'{x}\n{y}\n' for x, y in zip(examples[:result_num * 2:2], examples[1:result_num * 2:2]))

    with open(f'{word}.txt', 'a', encoding='utf-8') as f:
        print(translate_header, file=f)
        print(*translate_result, '\n', file=f)
        print(example_header, file=f)
        print(example_result, file=f)


def connect(translate_direction: str, word: str) -> requests.Response:
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = SESSION.get(f'{URL}{translate_direction}{word}', headers=headers)

    if req.status_code == 404:
        print(f'Sorry, unable to find {word}')
        exit()
    if not req:
        print('Something wrong with your internet connection')
        exit()

    return req


if __name__ == '__main__':
    main()
