from typing import Optional, List
import numpy as np

def processar_dados(dados: dict[str, str | int | bool]) -> str:
    """
    Processa um dicionário contendo informações de um usuário.

    :param dados: Dicionário com as seguintes chaves obrigatórias:

        - ``nome`` (str): Nome completo do usuário.
        - ``idade`` (int): Idade do usuário em anos.
        - ``ativo`` (bool): Indica se o usuário está ativo.

    :raises KeyError: Se alguma das chaves obrigatórias estiver ausente.
    :return: Uma string formatada com os dados processados.
    """
    nome = dados["nome"]
    idade = dados["idade"]
    ativo = dados["ativo"]

    status = "ativo" if ativo else "inativo"
    return f"{nome}, {idade} anos, status: {status}"


def analisar_dados(dados: list[float | str | dict[str, int | bool]]) -> str:
    """
    Analisa uma lista com estrutura fixa: [float, str, dict].

    :param dados: Lista com exatamente 3 elementos:
        - posição 0 (float): valor numérico.
        - posição 1 (str): descrição textual.
        - posição 2 (dict): dicionário com as chaves 'id' (int) e 'valido' (bool).
    :raises ValueError: Se a estrutura da lista estiver incorreta.
    :return: Texto formatado com o conteúdo processado.

    **Exemplo de uso**::

        >>> dados = [7.5, "Tensão limite", {"id": 101, "valido": True}]
        >>> resultado = analisar_dados(dados)
        >>> print(resultado)
        Tensão limite: 7.50 (ID=101, válido=True)
    """
    if not (isinstance(dados, list) and len(dados) == 3):
        raise ValueError("A lista deve conter exatamente 3 elementos.")
    
    valor, descricao, info = dados
    return f"{descricao}: {valor:.2f} (ID={info.get('id')}, válido={info.get('valido')})"


def calcular_estatisticas(valores: list[float], wander: str) -> tuple[float, float, float]:
    """
    Calcula estatísticas básicas a partir de uma lista de valores numéricos.

    :param valores: Lista de números reais.
    :raises ValueError: Se a lista estiver vazia.
    :return: Uma tupla contendo:

        - média (float)
        - valor mínimo (float)
        - valor máximo (float)
    """
    if not valores:
        raise ValueError("A lista de valores não pode estar vazia.")

    media = sum(valores) / len(valores)
    minimo = min(valores)
    maximo = max(valores)

    return media, minimo, maximo


def griewank(x: List[float], none_variable: Optional[object] = None) -> float:
    """
    The Griewank function has many widespread local minima, which are regularly distributed.

    See the `Griewank function documentation <https://wmpjrufg.github.io/METAPY/BENCH_GRIEWANK.html>`_.

    :param x: List of design variables.
    :param none_variable: Optional variable for compatibility with general-purpose frameworks.

    :return: Objective function value.
    """

    n_dimensions = len(x)
    sum = 0
    prod = 1
    for i in range(n_dimensions):
        x_i = x[i]
        sum += (x_i ** 2) / 4000
    prod *= np.cos(x_i / np.sqrt(i+1))
    of = sum - prod + 1

    return of


