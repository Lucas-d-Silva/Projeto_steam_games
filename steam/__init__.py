"""
Módulo de inicialização do pacote 'steam'.
Este arquivo expõe as principais classes e exceções customizadas para simplificar
as importações externas (interface pública do pacote).
"""

#Importa a classe responsável pelo carregamento e validação dos dados em CSV
from .leitor import LeitorCSV
#Importa a hierarquia de exceções customizadas para tratamento de erros
from .excecoes import (
    SteamError,
    ArquivoJogosNaoEncontradoError,
    FormatoInvalidoError,
    ColunaAusenteError
)
# Importa a classe responsável pelas regras de negócio e análises estatísticas
from .analisador import Analisador
#Define explicitamente quais símbolos são exportados quando alguém utiliza 'from steam import *'
__all__ = [
    'LeitorCSV',
    'SteamError',
    'ArquivoJogosNaoEncontradoError',
    'FormatoInvalidoError',
    'ColunaAusenteError',
    'Analisador'
]
