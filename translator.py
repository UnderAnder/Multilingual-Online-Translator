import requests
from time import sleep
from bs4 import BeautifulSoup

URL = 'https://context.reverso.net/translation/'


def main():
    lang = input('Type "en" if you want to translate from French into English,'
                 ' or "fr" if you want to translate from English into French:\n')
    word = input('Type the word you want to translate:\n')
    print(f'You chose "{lang}" as a language to translate "{word}".')
    translate(lang, word)


def translate(lang, word):
    language, req = connect(lang, word)

    soup = BeautifulSoup(req.content, 'lxml')

    translations = [x.text.strip() for x in soup.select("#translations-content > .translation")]
    examples = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]

    print('\n', language, 'Translations:')
    print('\n'.join(x for x in translations[:5]))
    print('\n', language, 'Examples')
    print('\n'.join(f'{x}\n{y}\n' for x, y in zip(examples[:10:2], examples[1:11:2])))


def connect(lang, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    conn, req = False, None
    language = 'French' if lang == 'fr' else 'English'
    translate_direction = "english-french/" if lang == "fr" else "french-english/"
    while not conn:
        req = requests.get(f'{URL}{translate_direction}{word}', headers=headers)
        conn = True if req else False
        sleep(1)
        print(req.status_code, req.reason)
    return language, req


if __name__ == '__main__':
    main()
