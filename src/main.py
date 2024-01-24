import datetime

from functions import format_print, header_and_footer, LINE_SIZE, select_path
from pymodbus.client.tcp import *
from time import sleep

INFORMATION: tuple = (
    {
        'parameter': 'Endereço IP',
        'standard_value': '192.168.1.1',
        'unidade': '',
    },
    {'parameter': 'Porta', 'standard_value': 502, 'unidade': ''},
    {'parameter': 'Timeout', 'standard_value': 2, 'unidade': ' s'},
    {'parameter': 'Tentativas', 'standard_value': 1, 'unidade': ' vez(es)'},
    {'parameter': 'Número do escravo', 'standard_value': 1, 'unidade': ''},
    {'parameter': 'Registro', 'standard_value': 400, 'unidade': ''},
    {
        'parameter': 'Quantidade de registros sequênciais',
        'standard_value': 20,
        'unidade': '',
    },
    {'parameter': 'Número de leituras', 'standard_value': 31, 'unidade': ''},
    {
        'parameter': 'Tempo entre leituras',
        'standard_value': 500,
        'unidade': 'ms',
    },
)


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


if __name__ == '__main__':
    # Cabeçalho
    header_and_footer(option=False)

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text='Deseja utilizar uma configuração diferente da padrão? [S/N]?'
    )

    for dado in INFORMATION:
        parameter: str = dado['parameter']
        value: int | str = dado['standard_value']
        unidade: str = dado['unidade']

        format_print(
            fill_char=' ',
            line_size=LINE_SIZE,
            text=f'  -> "{parameter}" valor padrão "{value}{unidade}"'
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
                text='Opção inválida. Selecione uma opção válida.'
            )

    device_address: str = str(_config(p_parameter=0, p_use_standard=use_standard))
    port: int = int(_config(p_parameter=1, p_use_standard=use_standard))
    timeout = _config(p_parameter=2, p_use_standard=use_standard)
    retry = _config(p_parameter=3, p_use_standard=use_standard)
    slave: int = int(_config(p_parameter=4, p_use_standard=use_standard))
    start_address: int = int(_config(p_parameter=5, p_use_standard=use_standard))
    count: int = int(_config(p_parameter=6, p_use_standard=use_standard))
    numero_leituras: int = int(_config(p_parameter=7, p_use_standard=use_standard))

    acquisition_time: float = (
        float(_config(p_parameter=8, p_use_standard=use_standard)) / 1000.0
    )

    format_print(fill_char='-', line_size=LINE_SIZE, text='')

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
        fill_char=' ',
        line_size=LINE_SIZE,
        text='Iniciando leitura...'
    )

    sleep(1)

    text: str = 'Communication;Time (s);Observation'
    for j in range(count):
        text += f';R{start_address + j}'

    text += '\n'

    export_data: list = [text]
    i = 0
    leitura_ok = 0
    menor: float = 0.0
    maior: float = 0.0
    atual: float = 0.0
    registers: Any = None
    inicio: float = 0.0
    inicio_geral: float = time.time()

    while i < numero_leituras:
        try:
            inicio = time.time()
            registers = client.read_holding_registers(start_address, count, slave)

        except Exception as error:
            print(f'Ocorreu o erro {error}')

        # Process and print the retrieved data
        atual = float(f'{(time.time() - inicio):.3f}')

        if i == 0:
            menor = atual
            maior = atual

        if registers.isError():
            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text=f'Leitura modbus {i + 1} falha (resposta em {atual} s)'
            )

            export_data.append(f'Falha na leitura;{atual};{registers.message}\n')

        else:
            data = registers.registers
            leitura_ok += 1

            format_print(
                fill_char=' ',
                line_size=LINE_SIZE,
                text=f'Leitura modbus {i + 1} ok (resposta em {atual} s)'
            )

            text: str = ''
            for d in data:
                text += f';{d}'

            export_data.append(f'Leitura ok;{atual}s;{text}\n')

            if atual < menor:
                menor = atual

            if atual > maior:
                maior = atual

        time.sleep(acquisition_time)
        i += 1

    client.close()

    tempo = datetime.datetime.fromtimestamp(
        (time.time() - inicio_geral), datetime.UTC
    ).strftime('%H:%M:%S')

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text='...finalizando leitura'
    )

    sleep(1.5)

    format_print(
        fill_char='-',
        line_size=LINE_SIZE,
        text=''
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f' > Total de leituras = {i};'
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f' > Leituras corretas = {leitura_ok} ({leitura_ok / i * 100:.2f} %);'
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=(
            f' > Falhas de leitura = {i - leitura_ok} ({(i - leitura_ok) / i * 100:.2f} %).'
        )
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=(
            f' > Menor tempo de leitura {menor} s.'
        )
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=(
            f' > Maior tempo de leitura {maior} s.'
        )
    )

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f' > Tempo total de execução = {tempo} s.'
    )

    filename = (
            select_path(
                p_text='Por gentileza, selecione o caminho '
                       'para exportação do arquivo "log.csv".',
                p_read_file=False,
            )
            + '\\'
            + "log.csv"
    )

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(''.join(export_data))

    format_print(
        fill_char=' ',
        line_size=LINE_SIZE,
        text=f'Arquivo exportado em {filename.replace("/", "\\")}.',
    )

    # Rodapé
    header_and_footer(option=True)
