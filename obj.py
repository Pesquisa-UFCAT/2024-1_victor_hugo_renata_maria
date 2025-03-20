import numpy as np

"""Arquivo com funções de momento resistente da viga de seção retangular"""


def momento_limite_armadura_simples(b_w: float, h: float, f_ck: float, gamma_c: float = 1.4) -> float:
    """
    Calcula o momento resistente limite m_rdlim para vigas de concreto armado.

    Args:
        b_w: largura da seção transversal
        d: altura útil da seção transversal
        f_ck: resistência de característica à compressão do concreto
        gamma_c: coeficiente parcial de segurança para o concreto

    Returns:
        mrdlim: valor do momento resistente limite utilizando armadura simples
    """
    f_ck /= 1E3
    if f_ck >  50:
        lambdaa = 0.80 - ((f_ck - 50) / 400)
        alpha_c = (1.00 - ((f_ck - 50) / 200)) * 0.85
        beta = 0.35
    else:
        lambdaa = 0.80
        alpha_c = 0.85
        beta = 0.45
    f_ck *= 1E3
    f_cd = f_ck / gamma_c

    d = h * 0.9

    return b_w * d**2 * lambdaa * beta * alpha_c * f_cd * (1 - 0.5 * lambdaa * beta)


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


def momento_resistente_secao_sem_cor(a_s: float, b_w: float, h: float, f_ck: float, f_yk: float = 500000, gamma_s: float = 1.15, gamma_c: float = 1.40) -> float:
    """
    Calcula o momento resistente para vigas de concreto armado.

    Args:
        f_ck: resistência característica à compressão do concreto (em kPa)
        a_s: área da armadura longitudinal (em mm²)
        b_w: largura da seção transversal (em mm)
        h: altura total da seção transversal (em mm)

    Returns:
        m_rd: valor do momento resistente limite utilizando armadura simples (em N.mm)
    """

    f_ck /= 1E3
    if f_ck > 50:
        lambdaa = 0.80 - ((f_ck - 50) / 400)
        alpha_c = (1.00 - ((f_ck - 50) / 200)) * 0.85
    else:
        lambdaa = 0.80
        alpha_c = 0.85

    f_ck *= 1E3
    f_cd = f_ck / gamma_c
    d = h * 0.9
    x = ((a_s * f_yk) / (f_cd * b_w * alpha_c * lambdaa))
    m_rd = a_s * f_yk * (d - x * 0.5 * lambdaa)
    return m_rd


def obj_mestrado_victor(x, none_variable):
    """Função objetivo que determina o momento resistente em vigas de concreto armado sujeitas a uma função de decaimento de resistência ao longo do tempo.
    """
    
    # User must copy and paste this code in time reliability objective function-
    id_analysis = int(x[-1])
    time_step = none_variable['time analysis']
    t_i = time_step[id_analysis] 
    print(t_i)
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


def verfica_tempo_limite(pf_list: list, temp_list: list, pf_limit: float) -> float
    """
    """
    
    return temp_limit


if __name__ == "__main__":
    x = [5000,5000,5000,5000,2,10,10]
    dados_viga = {'h (m)': 0.50, 'b_w (m)': 0.30, 'm_rd (kN.m)': 0, 'a_s (m2)': 0.15/100*0.30*0.50, 'gamma_c': 1.00, 'gamma_s': 1.00, 'gamma_f': 1.00}
    # dados_viga = {'d_b (m)': 8/1000, 'd_linha (m)': 3.9/100,'n_b': 3, 'gamma_c': 1.00, 'gamma_s': 1.00, 'b_w (m)': 0.2, 'h (m)': 0.50, 'cob (m)': 0.025, 'ano_construcao': 2000}
    # dados_corrosao = {'k_c': 30.5, 'k_fc': 1.7, 'a_d': 0, 'k_ad': 0.32, 'k_co2': 15.5, 'k_rh': 1300, 'k_ce': 1.3}
    none_variable = {'dados_viga': dados_viga, 'time analysis': list(range(0, 101))}
    print(obj_mestrado_victor(x, none_variable))