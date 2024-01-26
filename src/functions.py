from textwrap import wrap
from time import sleep
from tkinter import filedialog

LINE_SIZE = 96


def _division(number: int = 1) -> None:
    for value in range(number):
        format_print(fill_char='-', line_size=LINE_SIZE, text='')


def format_print(
    fill_char: str = ' ', line_size: int = 116, text: str = ''
) -> None:
    initial_chars = '| '
    final_chars = ' |'

    if text == '':
        initial_chars = '+' + fill_char
        final_chars = fill_char + '+'
        print(initial_chars + text.ljust(line_size, fill_char) + final_chars)
    else:
        for new_text in wrap(text, line_size - 4):
            print(
                initial_chars
                + new_text.ljust(line_size, fill_char)
                + final_chars
            )

    if 'initial_chars' in locals():
        del initial_chars

    if 'final_chars' in locals():
        del final_chars

    if 'new_text' in locals():
        del new_text


def header_and_footer(option: bool = False) -> None:
    texts = [
        '>>> PROGBIN AUTOMAÇÃO INDUSTRIAL LTDA <<<',
        'Seja bem-vindo ao programa de teste de comunicação modbus TCP',
    ]

    if option:
        texts.clear()
        texts = [
            'Grato pela utilização. Até logo.',
            'Pressione a tecla "enter" para finalizar...',
        ]

    for number, text in enumerate(texts):
        _division(number=1)
        text = text.center(LINE_SIZE, ' ')
        format_print(fill_char=' ', line_size=LINE_SIZE, text=text)

    _division(number=1)

    if option:
        input()

    if 'number' in locals():
        del number

    if 'text' in locals():
        del text

    if 'texts' in locals():
        del texts


def select_path(p_text: str, p_read_file: bool) -> str:
    format_print(fill_char=' ', line_size=LINE_SIZE, text=p_text)
    path: str = ''
    sleep(1.25)

    while True:
        if p_read_file:
            path = filedialog.askopenfilename()  #
        else:
            path = filedialog.askdirectory()

        if not path:
            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text='Seleção inválida. Por gentileza, tente novamente.',
            )
        else:
            break

    if p_read_file:
        format_print(
            fill_char=' ',
            line_size=LINE_SIZE,
            text=f'Diretório selecionado "{path.replace("/", "\\")}"',
        )

    sleep(0.75)

    return path
