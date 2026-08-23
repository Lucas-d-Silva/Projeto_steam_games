"""
Módulo responsável pelo processamento de dados e regras de negócio da Steam.
Realiza cálculos estatísticos referentes a precificação, datas de lançamento e engajamento.
"""
from datetime import datetime
from .leitor import LeitorCSV

class Analisador:
    """
    Classe principal para análise dos dados da plataforma Steam.
    """
    def __init__(self, caminho_arquivo: str):
        """
        Inicializa o analisador delegando a leitura do CSV ao LeitorCSV.
        """
        leitor = LeitorCSV(caminho_arquivo)
        self.dados = leitor.ler_dados()

    def calcular_percentual_gratuitos_e_pagos(self) -> dict:
        """
        Pergunta 1: Calcula a proporção entre jogos gratuitos (Preço == 0) e pagos.
        Retorna um dicionário com os percentuais arredondados em 2 casas decimais.
        """
        total = len(self.dados)
        if total == 0:
            return {"gratuitos": 0.0, "pagos": 0.0}

        gratuitos = 0
        for jogo in self.dados:
            try:
                # Converte o valor do preço para float e verifica se é zero
                preco = float(jogo.get("Price", 0))
                if preco == 0.0:
                    gratuitos += 1
            except (ValueError, TypeError):
                # Caso haja dado inconsistente ou incorrompido, ignora a linha sem quebrar o fluxo
                continue
        # Cálculo das porcentagens relativas ao total de registros
        perc_gratuitos = round((gratuitos / total) * 100, 2)
        perc_pagos = round(100.0 - perc_gratuitos, 2)

        return {"gratuitos": perc_gratuitos, "pagos": perc_pagos}

    def obter_ano_com_mais_lancamentos(self) -> list[int]:
        """
        Pergunta 2: Identifica o(s) ano(s) com o maior volume de lançamentos na plataforma.
        Trata múltiplos formatos de datas e lida com eventuais empates, retornando uma lista ordenada.
        """
        contagem_anos = {}

        for jogo in self.dados:
            data_str = jogo.get("Release date", "").strip()
            if not data_str:
                continue

            ano = None
            # Tenta fazer o parse da string de data usando diferentes padrões suportados
            for fmt in ("%b %d, %Y", "%b %Y", "%Y"):
                try:
                    ano = datetime.strptime(data_str, fmt).year
                    break # Para no primeiro formato correspondente
                except ValueError:
                    pass
            # Acumula a frequência do ano no dicionário de contagem
            if ano:
                contagem_anos[ano] = contagem_anos.get(ano, 0) + 1

        if not contagem_anos:
            return []
        # Descobre a quantidade máxima de lançamentos e filtra os anos que atingiram essa marca (trata empates)
        max_lancamentos = max(contagem_anos.values())
        anos_mais_lancamentos = [
            ano for ano, count in contagem_anos.items() if count == max_lancamentos
        ]

        return sorted(anos_mais_lancamentos)

    def comparar_engajamento_por_suporte_plataformas(self) -> dict:
        """
        Pergunta 3: Compara a taxa de aprovação média (% de avaliações positivas)
        entre jogos que suportam até 2 sistemas operacionais vs. jogos com suporte total (3 sistemas: Win, Mac, Linux).
        """
        taxas_ate_2 = []
        taxas_3 = []

        for jogo in self.dados:
            # Converte as colunas de suporte para booleano tratável
            win = str(jogo.get("Windows", "False")).strip().lower() in ["true", "1"]
            mac = str(jogo.get("Mac", "False")).strip().lower() in ["true", "1"]
            lin = str(jogo.get("Linux", "False")).strip().lower() in ["true", "1"]
            # Soma a quantidade de plataformas suportadas (0 a 3)
            qtd_sistemas = sum([win, mac, lin])

            try:
                pos = float(jogo.get("Positive", 0))
                neg = float(jogo.get("Negative", 0))
            except (ValueError, TypeError):
                continue

            total_votos = pos + neg
            # Evita divisão por zero para jogos sem nenhuma avaliação cadastrada
            if total_votos == 0:
                continue
            # Calcula a taxa individual de aprovação do jogo em porcentagem
            taxa = (pos / total_votos) * 100
            # Agrupa os resultados conforme a quantidade de sistemas operacionais suportados
            if qtd_sistemas <= 2:
                taxas_ate_2.append(taxa)
            elif qtd_sistemas == 3:
                taxas_3.append(taxa)
        # Calcula a média aritmética de aprovação para cada grupo
        med_2 = sum(taxas_ate_2) / len(taxas_ate_2) if taxas_ate_2 else 0.0
        med_3 = sum(taxas_3) / len(taxas_3) if taxas_3 else 0.0

        dif = round(med_3 - med_2, 2)

        return {
            "total_ate_2_sistemas": len(taxas_ate_2),
            "taxa_aprovacao_ate_2": round(med_2, 2),
            "total_3_sistemas": len(taxas_3),
            "taxa_aprovacao_todos_3": round(med_3, 2),
            "diferenca_pontos_percentuais": dif
        }

