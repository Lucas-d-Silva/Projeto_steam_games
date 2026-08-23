"""
Módulo de exceções customizadas para a biblioteca 'steam'.
Define uma hierarquia de erros para facilitar o tratamento e diagnóstico no leitor e analisador.
"""
class SteamError(Exception):
    """
    Exceção base para todas as falhas relacionadas ao pacote 'steam'.
    Permite capturar qualquer erro genérico do módulo com um único 'except SteamError'.
    """
    pass

class ArquivoJogosNaoEncontradoError(SteamError):
    """
    Lançada quando o caminho especificado para o arquivo CSV de jogos não existe no sistema de arquivos.
    """
    pass

class FormatoInvalidoError(SteamError):
    """
    Lançada quando o arquivo fornecido não possui a extensão ou estrutura esperada (ex: extensão diferente de .csv).
    """
    pass

class ColunaAusenteError(SteamError):

    """
    Lançada durante a validação do cabeçalho do CSV quando alguma das colunas obrigatórias está ausente.
    """
    pass
