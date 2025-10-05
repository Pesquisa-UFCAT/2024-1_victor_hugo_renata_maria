f"""Função objetivo para determinar o momento resistente de uma viga de concreto armado com e sem corrosão."""
import math
import time


def meu_problema_murilo(x, none_variable):
    """
    Problema de otimização para determinar o momento resistente de uma viga de concreto armado com e sem corrosão.
    
    Args:
        x (List): Lista com as variáveis de decisão
        none_variable (Dict): Dicionário com as variáveis deterministicas de projeto
    """

    # Atribuindo o tempo (tempo_i) de análise de acordo com o time step desejado
    id_analisado_tempo_i = int(x[-1])
    serie_tempo_iral = none_variable['tempos reais']
    tempo_i = serie_tempo_iral[id_analisado_tempo_i]

    # Variáveis aleatórias
    carga_g = x[0]
    carga_q = x[1]
    f_ck = x[2]
    f_yk = x[3]
    temp = x[4]
    ur = x[5]
    if x[6] < 0.10:
        i_corr_20 = 0.10
    else:
        i_corr_20 = x[6]
    theta_r = x[7]
    theta_s = x[8]

    # Constantes geométricas
    D_BARRAS = none_variable['dados_viga']['d_b (m)']
    N_BARRAS = none_variable['dados_viga']['n_b']
    B_W = none_variable['dados_viga']['b_w (m)']
    H = none_variable['dados_viga']['h (m)']
    COB = none_variable['dados_viga']['cob (m)']
    GAMMA_C = none_variable['dados_viga']['gamma_c']
    GAMMA_S = none_variable['dados_viga']['gamma_s']
    ANO_CONSTRUCAO_ESTRUTURA = none_variable['dados_viga']['ano_construcao']
    D_UTIL = H - none_variable['dados_viga']['d_linha (m)']

    # Constantes de despassivação da armadura
    K_C = none_variable['dados_corrosao']['k_c']
    K_FC = none_variable['dados_corrosao']['k_fc']
    A_D = none_variable['dados_corrosao']['a_d']
    K_AD = none_variable['dados_corrosao']['k_ad']
    K_CO2 = none_variable['dados_corrosao']['k_co2']
    K_RH = none_variable['dados_corrosao']['k_rh']
    K_CE = none_variable['dados_corrosao']['k_ce']

    # Esforços (sistema bi - apoiado)
    m_sd = carga_g + carga_q

    # Determinando o tempo de iniciação da corrosão das armaduras
    t_cor_0, _, co2 = tempo_iniciacao_corrosao(K_C, K_FC, f_ck,
                                       A_D, K_AD, K_CO2,
                                       ur,K_RH, K_CE, COB, ANO_CONSTRUCAO_ESTRUTURA)
    
    co_2 = rcp_co2(ANO_CONSTRUCAO_ESTRUTURA + tempo_i)
    y_carb = profundidade_carbonatacao_possan(K_C, K_FC,  f_ck/1000, tempo_i,
                                                    A_D, K_AD, co_2, K_CO2,
                                                    ur*0.01, K_RH, K_CE)


    return [t_cor_0, y_carb], [1, 1], [1, 1]


def profundidade_carbonatacao_possan(k_c, k_fc, f_ck, t, ad, k_ad, co_2, k_co_2, ur, k_rh, k_ce):
    """
    Determina a profundidade de carbonatação do concreto de acordo com o modelo de Possan et al. (2016) 10.1007/s41024-016-0010-9.

    Args:
        k_c (Float): Fator relacionado ao tipo de cimento (Tabela 3a)
        k_fc (Float): Fator relacionado à resistência à compressão do concreto (Tabela 3a)
        f_ck (Float): Resistência característica do concreto (MPa)
        t (Float): Idade da estrutura (anos)
        ad (Float): Material pozolânico no concreto (relativo à massa de cimento) (%)
        k_ad (Float): Fator relacionado a adições pozolânicas de concreto (Tabela 3a)
        co_2 (Float): Concentração de CO2 atmosférico (%)
        k_co_2 (Float): Fator relacionado a concentração de CO2 do ambiente (Tabela 3a)
        ur (Float): Umidade relativa média (em % * 0.01)
        k_rh (Float): Fator relacionado à umidade relativa (Tabela 3a)
        k_ce (Float): Fator relacionado à exposição da estrutura (Tabela 3b)

    Returns:
        y_carb (Float): Profundidade de carbonatação do concreto (m)
    """

    aux_1 = k_c * (20 / f_ck) ** k_fc
    aux_2 = (t / 20) ** (1 / 2)
    aux_31 =  (k_ad * ad ** (3 / 2)) / (40 + f_ck)
    aux_32 =  (k_co_2 * co_2 ** (1 / 2)) / (60 + f_ck)
    aux_33 = (k_rh * (ur - 0.58) ** 2) / (100 + f_ck)
    y_carb = aux_1 * aux_2 * math.exp(aux_31 + aux_32 - aux_33) * k_ce

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


def momento_resistente_sem_corrosao(d_barras, n_barras, f_ck, f_yk, b_w, d, gamma_c, gamma_s):
    """
    Determina o momento resistente de uma viga de concreto armado sem corrosão.

    Args: 
        d_barras (Float): Diâmetro da barra de aço (m)
        n_barras (int): Número de barras de aço
        f_ck (Float): Resistência característica do concreto (kPa)
        f_yk (Float): Resistência característica do aço (kPa)
        b_w (Float): Largura da seção (m)
        d (Float): Altura útil da seção (m)
        gamma_c (Float): Coeficiente de ponderação do concreto
        gamma_s (Float): Coeficiente de ponderação do aço
            
    Returns:
        m_rd (Float): Momento resistente da viga (kN.m)
    """

    # Resistência de cálculo
    f_cd = f_ck / gamma_c
    f_yd = f_yk / gamma_s

    # Propriedades do dimensionamento
    f_ck /= 1E3
    if f_ck >  50:
        lambda_c = 0.80 - ((f_ck - 50) / 400)
        alpha_c = (1.00 - ((f_ck - 50) / 200)) * 0.85
        beta = 0.35
    else:
        lambda_c = 0.80
        alpha_c = 0.85
        beta = 0.45
    f_ck *= 1E3

    # Momento resistente
    area_aco = n_barras * ((math.pi * d_barras ** 2) / 4)
    x_iii = (area_aco * f_yd) / (alpha_c * f_cd * b_w * lambda_c)
    m_rd = area_aco * f_yd * (d - 0.50 * lambda_c * x_iii)

    return m_rd


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


if __name__ == "__main__":

    # Profundida de carbonatação
    k_c = 30.5
    k_fc = 1.7
    k_ad = 0.0
    k_co2 = 15.5
    k_rh = 1300
    k_ce = 1.30
    ad = 0
    f_ck = 29071.097197
    co2 = 0.04562
    ur = 64.3183
    y_carb = []
    for i in range(0, 101):
        y_carb.append(profundidade_carbonatacao_possan(k_c, k_fc,  f_ck/1000,
                                                       i, ad, k_ad, co2, k_co2,
                                                       ur/100, k_rh, k_ce))
    print('profundidade de carbonatacao com 100 anos (m): ', y_carb[-1])

    # Tempo de iniciação da corrosão
    cob = 2.5/100
    t_cor_0 = tempo_iniciacao_corrosao(k_c, k_fc, f_ck,
                                       ad, k_ad, k_co2,
                                       ur,k_rh, k_ce, cob, 2023)
    print('tempo de inicio de corrosao (anos): ', t_cor_0)

    # Momento resistente sem corrosão
    d_barras = 8/1000
    n_barras = 3
    f_ck = 25E3
    f_yk = 500E3
    b_w = 0.20
    d_linha = 3.9/100
    h = 0.5
    d = h - d_linha
    gamma_c, gamma_s = 1.00, 1.00
    m_rd = momento_resistente_sem_corrosao(d_barras, n_barras, f_ck, f_yk, b_w, d, gamma_c, gamma_s)
    print('momento resistente sem corrosao (kN.m): ', m_rd)

    # Momento resistente sem corrosão
    d_barras = 8/1000
    n_barras = 3
    f_ck = 29071.097197
    f_yk = 602379.18505
    b_w = 0.20
    d_linha = 3.9/100
    h = 0.5
    d = h - d_linha
    print(d)
    m_rd = momento_resistente_sem_corrosao(d_barras, n_barras, f_ck, f_yk, b_w, d, gamma_c, gamma_s)
    print('momento resistente sem corrosao (kN.m): ', m_rd)

    # Momento resistente sem corrosão
    d_barras = 12.5/1000
    n_barras = 4
    f_ck = 25E3
    f_yk = 500E3
    b_w = 0.20
    d_linha = 4.1/100
    h = 0.5
    d = h - d_linha
    m_rd = momento_resistente_sem_corrosao(d_barras, n_barras, f_ck, f_yk, b_w, d, gamma_c, gamma_s)
    print('momento resistente sem corrosao (kN.m): ', m_rd)

    # Momento resistente sem corrosão
    d_barras = 16/1000
    n_barras = 4
    f_ck = 25E3
    f_yk = 500E3
    b_w = 0.20
    d_linha = 4.3/100
    h = 0.5
    d = h - d_linha
    m_rd = momento_resistente_sem_corrosao(d_barras, n_barras, f_ck, f_yk, b_w, d, gamma_c, gamma_s)
    print('momento resistente sem corrosao (kN.m): ', m_rd)

    # Índice de corrosão
    i_cor20 = 1E-5
    temp = 40
    i_cor = indice_corrosao_(i_cor20, temp)
    print('indice de corrosao (microA/cm2): ', i_cor)

    # Momento resistente com corrosão
    t = 50
    t_i_cor = 32
    m_rd, c_f, d_novo = momento_resistente_com_corrosao_azad_algohi(d_barras, n_barras, f_ck, f_yk,
                                                                    b_w, d, gamma_c, gamma_s,
                                                                    i_cor20, temp, t, t_i_cor)
    print('diametro d novo: ', d_novo, 'c_f: ', c_f, 'momento resistente com corrosao (kN.m): ', m_rd)
