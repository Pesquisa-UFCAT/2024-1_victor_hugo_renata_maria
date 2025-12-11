"""Objective function"""
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from scipy.interpolate import CubicSpline
from scipy.optimize import bisect
from typing import Any, Dict, List, Tuple, Optional


def f_alpha(beta: float, args: list) -> float:
    """Computes the residual of the normal force equilibrium equation in a rectangular reinforced concrete section, given a value of beta (x/d). Reference: NBR 6118 (2023)

    :param beta: x/d ratio of the section
    :param args: list of parameters [f_ck, f_yk, b_w, d, a_st, e_s, gamma_c, gamma_s]
                 f_ck: characteristic compressive strength of concrete (kPa)
                 f_yk: characteristic tensile strength of steel (kPa)
                 b_w: section width (m)
                 d: effective depth of the section (m)
                 a_st: tensile reinforcement area (m²)
                 e_s: modulus of elasticity of steel (kPa)
                 gamma_c: partial safety factor for concrete
                 gamma_s: partial safety factor for steel

    :return: residual of the normal force equilibrium equation
    """
    f_ck, f_yk, b_w, d, a_st, e_s, gamma_c, gamma_s = args

    # Material and geometric properties
    f_ck /= 1E3
    if f_ck > 50:
        aux1 = (f_ck - 50) / 400
        lambda_c = 0.80 - aux1
        aux2 = (f_ck - 50) / 200
        alpha_c = (1.00 - aux2) * 0.85
        eta_c = (40 / f_ck) ** (1/3)
        epsilon_cu = 2.6 / 1000 + 35 / 1000 * ((90 - f_ck) / 100) ** 4
    else:
        lambda_c = 0.80
        alpha_c = 0.85
        eta_c = 1.00
        epsilon_cu = 3.5 / 1000
    f_ck *= 1E3

    # Concrete stress
    f_cd = f_ck / gamma_c
    sigma_cd = alpha_c * eta_c * f_cd
    x = beta * d

    # Concrete force
    r_cc = sigma_cd * (lambda_c * x * b_w)

    # Limit between domain 2 and 3 and strains
    beta_x_limit = epsilon_cu / (epsilon_cu + 10/1000)

    # Strains
    if beta <= beta_x_limit: 
        # Domain 2
        epsilon_st = 10 / 1000
        epsilon_cc = epsilon_st * beta / (1 - beta)
    else:
        # Domain 3
        epsilon_cc = epsilon_cu
        epsilon_st = epsilon_cc * (1 - beta) / x

    # Steel stress
    f_yd = f_yk / gamma_s
    epsilon_yd = f_yd / e_s
    if np.abs(epsilon_st) <= epsilon_yd:
        sigma_st = e_s * epsilon_st
    else:
        sigma_st = np.sign(epsilon_st) * f_yd

    # Steel force
    r_st = sigma_st * a_st

    return r_cc - r_st


def momento_limite_armadura_simples(a_st: float, b_w: float, h: float, relacao_h_d: float, f_ck: float, f_yk: float, e_s: float, gamma_c: float = 1.00, gamma_s: float = 1.00) -> float:
    """Computing the flexural capacity of a reinforced concrete beam with a rectangular section and simple reinforcement according to NBR 6118 (2023).

    :param a_st: tensile reinforcement area (m²)
    :param b_w: section width (m)
    :param h: total section height (m)
    :param relacao_h_d: d/h ratio of the section
    :param f_ck: characteristic compressive strength of concrete (kPa)
    :param f_yk: characteristic tensile strength of steel (kPa)
    :param e_s: modulus of elasticity of steel (kPa)
    :param gamma_c: partial safety factor for concrete
    :param gamma_s: partial safety factor for steel

    :return: flexural capacity (kN·m)
    """

    # Material and geometric properties
    f_ck /= 1E3
    if f_ck > 50:
        aux1 = (f_ck - 50) / 400
        lambda_c = 0.80 - aux1
        aux2 = (f_ck - 50) / 200
        alpha_c = (1.00 - aux2) * 0.85
        eta_c = (40 / f_ck) ** (1/3)
    else:
        lambda_c = 0.80
        alpha_c = 0.85
        eta_c = 1.00
    f_ck *= 1E3
    d = h * relacao_h_d

    # Encontrar equilíbrio de forças normais
    args = (f_ck, f_yk, b_w, d, a_st, e_s, gamma_c, gamma_s)
    resultado = sc.optimize.root_scalar(lambda beta: f_alpha(beta, args), bracket=(0.00001, d/h), method='bisect')

    # Profundidade da linha neutra
    x = resultado.root * d

    # Momento resistente
    f_cd = f_ck / gamma_c
    sigma_cd = alpha_c * eta_c * f_cd

    # Força no concreto
    r_cc = sigma_cd * (lambda_c * x * b_w)
    m_rd = r_cc * (d - 0.5 * lambda_c * x)

    return m_rd


def corrosion_index(i_corr_20: float, temperature: float) -> float:
    """Determines the corrosion index of steel reinforcements in reinforced concrete considering the influence of ambient temperature on the corrosion rate, according to Peng and Stewart (2016).

    :param i_corr_20: Índice de corrosão a 20°C (μA/cm²)
    :param temperatura: Temperatura do ambiente (°C)

    :return: Índice de corrosão ajustado para a temperatura T (μA/cm²)
    """

    # Correção para temperaturas diferentes de 20°C
    if temperature > 20:
        k = 0.073
    elif temperature < 20:
        k = 0.025
    elif temperature == 20:
        k = 0
    i_corr = i_corr_20 * (1 + k * (temperature - 20))

    return i_corr



def momento_resistente_com_corrosao_azad_algohi(
    d_0: float,
    n_barras: int,
    f_ck: float,
    f_yk: float,
    e_s: float,
    b_w: float,
    h: float,
    relacao_d_h: float,
    i_corr_20: float,
    temperatura: float,
    tempo_decorrido: float,
    tempo_iniciacao: float,
    gamma_c: float,
    gamma_s: float
) -> tuple[float, float, float, float]:
    """
    Determina o momento resistente de uma viga de concreto armado considerando
    os efeitos da corrosão nas armaduras de aço.

    :reference: Al-Gohi, B. H. A. (2008), “Time-dependent modeling of loss of flexural strength of corroding RC beams”.

    :param d_0: Diâmetro original da barra de aço (m)
    :param n_barras: Número de barras de aço na seção
    :param f_ck: Resistência característica do concreto (kPa)
    :param f_yk: Resistência característica do aço (kPa)
    :param e_s: Módulo de elasticidade do aço (kPa)
    :param b_w: Largura da seção transversal da viga (m)
    :param h: Altura total da seção da viga (m)
    :param relacao_d_h: Relação altura útil / altura total da seção (adimensional)
    :param i_corr_20: Índice de corrosão a 20°C (μA/cm²)
    :param temperatura: Temperatura do ambiente (°C)
    :param tempo_decorrido: Tempo decorrido desde a instalação da estrutura (anos)
    :param tempo_iniciacao: Tempo estimado de início da corrosão (anos)
    :param gamma_c: Coeficiente parcial de segurança do concreto (padrão = 1.4)
    :param gamma_s: Coeficiente parcial de segurança do aço (padrão = 1.15)

    :return: Tupla contendo:
        m_rd: Momento resistente da viga (kN·m)
        c_f: Coeficiente de redução da aderência devido à corrosão (adimensional)
        d_corroido: Diâmetro corroido da barra de aço (m)
        i_corr: Índice de corrosão ajustado para a temperatura T (μA/cm²)
    """

    # Índice de corrosão
    tempo_corrosao = tempo_decorrido - tempo_iniciacao
    i_corr = corrosion_index(i_corr_20, temperatura)

    # Perda de seção devido à corrosão
    d_0 *= 1000
    delta_dim = 0.0232 * i_corr * tempo_corrosao
    d_corroido = d_0 - delta_dim
    d_corroido /= 1000

    # Momento resistente com corrosão considerando apenas perda de seção
    a_s_initial = n_barras * (np.pi * (d_corroido ** 2) / 4)
    m_rd = momento_limite_armadura_simples(a_s_initial, b_w, h, relacao_d_h, f_ck, f_yk, e_s)

    # Momento resistente com corrosão considerando perda de seção e redução da aderência
    i_corr /= 1000
    cf_aux = 5 / (d_0 ** 0.54 * (i_corr * tempo_corrosao * 365) ** 0.19)
    if cf_aux > 1.00:
        c_f = 1.00
    else:
        c_f = cf_aux
    m_rd *= c_f

    return m_rd, c_f, d_corroido, i_corr


# def profundidade_carbonatacao_possan(
#     k_c: float, k_fc: float, f_ck: float, t: float, ad: float, k_ad: float,
#     co_2: float, k_co_2: float, ur: float, k_rh: float, k_ce: float
# ) -> float:
#     """
#     Determina a profundidade de carbonatação do concreto de acordo com o modelo
#     de Possan et al. (2016).

#     :param k_c: Fator relacionado ao tipo de cimento (Tabela 3a)
#     :param k_fc: Fator relacionado à resistência à compressão do concreto (Tabela 3a)
#     :param f_ck: resistência característica do concreto (kPa)
#     :param t: idade da estrutura (anos)
#     :param ad: material pozolânico no concreto (% relativo à massa de cimento)
#     :param k_ad: fator relacionado a adições pozolânicas (Tabela 3a)
#     :param co_2: concentração de CO2 atmosférico (%)
#     :param k_co_2: fator relacionado à concentração de CO2 (Tabela 3a)
#     :param ur: umidade relativa média (% * 0.01)
#     :param k_rh: fator relacionado à umidade relativa (Tabela 3a)
#     :param k_ce: fator relacionado à exposição da estrutura (Tabela 3b)

#     :return: profundidade de carbonatação do concreto (m)
#     """

#     # Fator relacionado ao tipo de cimento e à resistência do concreto
#     aux_1 = k_c * (20 / f_ck) ** k_fc  

#     # Fator relacionado à idade da estrutura (considerando t em anos)
#     aux_2 = (t / 20) ** (1 / 2)  

#     # Fatores relacionados às adições pozolânicas (ad) e resistência do concreto
#     aux_31 = (k_ad * ad ** (3 / 2)) / (40 + f_ck)  

#     # Fator relacionado à concentração de CO₂ no ambiente e resistência do concreto
#     aux_32 = (k_co_2 * co_2 ** (1 / 2)) / (60 + f_ck)  

#     # Fator relacionado à umidade relativa e resistência do concreto
#     aux_33 = (k_rh * (ur - 0.58) ** 2) / (100 + f_ck)  

#     # Profundidade de carbonatação do concreto (em mm), ajustando pelos fatores de exposição
#     y_carb = aux_1 * aux_2 * np.exp(aux_31 + aux_32 - aux_33) * k_ce  

#     # Converte profundidade de mm para metros e retorna
#     return y_carb / 1000



# def rcp_co2(ano: int) -> float:
#     """
#     Determina a concentração de dióxido de carbono (CO₂) atmosférico em função do ano, 
#     conforme o modelo de cenário representativo de concentração (RCP).

#     :reference: Intergovernmental Panel on Climate Change (IPCC). 
#                 Climate Change 2013: The Physical Science Basis. 
#                 Cambridge University Press, 2013. (Modelos RCP)
    
#     :param ano: Ano de referência (adimensional)

#     :return: Concentração de CO₂ atmosférico correspondente ao ano indicado (%)
#     """

#     i_aux = ano - 2000
#     co_2_percentual = (0.07278*i_aux**2 + 1.86395*i_aux + 340.93383) / (1E6/1E2)

#     return co_2_percentual



# def tempo_iniciacao_corrosao(
#     k_c: float, k_fc: float, f_ck: float, ad: float, k_ad: float, k_co_2: float,
#     ur: float, k_rh: float, k_ce: float, cob: float, ano_instalacao_estrutura: int = 2000
# ) -> tuple[float, float, float]:
#     """
#     Determina o tempo de iniciação da corrosão das armaduras em função do modelo
#     de Possan et al. (2016).

#     :param k_c: Fator relacionado ao tipo de cimento (Tabela 3a)
#     :param k_fc: Fator relacionado à resistência à compressão do concreto (Tabela 3a)
#     :param f_ck: resistência característica do concreto (kPa)
#     :param ad: material pozolânico no concreto (%)
#     :param k_ad: fator relacionado a adições pozolânicas (Tabela 3a)
#     :param k_co_2: fator relacionado à concentração de CO2 (Tabela 3a)
#     :param ur: umidade relativa média (%)
#     :param k_rh: fator relacionado à umidade relativa (Tabela 3a)
#     :param k_ce: fator relacionado à exposição da estrutura (Tabela 3b)
#     :param cob: cobrimento da armadura (m)
#     :param ano_instalacao_estrutura: ano de instalação da estrutura

#     :return:
#         inicio_corrosao: tempo de iniciação da corrosão (anos)
#         y_carb: profundidade de carbonatação (m)
#         co_2: concentração de CO2 (%)
#     """

#     # Inicializando o ano da estrutura
#     ano = ano_instalacao_estrutura

#     # Procurando o tempo de iniciação para a amostra em questão (máximo da busca = 150 anos)
#     t_max = 150
#     for i in range(0, t_max):
#         # Equação interpoladora RCP 8.5
#         co_2 = rcp_co2(ano)
#         y_carb = profundidade_carbonatacao_possan(k_c, k_fc,  f_ck/1000, i,
#                                                     ad, k_ad, co_2, k_co_2,
#                                                     ur*0.01, k_rh, k_ce)
#         if y_carb >= cob:
#             ti = i
#             break
#         else:
#             ti = t_max
#         ano += 1
        
#     return ti, y_carb, co_2

# def area_aco_flexao_simples(
#     m_sd: float, b_w: float, h: float, f_ck: float, f_ywk: float = 500000,
#     gamma_c: float = 1.4, gamma_s: float = 1.15, impressao: bool = False
# ) -> float:
#     """
#     Calcula a área de aço necessária para resistir aos esforços de flexão em
#     uma viga de concreto armado de acordo com a NBR 6118 (2023).

#     :param m_sd: momento solicitante (kN·m)
#     :param b_w: largura da seção (m)
#     :param h: altura da seção (m)
#     :param f_ck: resistência característica à compressão do concreto (kPa)
#     :param f_ywk: resistência característica à tração do aço (kPa)
#     :param gamma_c: coeficiente parcial de segurança do concreto
#     :param gamma_s: coeficiente parcial de segurança do aço
#     :param impressao: se True, imprime informações intermediárias

#     :return: área de aço necessária (m²)
#     """

#     # Converte f_ck de kPa para MPa para o cálculo intermediário
#     f_ck /= 1E3  

#     # Ajusta os coeficientes lambda e alpha_c de acordo com f_ck
#     if f_ck > 50:
#         # Para concretos de alta resistência, aplica redução nos coeficientes
#         lambdaa = 0.80 - ((f_ck - 50) / 400)  
#         alpha_c = (1.00 - ((f_ck - 50) / 200)) * 0.85  
#     else:
#         # Para f_ck ≤ 50 MPa, coeficientes padrão
#         lambdaa = 0.80
#         alpha_c = 0.85

#     # Altura útil da seção (considerando cobrimento e diâmetro da armadura)
#     d = h * 0.9  

#     # Converte f_ck de volta para kPa para cálculo de tensão de projeto
#     f_ck *= 1E3  

#     # Tensão de cálculo do concreto (considerando coeficiente parcial de segurança)
#     f_cd = f_ck / gamma_c  

#     # Calcula zeta = M_sd / (b * alpha_c * f_cd), usado para determinação da profundidade do eixo neutro
#     zeta = m_sd / (b_w * alpha_c * f_cd)  

#     # Calcula o valor auxiliar para a equação quadrática do eixo neutro
#     aux = d ** 2 - 2 * zeta  

#     # Profundidade do eixo neutro da seção (x)
#     x = (d - np.sqrt(aux)) / lambdaa  

#     # Braço de alavanca efetivo da seção (z)
#     z = d - 0.50 * lambdaa * x  

#     # Tensão de cálculo do aço (considerando coeficiente parcial de segurança)
#     f_yd = f_ywk / gamma_s  

#     # Área de aço necessária para resistir ao momento fletor (m²)
#     a_s = m_sd / (z * f_yd)  

#     # Área total da seção de concreto (m²)
#     a_c = b_w * h  

#     # Taxa de armadura (%) em relação à área da seção de concreto
#     pho_s = a_s / a_c * 100  

#     # Retorna área de aço e taxa de armadura
#     return a_s, pho_s



# # def obj_mestrado_victor(x: List[float], none_variable: Dict[str, Any]) -> Tuple[List[float], List[float], List[float]]:
# #     """
# #     Função objetivo que determina o momento resistente de vigas de concreto armado sujeitas
# #     a uma função de decaimento de resistência ao longo do tempo.

# #     :param x: Lista de variáveis aleatórias e de controle, contendo:
# #         x[0] = M_g: Momento devido ao carregamento permanente (kN·m)
# #         x[1] = M_q: Momento devido ao carregamento acidental (kN·m)
# #         x[2] = f_ck: Resistência característica do concreto (kPa)
# #         x[3] = f_yk: Resistência característica do aço (kPa)
# #         x[4] = e_r: Fator de amplificação do momento resistente (adimensional)
# #         x[5] = e_s: Fator de amplificação da demanda (adimensional)
# #         x[-1] = id_analysis: Índice de passo de tempo para análise de confiabilidade

# #     :param none_variable: Dicionário contendo parâmetros fixos e listas de tempo, com chaves:
# #         'time analysis': lista de tempos (anos)
# #         'dados_viga': dicionário com dados da viga:
# #             - gamma_c: coeficiente parcial de segurança do concreto
# #             - gamma_s: coeficiente parcial de segurança do aço
# #             - gamma_f: coeficiente de combinação de ações
# #             - b_w (m): largura da seção transversal
# #             - h (m): altura da seção
# #             - a_s (m²): área de aço da seção

# #     :return: Tupla de listas:
# #         [m_r * e_r]: Momento resistente amplificado (kN·m)
# #         [m_s * e_s]: Momento solicitante amplificado (kN·m)
# #         [constraint]: Função de estado limite (kN·m)
# #     """
    
# #     # Seleciona o índice do passo de tempo e o valor correspondente
# #     id_analysis = int(x[-1])
# #     time_step = none_variable['time analysis']
# #     t_i = time_step[id_analysis]  # Tempo de análise atual (anos)

# #     # Variáveis aleatórias (momento e propriedades do material)
# #     m_g = x[0]  # Momento devido ao peso permanente (kN·m)
# #     m_q = x[1]  # Momento devido ao carregamento variável (kN·m)
# #     f_ck = x[2]  # Resistência característica do concreto (kPa)
# #     f_yk = x[3]  # Resistência característica do aço (kPa)
# #     e_r = x[4]  # Fator de amplificação do momento resistente (adimensional)
# #     e_s = x[5]  # Fator de amplificação do momento solicitante (adimensional)

# #     # Variáveis fixas da viga
# #     # dados_viga = none_variable['dados_viga']
# #     gamma_c = dados_viga['gamma_c']
# #     gamma_s = dados_viga['gamma_s']
# #     gamma_f = dados_viga['gamma_f']
# #     b_w = dados_viga['b_w (m)']
# #     h = dados_viga['h (m)']
# #     a_s = dados_viga['a_s (m2)']

# #     # Critério de degradação da resistência ao longo do tempo
# #     if t_i == 0:
# #         degrad = 1.0  # Sem degradação no instante inicial
# #     else:
# #         a_d = 1.0
# #         b_d = 0.000055  # Coeficiente de degradação
# #         degrad = a_d * (1 - b_d * t_i ** 2)  # Redução quadrática ao longo do tempo

# #     # Cálculo da capacidade resistente da seção
# #     m_r = momento_resistente_secao_sem_cor(a_s, b_w, h, f_ck, f_yk, gamma_s, gamma_c)
# #     m_r *= degrad  # Aplica degradação temporal

# #     # Cálculo do momento solicitante
# #     m_s = gamma_f * (m_g + m_q)

# #     # Função de estado limite (restrição de segurança)
# #     constraint = e_r * m_r - e_s * m_s

# #     # Retorna momento resistente, momento solicitante e função de estado limite
# #     return [m_r * e_r], [m_s * e_s], [constraint]




# def verifica_tempo_limite(
#     pf_list: List[float],
#     temp_list: List[float],
#     pf_limit: float,
#     plotar: bool = False
# ) -> Optional[float]:
#     """
#     Verifica e determina o tempo em que a estrutura atinge o valor limite de probabilidade de falha (pf).

#     :reference: Adaptado para análise de confiabilidade de estruturas, baseado em metodologia de confiabilidade estrutural.

#     :param pf_list: Lista de valores de probabilidade de falha ao longo do tempo (adimensional)
#     :param temp_list: Lista de tempos correspondentes (anos)
#     :param pf_limit: Valor limite de pf que define a reta horizontal para comparação
#     :param plotar: Se True, exibe o gráfico das curvas de pf ao longo do tempo e a interseção com pf_limit

#     :return: Tempo (anos) em que pf atinge o valor limite. Retorna None se não houver interseção.
#     """

#     # Verificando se os dados estão ordenados por tempo
#     sorted_indices = np.argsort(temp_list)
#     X1 = np.array(temp_list)[sorted_indices]
#     Y1 = np.array(pf_list)[sorted_indices]

#     # Criando a curva da reta horizontal
#     X2 = X1  # Mantemos os mesmos tempos
#     Y2 = np.full_like(X1, pf_limit)  # Criamos um array constante com o valor de pf_limit

#     # Criando interpolação apenas para pf_list
#     f1 = CubicSpline(X1, Y1)

#     # Função para encontrar interseção
#     def diff(x):
#         return f1(x) - pf_limit

#     # Definição do intervalo de busca
#     x_min, x_max = X1[0], X1[-1]
#     x_values = np.linspace(x_min, x_max, 1000)

#     x_cross, y_cross = None, None
#     for i in range(len(x_values) - 1):
#         if diff(x_values[i]) * diff(x_values[i+1]) < 0:
#             x_cross = bisect(diff, x_values[i], x_values[i+1])
#             y_cross = f1(x_cross)
#             # print(f"As curvas se cruzam em X = {x_cross:.2f}, Y = {y_cross:.2f}")
#             # print(f"Tempo limite = {x_cross:.2f}")
#             break

#     # Plotando o gráfico
#     if plotar:
#         plt.figure(figsize=(8, 6))
#         plt.plot(X1, Y1, label="Curva pf", color='blue')
#         plt.axhline(y=pf_limit, color='red', linestyle="--", label="pf Limite")  # Linha reta horizontal

#         plt.scatter(X1, Y1, color='blue', marker='o', label="Pontos Curva pf")

#         if x_cross is not None and y_cross is not None:
#             plt.scatter(x_cross, y_cross, color='black', marker='x', s=100, label="Interseção")
#             plt.text(x_cross, y_cross, f"({x_cross:.2f}, {y_cross:.2f})", fontsize=12, verticalalignment='bottom')

#         plt.xlabel("Ano")
#         plt.ylabel("pf")
#         plt.title("Interseção das Curvas")
#         plt.legend()
#         plt.grid(True)
#         plt.show()

#     return x_cross



# if __name__ == "__main__":
#     resultado = momento_limite_armadura_simples(
#         a_st=0.00016,
#         b_w=0.14,
#         h=0.30,
#         relacao_h_d=0.9,
#         f_ck=20000,
#         f_yk=500000,
#         e_s=200000000,
#         gamma_c=1.00,
#         gamma_s=1.00
#     )
#     print(f"Momento resistente: {resultado:.2f} kN·m")

# if __name__ == "__main__":
#     resultado =  momento_resistente_com_corrosao_azad_algohi(
#         d_0 = 0.0125,
#         n_barras = 1.3038,
#         f_ck = 20000,
#         f_yk = 500000,
#         e_s = 200000000,
#         b_w = 0.14,
#         h = 0.30,
#         relacao_d_h = 0.9,
#         i_corr_20 = 0.431,
#         temperatura = 29.29,
#         tempo_decorrido = 40,
#         tempo_iniciacao = 20,
#         gamma_c = 1.0,
#         gamma_s = 1.0
#     )
    