"""Objective function"""
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from scipy.interpolate import CubicSpline
from scipy.optimize import bisect


def f_alpha(beta, args):
    """
    Função que calcula o resíduo da equação de equilíbrio de forças normais em uma seção retangular de concreto armado, dado um valor de beta (x/d).

    :param beta: relação x/d da seção
    :param args: contém os parâmetros de simulação. [0] = f_ck - resistência característica à compressão do concreto (kPa), [1] = f_yk - resistência característica à tração do aço (kPa), [2] = b_w - largura da seção (m), [3] = d - altura útil (m), [4] = a_st - área de aço tracionado (m2), [5] = e_s - módulo de elasticidade do aço (kPa), [6] = gamma_c - coeficiente parcial de segurança do concreto, [7] = gamma_s - coeficiente parcial de segurança do aço

    :return: resíduo da equação de equilíbrio de forças normais
    """
    
    f_ck, f_yk, b_w, d, a_st, e_s, gamma_c, gamma_s = args

    # Propriedades dos materiais e da geometria
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

    # Tensão no concreto
    f_cd = f_ck / gamma_c
    sigma_cd = alpha_c * eta_c * f_cd
    x = beta * d

    # Força no concreto
    r_cc = sigma_cd * (lambda_c * x * b_w)

    # Limite domínio 2 com o 3 e deformações
    beta_x_limit = epsilon_cu / (epsilon_cu + 10/1000)

    # Deformações
    if beta <= beta_x_limit: 
        # Domínio 2
        epsilon_st = 10 / 1000
        epsilon_cc = epsilon_st * beta / (1 - beta)
    else:
        # Domínio 3
        epsilon_cc = epsilon_cu
        epsilon_st = epsilon_cc * (1 - beta) / x

    # Tensão no aço
    f_yd = f_yk / gamma_s
    epsilon_yd = f_yd / e_s
    if np.abs(epsilon_st) <= epsilon_yd:
        sigma_st = e_s * epsilon_st
    else:
        sigma_st = np.sign(epsilon_st) * f_yd

    # Força no aço
    r_st = sigma_st * a_st

    return r_cc - r_st


def momento_limite_armadura_simples(a_st: float, b_w: float, h: float, relacao_h_d: float, f_ck: float, f_yk: float, e_s: float, gamma_c: float = 1.4, gamma_s: float = 1.15) -> float:
    """
    Calcula o momento resistente limite m_rdlim para vigas de concreto armado de seção retangular com armadura simples.

    :param a_st: área de aço tracionado (m2)
    :param b_w: largura da seção (m)
    :param h: altura total da seção (m)
    :param relacao_h_d: relação d/h da seção
    :param f_ck: resistência característica à compressão do concreto (kPa)
    :param f_yk: resistência característica à tração do aço (kPa)
    :param e_s: módulo de elasticidade do aço (kPa)
    :param gamma_c: coeficiente parcial de segurança do concreto (padrão 1.4)
    :param gamma_s: coeficiente parcial de segurança do aço (padrão 1.15)

    :return: momento resistente para seções de armadura simples (kN.m)
    """

    # Propriedades dos materiais e da geometria
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


def profundidade_carbonatacao_possan(k_c, k_fc, f_ck, t, ad, k_ad, co_2, k_co_2, ur, k_rh, k_ce):
    """
    Determina a profundidade de carbonatação do concreto de acordo com o modelo de Possan et al. (2016) 10.1007/s41024-016-0010-9.

    :param k_c: Fator relacionado ao tipo de cimento (Tabela 3a)
    :param k_fc: Fator relacionado à resistência à compressão do concreto (Tabela 3a)
    :param f_ck: Resistência característica do concreto (MPa)
    :param t: Idade da estrutura (anos)
    :param ad: Material pozolânico no concreto (relativo à massa de cimento) (%)
    :param k_ad: Fator relacionado a adições pozolânicas de concreto (Tabela 3a)
    :param co_2: Concentração de CO2 atmosférico (%)
    :param k_co_2: Fator relacionado a concentração de CO2 do ambiente (Tabela 3a)
    :param ur: Umidade relativa média (em % * 0.01)
    :param k_rh: Fator relacionado à umidade relativa (Tabela 3a)
    :param k_ce: Fator relacionado à exposição da estrutura (Tabela 3b)

    :return: Profundidade de carbonatação do concreto (m)
    """

    aux_1 = k_c * (20 / f_ck) ** k_fc
    aux_2 = (t / 20) ** (1 / 2)
    aux_31 =  (k_ad * ad ** (3 / 2)) / (40 + f_ck)
    aux_32 =  (k_co_2 * co_2 ** (1 / 2)) / (60 + f_ck)
    aux_33 = (k_rh * (ur - 0.58) ** 2) / (100 + f_ck)
    y_carb = aux_1 * aux_2 * np.exp(aux_31 + aux_32 - aux_33) * k_ce

    return y_carb/1000


def rcp_co2(ano):
    """
    Determina a concentração de CO2 atmosférico em função do ano de acordo com o modelo.

    Args:
        ano (Integer): Ano (anos)

    Returns:
        co_2_percentual (Float): Concentração de CO2 atmosférico (%)
    """

    i_aux = ano - 2000
    co_2_percentual = (0.07278*i_aux**2 + 1.86395*i_aux + 340.93383) / (1E6/1E2)

    return co_2_percentual


def tempo_iniciacao_corrosao(k_c, k_fc, f_ck, ad, k_ad, k_co_2, ur, k_rh, k_ce, cob, ano_instalacao_estrutura=2000):
    """
    Determina o tempo de iniciação da corrosão das armaduras em função do modelo de Possan et al. (2016) 10.1007/s41024-016-0010-9.

    Args:
        k_c (Float): Fator relacionado ao tipo de cimento (Tabela 3a)
        k_fc (Float): Fator relacionado à resistência à compressão do concreto (Tabela 3a)
        f_ck (Float): Resistência característica do concreto (kPa)
        ad (Float): Material pozolânico no concreto (relativo à massa de cimento) (%)
        k_ad (Float): Fator relacionado a adições pozolânicas de concreto (Tabela 3a)
        k_co_2 (Float): Fator relacionado a concentração de CO2 do ambiente (Tabela 3a)
        ur (Float): Umidade relativa média (em %)
        k_rh (Float): Fator relacionado à umidade relativa (Tabela 3a)
        k_ce (Float): Fator relacionado à exposição da estrutura (Tabela 3b)
        cob (Float): Cobrimento da armadura (m)
        ano_instalacao_estrutura (Integer): Ano de instalação da estrutura (anos)

    Returns:
        inicio_corrosao (Float): Tempo de iniciação da corrosão das armaduras (anos)
        y_carb (Float): Profundidade de carbonatação do concreto (m)
        co_2 (Float): Concentração de CO2 atmosférico (%)
    """

    # Inicializando o ano da estrutura
    ano = ano_instalacao_estrutura

    # Procurando o tempo de iniciação para a amostra em questão (máximo da busca = 150 anos)
    t_max = 150
    for i in range(0, t_max):
        # Equação interpoladora RCP 8.5
        co_2 = rcp_co2(ano)
        y_carb = profundidade_carbonatacao_possan(k_c, k_fc,  f_ck/1000, i,
                                                    ad, k_ad, co_2, k_co_2,
                                                    ur*0.01, k_rh, k_ce)
        if y_carb >= cob:
            ti = i
            break
        else:
            ti = t_max
        ano += 1
        
    return ti, y_carb, co_2


def area_aco_flexao_simples( m_sd: float, b_w: float, h: float, f_ck: float, f_ywk: float = 500000, gamma_c: float = 1.4, gamma_s: float = 1.15, impressao: bool = False) -> float:
    """
    Esta função verifica a área de aço necessária para combater os esforços de flexão na peça de concreto armado de acordo com a NBR 6118 (2014).

    Entrada:

    """
    f_ck /= 1E3
    if f_ck >  50:
        lambdaa = 0.80 - ((f_ck - 50) / 400)
        alpha_c = (1.00 - ((f_ck - 50) / 200)) * 0.85
    else:
        lambdaa = 0.80
        alpha_c = 0.85

    d = h * 0.9
    f_ck *= 1E3
    f_cd = f_ck / gamma_c
    zeta = m_sd / (b_w * alpha_c * f_cd)
    aux = d ** 2 - 2 * zeta
    x = (d - np.sqrt(aux)) / lambdaa
    z = d - 0.50 * lambdaa * x
    f_yd = f_ywk / gamma_s
    a_s = m_sd / (z * f_yd)
    a_c = b_w * h
    pho_s = a_s / a_c * 100

    return a_s, pho_s


def obj_mestrado_victor(x, none_variable):
    """Função objetivo que determina o momento resistente em vigas de concreto armado sujeitas a uma função de decaimento de resistência ao longo do tempo.
    """
    
    # User must copy and paste this code in time reliability objective function-
    id_analysis = int(x[-1])
    time_step = none_variable['time analysis']
    t_i = time_step[id_analysis] 
    # print(t_i)
    # t_i is a time value from your list of times entered in the 'none variable' key.

    # Random variables
    m_g = x[0]
    m_q = x[1]
    f_ck = x[2]
    f_yk = x[3]
    e_r = x[4]
    e_s = x[5]

    # Fixed variables
    gamma_c = none_variable['dados_viga']['gamma_c']
    gamma_s = none_variable['dados_viga']['gamma_s']
    gamma_f = none_variable['dados_viga']['gamma_f']
    b_w = none_variable['dados_viga']['b_w (m)']
    h = none_variable['dados_viga']['h (m)']
    a_s = none_variable['dados_viga']['a_s (m2)']
    
    # Degradation criteria
    if t_i == 0:
        degrad = 1
    else:
        a_d = 1
        b_d = 0.000055
        degrad = a_d * (1 - b_d * t_i ** 2)

    # Capacity and demand
    m_r = momento_resistente_secao_sem_cor(a_s, b_w, h, f_ck, f_yk, gamma_s, gamma_c)
    m_r *= degrad
    m_s = gamma_f * (m_g + m_q)

    # State limit function
    constraint = e_r * m_r - e_s * m_s

    return [m_r * e_r], [m_s * e_s], [constraint]


def verifica_tempo_limite(pf_list: list, temp_list: list, pf_limit: float, plotar: bool=False) -> float:
    """
    Função que verifica e determina o tempo em que a estrutura alcança o valor de pf limite.

    Parâmetros:
    - pf_list: Lista com valores de pf ao longo do tempo.
    - temp_list: Lista com os valores de tempo correspondentes.
    - pf_limit: Valor limite de pf que define a reta horizontal.
    - plotar: Se True, exibe o gráfico das curvas e do ponto de interseção.

    Retorna:
    - x_cross: Valor de tempo onde as curvas se cruzam (None se não houver interseção).
    """
    # Verificando se os dados estão ordenados por tempo
    sorted_indices = np.argsort(temp_list)
    X1 = np.array(temp_list)[sorted_indices]
    Y1 = np.array(pf_list)[sorted_indices]

    # Criando a curva da reta horizontal
    X2 = X1  # Mantemos os mesmos tempos
    Y2 = np.full_like(X1, pf_limit)  # Criamos um array constante com o valor de pf_limit

    # Criando interpolação apenas para pf_list
    f1 = CubicSpline(X1, Y1)

    # Função para encontrar interseção
    def diff(x):
        return f1(x) - pf_limit

    # Definição do intervalo de busca
    x_min, x_max = X1[0], X1[-1]
    x_values = np.linspace(x_min, x_max, 1000)

    x_cross, y_cross = None, None
    for i in range(len(x_values) - 1):
        if diff(x_values[i]) * diff(x_values[i+1]) < 0:
            x_cross = bisect(diff, x_values[i], x_values[i+1])
            y_cross = f1(x_cross)
            # print(f"As curvas se cruzam em X = {x_cross:.2f}, Y = {y_cross:.2f}")
            # print(f"Tempo limite = {x_cross:.2f}")
            break

    # Plotando o gráfico
    if plotar:
        plt.figure(figsize=(8, 6))
        plt.plot(X1, Y1, label="Curva pf", color='blue')
        plt.axhline(y=pf_limit, color='red', linestyle="--", label="pf Limite")  # Linha reta horizontal

        plt.scatter(X1, Y1, color='blue', marker='o', label="Pontos Curva pf")

        if x_cross is not None and y_cross is not None:
            plt.scatter(x_cross, y_cross, color='black', marker='x', s=100, label="Interseção")
            plt.text(x_cross, y_cross, f"({x_cross:.2f}, {y_cross:.2f})", fontsize=12, verticalalignment='bottom')

        plt.xlabel("Ano")
        plt.ylabel("pf")
        plt.title("Interseção das Curvas")
        plt.legend()
        plt.grid(True)
        plt.show()

    return x_cross


def indice_corrosao_(i_corr_20, temperatura):
    """
    Determina o índice de corrosão para processos de corrosão em armaduras de aço considerando a carbonatação do concreto.

    Args:
        i_corr_20 (Float): Índice de corrosão a 20°C μA/cm²
        temperatura (Float): Temperatura do ambiente (°C)
    
    Returns:
        i_corr (Float): Índice de corrosão (μA/cm²) a uma temperatura T
    """

    # Correção para temperaturas diferentes de 20°C
    if temperatura > 20:
        k = 0.073
    elif temperatura < 20:
        k = 0.025
    elif temperatura == 20:
        k = 0
    i_corr = i_corr_20 * (1 + k * (temperatura - 20))

    return i_corr


def momento_resistente_com_corrosao_azad_algohi(d_0, n_barras, f_ck, f_yk, b_w, d, gamma_c, gamma_s, i_corr_20, temperatura, tempo_decorrido, tempo_iniciacao):
    """
    Determina o momento resistente de uma viga de concreto armado sem corrosão.

    Args:
        d_0 (Float): Diâmetro original da barra de aço (m)
        n_barras (int): Número de barras de aço
        f_ck (Float): Resistência característica do concreto (kPa)
        f_yk (Float): Resistência característica do aço (kPa)
        b_w (Float): Largura da seção (m)
        d (Float): Altura útil da seção (m)
        i_corr_20 (Float): Índice de corrosão a 20°C μA/cm²
        temperatura (Float): Temperatura do ambiente (°C)
        tempo_decorrido (Float): Tempo decorrido (anos)
        tempo_iniciacao (Float): Tempo de iniciação da corrosão (anos)
    
    Returns:
        m_rd (Float): Momento resistente da viga (kN.m)
        c_f (Float): Coeficiente de redução da aderência
        d_corroido (Float): Diâmetro corroido da barra de aço (m)
        i_corr (Float): Índice de corrosão (μA/cm²) a uma temperatura T
    """

    # Índice de corrosão
    tempo_corrosao = tempo_decorrido - tempo_iniciacao
    i_corr = indice_corrosao_(i_corr_20, temperatura)

    # Perda de seção devido à corrosão
    d_0 *= 1000
    delta_dim = 0.0232 * i_corr * tempo_corrosao
    d_corroido = d_0 - delta_dim
    d_corroido /= 1000

    # Momento resistente com corrosão considerando apenas perda de seção
    m_rd = momento_resistente_sem_corrosao(d_corroido, n_barras, f_ck, f_yk,
                                           b_w, d, gamma_c, gamma_s)

    # Momento resistente com corrosão considerando perda de seção e redução da aderência
    i_corr /= 1000
    cf_aux = 5 / (d_0 ** 0.54 * (i_corr * tempo_corrosao * 365) ** 0.19)
    if cf_aux > 1.00:
        c_f = 1.00
    else:
        c_f = cf_aux
    m_rd *= c_f

    return m_rd, c_f, d_corroido, i_corr
