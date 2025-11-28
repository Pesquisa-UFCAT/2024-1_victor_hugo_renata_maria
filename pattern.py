def std_matrix(std: list) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract D matrix and D^-1 matrix from a list of variables. Used in Y to X or X to Y transformation.

    :param std: Standard deviation parameters

    return: output[0] = D matrix, output[1] = D^-1 matrix
    """

    dneq = np.zeros((len(std), len(std)))
    dneq1 = np.zeros((len(std), len(std)))
    for i, sigma in enumerate(std):
        dneq[i, i] = sigma
        dneq1[i, i] = 1 / sigma

    return dneq, dneq1


def mu_matrix(mean: list) -> np.ndarray:
    """
    Extract mean matrix from a list of variables. Used in Y to X or X to Y transformation.

    :param mu: Mean parameters

    return: Mean matrix
    """

    mu_neq = np.zeros((len(mean), 1))
    for i, mu in enumerate(mean):
        mu_neq[i, 0] = mu

    return mu_neq