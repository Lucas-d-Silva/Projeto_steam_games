"""
Script de testes automatizados para validação do sistema 'steam'.
Verifica a acurácia dos cálculos com base na amostra de controle e atesta o disparo correto de exceções.
"""
import os
from steam import Analisador, ArquivoJogosNaoEncontradoError

def rodar_testes():
    """
    Executa a suíte de testes do sistema e compara os resultados com os gabaritos esperados.
    """
    print("=== INICIANDO TESTES DO SISTEMA STEAM (AMOSTRA DE 20 JOGOS) ===")
    
    # 1. Validação de pré-requisito: verifica existência da amostra no ambiente
    caminho_amostra = "amostra_20.csv"
    if not os.path.exists(caminho_amostra):
        print(f"❌ Erro: Arquivo '{caminho_amostra}' não encontrado. Faça o upload do CSV.")
        return

    # 2. Teste de Instanciação e Carregamento de Dados
    analisador = Analisador(caminho_amostra)
    assert len(analisador.dados) == 20, f"Esperado 20 jogos, mas carregou {len(analisador.dados)}"
    print(f"\n[1] Carregamento: SUCESSO ({len(analisador.dados)} jogos)")
    
    # Definção dos valores esperados (Gabarito Oficial para a amostra de 20 registros)
    GABARITO_P1 = {"gratuitos": 5.0, "pagos": 95.0}
    GABARITO_P2 =  [2018]
    GABARITO_P3_DIF = 18.28
  
    # 3. Teste da Pergunta 1: Percentual de jogos gratuitos e pagos
    p1 = analisador.calcular_percentual_gratuitos_e_pagos()
    assert p1 == GABARITO_P1, f"❌ Falha P1: Calculado {p1} difere de {GABARITO_P1}"
    print(f"[2] Pergunta 1: APROVADO ✅ ({p1})")
    
    # 4. Teste da Pergunta 2: Ano com mais lançamentos
    p2 = sorted(analisador.obter_ano_com_mais_lancamentos())
    assert p2 == GABARITO_P2, f"❌ Falha P2: Calculado {p2} difere de {GABARITO_P2}"
    print(f"[3] Pergunta 2: APROVADO ✅ (Anos: {p2})")
    
    # 5. Teste da Pergunta 3: Comparativo de engajamento por suporte a plataformas
    p3 = analisador.comparar_engajamento_por_suporte_plataformas()
    dif = p3.get("diferenca_pontos_percentuais")
    assert dif == GABARITO_P3_DIF, f"❌ Falha P3: Calculado {dif} difere de {GABARITO_P3_DIF}"
    print(f"[4] Pergunta 3: APROVADO ✅ (Diferença: {dif} p.p.)")
    
    # 6. Teste de Tratamento de Exceções: Garante disparo da exceção correta para arquivo inexistente
    print("\n[5] Teste de Exceção (Arquivo Inexistente):")
    try:
        Analisador("arquivo_inexistente.csv")
        print("❌ Falha: Deveria ter lançado a exceção.")
    except ArquivoJogosNaoEncontradoError as e:
        print(f"    - Sucesso! Exceção capturada corretamente: {e}")

    print("\n🎉 TODOS OS TESTES PASSARAM E FORAM VALIDADOS COM SUCESSO!")
    
# Ponto de entrada do script ao ser executado via terminal ou subprocesso
if __name__ == "__main__":
    rodar_testes()
