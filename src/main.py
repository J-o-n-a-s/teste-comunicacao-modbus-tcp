from datetime import UTC, datetime
from time import sleep, time

from pymodbus.client.tcp import Any, Framer, ModbusTcpClient

from default_setting import INFORMATION
from functions import LINE_SIZE, format_print, header_and_footer, select_path


def _config(p_parameter: int, p_use_standard: bool) -> int | str:
    while True:
        _parameter: str = INFORMATION[p_parameter]['parameter']
        _value: int | str = INFORMATION[p_parameter]['standard_value']
        _unidade: str = INFORMATION[p_parameter]['unidade']

        if p_use_standard:
            break

        response = (
            input(
                f'| "{_parameter}" valor padrão "{_value}{_unidade}", modificar [S/N]? '
            )
            .strip()
            .upper()[0]
        )

        if response == 'S':
            new_value = input(
                f'| Informe o novo valor para o parâmetro "{_parameter.lower()}" = '
            )

            if isinstance(_value, int):
                _value = int(new_value)

            break

        elif response == 'N':
            break

    return _value


def _preencher_direita(p_data: str, p_number: int, p_character: str) -> str:
    if len(p_data) < p_number:
        p_data = _preencher_direita(
            p_data=f'{p_data}{p_character}',
            p_number=p_number,
            p_character=p_character,
        )

    return p_data


if __name__ == '__main__':
    # Cabeçalho
    header_and_footer(option=False)

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text='Deseja utilizar uma configuração diferente da padrão? [S/N]?',
    )

    for dado in INFORMATION:
        parameter: str = dado['parameter']
        value: int | str = dado['standard_value']
        unidade: str = dado['unidade']

        format_print(
            fill_char=' ',
            line_size=LINE_SIZE,
            text=f'  -> "{parameter}" valor padrão "{value}{unidade}"',
        )

    while True:
        valor: str = input('| > ').strip().upper()[0]

        if valor in 'SN':
            use_standard = valor == 'N'
            format_print(fill_char='-', line_size=LINE_SIZE, text='')
            break

        else:
            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text='Opção inválida. Selecione uma opção válida.',
            )

    device_address: str = str(
        _config(p_parameter=0, p_use_standard=use_standard)
    )
    port: int = int(_config(p_parameter=1, p_use_standard=use_standard))
    timeout = _config(p_parameter=2, p_use_standard=use_standard)
    retry = _config(p_parameter=3, p_use_standard=use_standard)
    slave: int = int(_config(p_parameter=4, p_use_standard=use_standard))
    start_address: int = int(
        _config(p_parameter=5, p_use_standard=use_standard)
    )
    count: int = int(_config(p_parameter=6, p_use_standard=use_standard))
    numero_leituras: int = int(
        _config(p_parameter=7, p_use_standard=use_standard)
    )

    acquisition_time: float = (
        float(_config(p_parameter=8, p_use_standard=use_standard)) / 1000.0
    )

    if valor == 'S':
        format_print(fill_char='-', line_size=LINE_SIZE, text='')

    while True:
        valor = (
            input('| Deseja salvar os dados no arquivo de log? [S/N] ')
            .strip()
            .upper()[0]
        )

        if valor in 'SN':
            log: bool = valor == 'S'
            break

        else:
            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text='Opção inválida. Selecione uma opção válida.',
            )

    filename: str = ''

    if log:
        filename = (
            select_path(
                p_text='Por gentileza, selecione o caminho '
                'para exportação do arquivo "log_AAAA-MM-DD_HH-MM.csv".',
                p_read_file=False,
            )
            + '\\'
            + 'log.csv'
        )

    format_print(fill_char='-', line_size=LINE_SIZE, text='')

    sleep(0.5)

    # Connect to the Modbus TCP/IP device
    client = ModbusTcpClient(
        host=device_address,
        port=port,
        framer=Framer.SOCKET,
        timeout=timeout,
        retries=retry,
        retry_on_empty=True,
        close_comm_on_error=False,
        strict=True,
        # source_address=("localhost", 0),
    )

    client.connect()

    format_print(
        fill_char=' ', line_size=LINE_SIZE, text='Iniciando leitura...'
    )

    sleep(0.5)

    text: str = 'Communication;Time (s);Observation'
    for j in range(count):
        text += f';R{start_address + j}'

    export_data: list = [text + '\n']

    i = 0
    leitura_ok = 0
    menor: float = 0.0
    maior: float = 0.0
    atual: float = 0.0
    registers: Any = None
    inicio: float = 0.0

    inicio_geral: float = time()

    while i < numero_leituras:
        try:
            inicio = time()
            registers = client.read_holding_registers(
                start_address, count, slave
            )

        except Exception as error:
            print(f'Ocorreu o erro {error}')

        # Process and print the retrieved data
        atual = float(f'{(time() - inicio):.3f}')

        _split: list = str(atual).split('.')
        _split[1] = _preencher_direita(
            p_data=_split[1], p_number=3, p_character='0'
        )
        _atual: str = f'{_split[0]},{_split[1]}'

        if i == 0:
            menor = atual
            maior = atual

        if registers.isError():
            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text=f' Leitura modbus {i + 1} falha (resposta em {_atual} s)',
            )

            if log:
                export_data.append(
                    f'Falha na leitura;{_atual};{registers.message}\n'
                )

        else:
            data = registers.registers
            leitura_ok += 1

            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text=f' Leitura modbus {i + 1} ok (resposta em {_atual} s)',
            )

            text = ''

            for d in data:
                text += f';{d}'

            if log:
                export_data.append(f'Leitura ok;{_atual};{text}\n')

            if atual < menor:
                menor = atual

            if atual > maior:
                maior = atual

        if atual <= acquisition_time:
            sleep(acquisition_time - atual)

        i += 1

    client.close()

    tempo = datetime.fromtimestamp((time() - inicio_geral), UTC).strftime(
        '%H:%M:%S'
    )

    format_print(
        fill_char=' ', line_size=LINE_SIZE, text='...finalizando leitura'
    )

    sleep(1.5)

    format_print(fill_char='-', line_size=LINE_SIZE, text='')

    format_print(
        fill_char=' ', line_size=LINE_SIZE, text=f' > Total de leituras = {i};'
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=(
            f' > Leituras corretas = '
            f'{leitura_ok} ({leitura_ok / i * 100:.2f} %);'.replace('.', ',')
        ),
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=(
            f' > Falhas de leitura = '
            f'{i - leitura_ok} ({(i - leitura_ok) / i * 100:.2f} %).'.replace(
                '.', ','
            )
        ),
    )

    _split = str(menor).split('.')
    _split[1] = _preencher_direita(
        p_data=_split[1], p_number=3, p_character='0'
    )
    _menor: str = f'{_split[0]},{_split[1]}'

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f' > Menor tempo de leitura {_menor} s.',
    )

    _split = str(maior).split('.')
    _split[1] = _preencher_direita(
        p_data=_split[1], p_number=3, p_character='0'
    )
    _maior: str = f'{_split[0]},{_split[1]}'

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f' > Maior tempo de leitura {_maior} s.',
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f' > Tempo total de execução = {tempo}.',
    )

    if log:
        _split = filename.split('.')
        filename = (
            _split[0] + datetime.now().strftime('_%Y-%m-%d_%H-%M.') + _split[1]
        )

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(''.join(export_data))

        format_print(fill_char='-', line_size=LINE_SIZE, text='')

        format_print(
            fill_char=' ',
            line_size=LINE_SIZE,
            text=f'Arquivo exportado em {filename.replace("/", "\\")}.',
        )

    # Rodapé
    header_and_footer(option=True)
