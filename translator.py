def main():
    lang = input('Type "en" if you want to translate from French into English,'
                 ' or "fr" if you want to translate from English into French:\n')
    word = input('Type the word you want to translate:\n')
    print(f'You chose "{lang}" as a language to translate "{word}".')


if __name__ == '__main__':
    main()
