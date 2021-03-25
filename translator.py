import requests
from bs4 import BeautifulSoup

URL = 'https://context.reverso.net/translation/'


def main():
    lang = input('Type "en" if you want to translate from French into English,'
                 ' or "fr" if you want to translate from English into French:\n')
    word = input('Type the word you want to translate:\n')
    print(f'You chose "{lang}" as a language to translate "{word}".')
    translate(lang, word)


def translate(lang, word):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(f'{URL}{"english-french/" if lang == "fr" else "french-english/"}{word}', headers=headers)
    print(req.status_code, 'OK')
    if not req:
        pass
        # retry
    soup = BeautifulSoup(req.content, 'lxml')
    print('Translations')
    translations = []
    for translation in soup.find_all('a', class_='translation'):
        translations.append(translation.text.strip())
    print(translations)
    examples = []
    for example in soup.find_all('div', class_='ltr'):
        examples.append(example.text.strip())
    print(examples)


if __name__ == '__main__':
    main()
