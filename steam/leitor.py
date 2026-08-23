"""
Módulo responsável pelo carregamento e validação dos dados brutos em arquivo CSV.
Garante a integridade do arquivo antes de disponibilizar os registros para o analisador.
"""
import csv
import os
from .excecoes import ArquivoJogosNaoEncontradoError, FormatoInvalidoError, ColunaAusenteError

class LeitorCSV:
    """
    Classe utilitária para leitura, validação de extensão e verificação de esquemas em arquivos CSV.
    """
    def __init__(self, caminho_arquivo: str):
        """
        Recebe o caminho relativo ou absoluto do arquivo a ser lido.
        """
        self.caminho_arquivo = caminho_arquivo

    def ler_dados(self) -> list[dict]:
        """
        Executa as validações de pré-requisitos e carrega os dados em formato de lista de dicionários.
        Lança exceções customizadas em caso de arquivo inexistente, extensão inválida ou colunas ausentes.
        """

        # 1. Valida se o arquivo realmente existe no disco
        if not os.path.exists(self.caminho_arquivo):
            raise ArquivoJogosNaoEncontradoError(f"Arquivo '{self.caminho_arquivo}' não foi encontrado.")

        # 2. Valida o formato/extensão do arquivo fornecido           
        if not self.caminho_arquivo.lower().endswith('.csv'):
            raise FormatoInvalidoError(f"O arquivo '{self.caminho_arquivo}' deve ter a extensão .csv.")

        try:
            # 3. Abre o arquivo com enconding UTF-8 e converte para dicionário
            with open(self.caminho_arquivo, mode='r', encoding='utf-8') as f:
                leitor = csv.DictReader(f)
                dados = list(leitor)

            # Retorna lista vazia caso o CSV esteja completamente em branco    
            if not dados:
                return []
            # 4. Validação do schema: garante que todas as colunas essenciais estão presentes
            colunas_obrigatorias = {'Name', 'Price', 'Release date', 'Windows', 'Mac', 'Linux', 'Positive', 'Negative'}
            colunas_presentes = set(dados[0].keys())

            # Verifica se o conjunto obrigatório está contido no cabeçalho do arquivo
            if not colunas_obrigatorias.issubset(colunas_presentes):
                faltantes = colunas_obrigatorias - colunas_presentes
                raise ColunaAusenteError(f"Colunas obrigatórias ausentes: {faltantes}")

            return dados

        except Exception as e:
            # Propaga exceções de domínio já tratadas para manter a precisão do erro
            if isinstance(e, (ArquivoJogosNaoEncontradoError, FormatoInvalidoError, ColunaAusenteError)):
                raise e
                # Encapsula quaisquer outros erros inesperados (ex: IO/Permissão) na exceção base do pacote
            raise SteamError(f"Erro ao ler arquivo CSV: {e}")
