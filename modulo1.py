from typing import Union, Callable
import re
from datetime import datetime

from scipy.integrate import quad
import scipy.stats as stats
import numpy as np
from numpy import sqrt, pi, exp
import pandas as pd

import parepy_toolbox.distributions as parepydi


def sampling(n_samples: int, model: dict, variables_setup: list) -> np.ndarray:
    """
    Generates a set of random numbers according to a specified probability distribution model.

    :param n_samples: Number of samples to generate.
    :param model: Dictionary containing the model parameters.
    :param variables_setup: List of dictionaries, each containing parameters for a random variable.

    :return: Numpy array with the generated random samples.
    """

    # Model settings
    model_sampling = model['model sampling'].upper()
    id_type = []
    id_corr = []
    for v in variables_setup:
        if 'parameters' in v and 'corr' in v['parameters']:
            id_type.append('g-corr-g_var')
            id_corr.append(v['parameters']['corr']['var'])
        else:
            id_type.append('g')
    for k in id_corr:
        id_type[k] = 'g-corr-b_var'

    if model_sampling in ['MCS', 'LHS']:
        random_sampling = np.zeros((n_samples, len(variables_setup)))

        for j, variable in enumerate(variables_setup):
            if id_type[j] == 'g-corr-b_var':
                continue
            type_dist = variable['type'].upper()
            seed_dist = variable['seed']
            params = variable['parameters']

            if (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g':
                mean = params['mean']
                sigma = params['sigma']
                parameters = {'mean': mean, 'sigma': sigma}
                random_sampling[:, j] = parepydi.normal_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

            elif (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g-corr-g_var':
                mean = params['mean']
                sigma = params['sigma']
                parameters_g = {'mean': mean, 'sigma': sigma}
                pho = params['corr']['pho']
                m = params['corr']['var']
                parameters_b = variables_setup[m]['parameters']
                random_sampling[:, m], random_sampling[:, j] = parepydi.corr_normal_sampling(parameters_b, parameters_g, pho, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

            elif type_dist == 'UNIFORM' and id_type[j] == 'g':
                min_val = params['min']
                max_val = params['max']
                parameters = {'min': min_val, 'max': max_val}
                random_sampling[:, j] = parepydi.uniform_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

            elif type_dist == 'GUMBEL MAX' and id_type[j] == 'g':
                mean = params['mean']
                sigma = params['sigma']
                parameters = {'mean': mean, 'sigma': sigma}
                random_sampling[:, j] = parepydi.gumbel_max_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

            elif type_dist == 'GUMBEL MIN' and id_type[j] == 'g':
                mean = params['mean']
                sigma = params['sigma']
                parameters = {'mean': mean, 'sigma': sigma}
                random_sampling[:, j] = parepydi.gumbel_min_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

            elif type_dist == 'LOGNORMAL' and id_type[j] == 'g':
                mean = params['mean']
                sigma = params['sigma']
                parameters = {'mean': mean, 'sigma': sigma}
                random_sampling[:, j] = parepydi.lognormal_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

            elif type_dist == 'TRIANGULAR' and id_type[j] == 'g':
                min_val = params['min']
                max_val = params['max']
                mode = params['mode']
                parameters = {'min': min_val, 'max': max_val, 'mode': mode}
                random_sampling[:, j] = parepydi.triangular_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)
    elif model_sampling in ['MCS-TIME', 'MCS_TIME', 'MCS TIME', 'LHS-TIME', 'LHS_TIME', 'LHS TIME']:
        time_analysis = model['time steps']
        random_sampling = np.empty((0, len(variables_setup)))
        match = re.search(r'\b(MCS|LHS)\b', model_sampling.upper(), re.IGNORECASE)
        model_sampling = match.group(1).upper()

        for _ in range(n_samples):
            temporal_sampling = np.zeros((time_analysis, len(variables_setup)))

            for j, variable in enumerate(variables_setup):
                if id_type[j] == 'g-corr-b_var':
                    continue
                type_dist = variable['type'].upper()
                seed_dist = variable['seed']
                sto = variable['stochastic variable']
                params = variable['parameters']

                if (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g':
                    mean = params['mean']
                    sigma = params['sigma']
                    parameters = {'mean': mean, 'sigma': sigma}
                    if sto is False:
                        temporal_sampling[:, j] = parepydi.normal_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                    else:
                        temporal_sampling[:, j] = parepydi.normal_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

                elif (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g-corr-g_var':
                    mean = params['mean']
                    sigma = params['sigma']
                    parameters_g = {'mean': mean, 'sigma': sigma}
                    pho = params['corr']['pho']
                    m = params['corr']['var']
                    parameters_b = variables_setup[m]['parameters']
                    if sto is False:
                        temporal_sampling[:, m], temporal_sampling[:, j] = parepydi.corr_normal_sampling(parameters_b, parameters_g, pho, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                        temporal_sampling[1:, m]
                    else:
                        temporal_sampling[:, m], temporal_sampling[:, j] = parepydi.corr_normal_sampling(parameters_b, parameters_g, pho, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

                elif type_dist == 'UNIFORM' and id_type[j] == 'g':
                    min_val = params['min']
                    max_val = params['max']
                    parameters = {'min': min_val, 'max': max_val}
                    if sto is False:
                        temporal_sampling[:, j] = parepydi.uniform_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                    else:
                        temporal_sampling[:, j] = parepydi.uniform_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

                elif type_dist == 'GUMBEL MAX' and id_type[j] == 'g':
                    mean = params['mean']
                    sigma = params['sigma']
                    parameters = {'mean': mean, 'sigma': sigma}
                    if sto is False:
                        temporal_sampling[:, j] = parepydi.gumbel_max_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                    else:
                        temporal_sampling[:, j] = parepydi.gumbel_max_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

                elif type_dist == 'GUMBEL MIN' and id_type[j] == 'g':
                    mean = params['mean']
                    sigma = params['sigma']
                    parameters = {'mean': mean, 'sigma': sigma}
                    if sto is False:
                        temporal_sampling[:, j] = parepydi.gumbel_min_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                    else:
                        temporal_sampling[:, j] = parepydi.gumbel_min_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

                elif type_dist == 'LOGNORMAL' and id_type[j] == 'g':
                    mean = params['mean']
                    sigma = params['sigma']
                    parameters = {'mean': mean, 'sigma': sigma}
                    if sto is False:
                        temporal_sampling[:, j] = parepydi.lognormal_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                    else:
                        temporal_sampling[:, j] = parepydi.lognormal_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

                elif type_dist == 'TRIANGULAR' and id_type[j] == 'g':
                    min_val = params['min']
                    max_val = params['max']
                    mode = params['mode']
                    parameters = {'min': min_val, 'max': max_val, 'mode': mode}
                    if sto is False:
                        temporal_sampling[:, j] = parepydi.triangular_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
                        temporal_sampling[1:, j]
                    else:
                        temporal_sampling[:, j] = parepydi.triangular_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

            random_sampling = np.concatenate((random_sampling, temporal_sampling), axis=0)  

        time_sampling = np.zeros((time_analysis * n_samples, 1))
        cont = 0
        for _ in range(n_samples):
            for m in range(time_analysis):
                time_sampling[cont, 0] = int(m)
                cont += 1
        random_sampling = np.concatenate((random_sampling, time_sampling), axis=1)   

    return random_sampling


def newton_raphson(f: Callable, df: Callable, x0: float, tol: float) -> float:
    """
    Calculates the root of a function using the Newton-Raphson method.

    :param f: Function for which the root is sought.
    :param df: Derivative of the function.
    :param x0: Initial guess for the root.
    :param tol: Tolerance for convergence.

    :return: Approximated root of the function.
    """

    if abs(f(x0)) < tol:
        return x0
    else:
        return newton_raphson(f, df, x0 - f(x0)/df(x0), tol)


def pf_equation(beta: float) -> float:
    """
    Calculates the probability of failure (pf) for a given reliability index (β), using the cumulative distribution function (CDF) of the standard normal distribution.

    :param beta: Reliability index (β).
    :return: Probability of failure.
    """

    def integrand(x):
        return 1/sqrt(2*np.pi) * np.exp(-x**2/2)

    def integral_x(x):
        integral, _ = quad(integrand, 0, x)
        return 1 - (0.5 + integral)

    return integral_x(beta)


def beta_equation(pf: float) -> Union[float, str]:
    """
    This function calculates the reliability index value for a given probability of failure (pf).

    :param pf: Probability of failure (pf) value to be converted to beta.

    :raises ValueError: If pf is not between 0 and 1.

    :return: Beta value (β) corresponding to the given pf.

    """

    if pf > 0.5:
        beta_value = "minus infinity"
    else:
        F = lambda BETA: BETA*(0.00569689925051199*sqrt(2)*exp(-0.497780952459929*BETA**2)/sqrt(pi) + 0.0131774933075162*sqrt(2)*exp(-0.488400032299965*BETA**2)/sqrt(pi) + 0.0204695783506533*sqrt(2)*exp(-0.471893773055302*BETA**2)/sqrt(pi) + 0.0274523479879179*sqrt(2)*exp(-0.448874334002837*BETA**2)/sqrt(pi) + 0.0340191669061785*sqrt(2)*exp(-0.42018898411968*BETA**2)/sqrt(pi) + 0.0400703501675005*sqrt(2)*exp(-0.386874144322843*BETA**2)/sqrt(pi) + 0.045514130991482*sqrt(2)*exp(-0.350103048710684*BETA**2)/sqrt(pi) + 0.0502679745335254*sqrt(2)*exp(-0.311127540182165*BETA**2)/sqrt(pi) + 0.0542598122371319*sqrt(2)*exp(-0.271217130855817*BETA**2)/sqrt(pi) + 0.0574291295728559*sqrt(2)*exp(-0.231598755762806*BETA**2)/sqrt(pi) + 0.0597278817678925*sqrt(2)*exp(-0.19340060305222*BETA**2)/sqrt(pi) + 0.0611212214951551*sqrt(2)*exp(-0.157603139738968*BETA**2)/sqrt(pi) + 0.0615880268633578*sqrt(2)*exp(-0.125*BETA**2)/sqrt(pi) + 0.0611212214951551*sqrt(2)*exp(-0.0961707934336129*BETA**2)/sqrt(pi) + 0.0597278817678925*sqrt(2)*exp(-0.0714671611917261*BETA**2)/sqrt(pi) + 0.0574291295728559*sqrt(2)*exp(-0.0510126028581118*BETA**2)/sqrt(pi) + 0.0542598122371319*sqrt(2)*exp(-0.0347157651329596*BETA**2)/sqrt(pi) + 0.0502679745335254*sqrt(2)*exp(-0.0222960750615538*BETA**2)/sqrt(pi) + 0.045514130991482*sqrt(2)*exp(-0.0133198644739499*BETA**2)/sqrt(pi) + 0.0400703501675005*sqrt(2)*exp(-0.00724451280416452*BETA**2)/sqrt(pi) + 0.0340191669061785*sqrt(2)*exp(-0.00346766973926267*BETA**2)/sqrt(pi) + 0.0274523479879179*sqrt(2)*exp(-0.00137833506369952*BETA**2)/sqrt(pi) + 0.0204695783506533*sqrt(2)*exp(-0.000406487440814915*BETA**2)/sqrt(pi) + 0.0131774933075162*sqrt(2)*exp(-6.80715702059458e-5*BETA**2)/sqrt(pi) + 0.00569689925051199*sqrt(2)*exp(-2.46756468031828e-6*BETA**2)/sqrt(pi))/2 + pf - 0.5
        F_PRIME = lambda BETA: BETA*(-0.00567161586997623*sqrt(2)*BETA*exp(-0.497780952459929*BETA**2)/sqrt(pi) - 0.0128717763140469*sqrt(2)*BETA*exp(-0.488400032299965*BETA**2)/sqrt(pi) - 0.0193189331214818*sqrt(2)*BETA*exp(-0.471893773055302*BETA**2)/sqrt(pi) - 0.0246453088397815*sqrt(2)*BETA*exp(-0.448874334002837*BETA**2)/sqrt(pi) - 0.0285889583658099*sqrt(2)*BETA*exp(-0.42018898411968*BETA**2)/sqrt(pi) - 0.0310043648675369*sqrt(2)*BETA*exp(-0.386874144322843*BETA**2)/sqrt(pi) - 0.0318692720390705*sqrt(2)*BETA*exp(-0.350103048710684*BETA**2)/sqrt(pi) - 0.031279502533111*sqrt(2)*BETA*exp(-0.311127540182165*BETA**2)/sqrt(pi) - 0.0294323811914605*sqrt(2)*BETA*exp(-0.271217130855817*BETA**2)/sqrt(pi) - 0.0266010299072288*sqrt(2)*BETA*exp(-0.231598755762806*BETA**2)/sqrt(pi) - 0.0231028167058843*sqrt(2)*BETA*exp(-0.19340060305222*BETA**2)/sqrt(pi) - 0.0192657928246347*sqrt(2)*BETA*exp(-0.157603139738968*BETA**2)/sqrt(pi) - 0.0153970067158395*sqrt(2)*BETA*exp(-0.125*BETA**2)/sqrt(pi) - 0.0117561527336413*sqrt(2)*BETA*exp(-0.0961707934336129*BETA**2)/sqrt(pi) - 0.00853716430789267*sqrt(2)*BETA*exp(-0.0714671611917261*BETA**2)/sqrt(pi) - 0.00585921875877428*sqrt(2)*BETA*exp(-0.0510126028581118*BETA**2)/sqrt(pi) - 0.00376734179556552*sqrt(2)*BETA*exp(-0.0347157651329596*BETA**2)/sqrt(pi) - 0.00224155706678351*sqrt(2)*BETA*exp(-0.0222960750615538*BETA**2)/sqrt(pi) - 0.00121248411291229*sqrt(2)*BETA*exp(-0.0133198644739499*BETA**2)/sqrt(pi) - 0.000580580329711626*sqrt(2)*BETA*exp(-0.00724451280416452*BETA**2)/sqrt(pi) - 0.000235934471270962*sqrt(2)*BETA*exp(-0.00346766973926267*BETA**2)/sqrt(pi) - 7.56770676252561e-5*sqrt(2)*BETA*exp(-0.00137833506369952*BETA**2)/sqrt(pi) - 1.66412530366349e-5*sqrt(2)*BETA*exp(-0.000406487440814915*BETA**2)/sqrt(pi) - 1.79402532164194e-6*sqrt(2)*BETA*exp(-6.80715702059458e-5*BETA**2)/sqrt(pi) - 2.81149347557902e-8*sqrt(2)*BETA*exp(-2.46756468031828e-6*BETA**2)/sqrt(pi))/2 + 0.002848449625256*sqrt(2)*exp(-0.497780952459929*BETA**2)/sqrt(pi) + 0.00658874665375808*sqrt(2)*exp(-0.488400032299965*BETA**2)/sqrt(pi) + 0.0102347891753266*sqrt(2)*exp(-0.471893773055302*BETA**2)/sqrt(pi) + 0.0137261739939589*sqrt(2)*exp(-0.448874334002837*BETA**2)/sqrt(pi) + 0.0170095834530893*sqrt(2)*exp(-0.42018898411968*BETA**2)/sqrt(pi) + 0.0200351750837502*sqrt(2)*exp(-0.386874144322843*BETA**2)/sqrt(pi) + 0.022757065495741*sqrt(2)*exp(-0.350103048710684*BETA**2)/sqrt(pi) + 0.0251339872667627*sqrt(2)*exp(-0.311127540182165*BETA**2)/sqrt(pi) + 0.027129906118566*sqrt(2)*exp(-0.271217130855817*BETA**2)/sqrt(pi) + 0.028714564786428*sqrt(2)*exp(-0.231598755762806*BETA**2)/sqrt(pi) + 0.0298639408839463*sqrt(2)*exp(-0.19340060305222*BETA**2)/sqrt(pi) + 0.0305606107475775*sqrt(2)*exp(-0.157603139738968*BETA**2)/sqrt(pi) + 0.0307940134316789*sqrt(2)*exp(-0.125*BETA**2)/sqrt(pi) + 0.0305606107475775*sqrt(2)*exp(-0.0961707934336129*BETA**2)/sqrt(pi) + 0.0298639408839463*sqrt(2)*exp(-0.0714671611917261*BETA**2)/sqrt(pi) + 0.028714564786428*sqrt(2)*exp(-0.0510126028581118*BETA**2)/sqrt(pi) + 0.027129906118566*sqrt(2)*exp(-0.0347157651329596*BETA**2)/sqrt(pi) + 0.0251339872667627*sqrt(2)*exp(-0.0222960750615538*BETA**2)/sqrt(pi) + 0.022757065495741*sqrt(2)*exp(-0.0133198644739499*BETA**2)/sqrt(pi) + 0.0200351750837502*sqrt(2)*exp(-0.00724451280416452*BETA**2)/sqrt(pi) + 0.0170095834530893*sqrt(2)*exp(-0.00346766973926267*BETA**2)/sqrt(pi) + 0.0137261739939589*sqrt(2)*exp(-0.00137833506369952*BETA**2)/sqrt(pi) + 0.0102347891753266*sqrt(2)*exp(-0.000406487440814915*BETA**2)/sqrt(pi) + 0.00658874665375808*sqrt(2)*exp(-6.80715702059458e-5*BETA**2)/sqrt(pi) + 0.002848449625256*sqrt(2)*exp(-2.46756468031828e-6*BETA**2)/sqrt(pi)
        beta_value = newton_raphson(F, F_PRIME, 0.0, 1E-15)

        return beta_value


def calc_pf_beta(df_or_path: Union[pd.DataFrame, str], numerical_model: str, n_constraints: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculates the probability of failure (pf) and reliability index (β) based on the columns of a DataFrame
    that start with 'I' (indicator function). If a .txt file path is passed, this function evaluates pf and β values too.

    :param df_or_path: A DataFrame containing boolean indicator columns prefixed with 'I', or a string path to a .txt file.

    :param numerical_model: Dictionary containing the numerical model.

    :param n_constraints: Number of limit state functions or constraints.

    :return: Tuple of DataFrames:

        - df_pf: probability of failure values for each column prefixed with 'G'.
        - df_beta: reliability index values for each column prefixed with 'G'.
    """

    # Read dataset
    if isinstance(df_or_path, str) and df_or_path.endswith('.txt'):
        df = pd.read_csv(df_or_path, delimiter='\t')
    else:
        df = df_or_path

    # Calculate pf and beta values
    if numerical_model.upper() in ['MCS', 'LHS']:
        filtered_df = df.filter(like='I_', axis=1)
        pf_results = filtered_df.mean(axis=0)
        df_pf = pd.DataFrame([pf_results.to_list()], columns=pf_results.index)
        beta_results = [beta_equation(pf) for pf in pf_results.to_list()] 
        df_beta = pd.DataFrame([beta_results], columns=pf_results.index)
    elif numerical_model.upper() in ['TIME-MCS', 'TIME-LHS', 'TIME MCS', 'TIME LHS', 'MCS TIME', 'LHS TIME', 'MCS-TIME', 'LHS-TIME']:
        df_pf = pd.DataFrame()
        df_beta = pd.DataFrame()
        for i in range(n_constraints):
            filtered_df = df.filter(like=f'I_{i}', axis=1)
            pf_results = filtered_df.mean(axis=0)
            beta_results = [beta_equation(pf) for pf in pf_results.to_list()]
            df_pf[f'G_{i}'] = pf_results.to_list()
            df_beta[f'G_{i}'] = beta_results

    return df_pf, df_beta

def cornell_algorithm_structural_analysis(setup: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Applies the Cornell reliability algorithm to evaluate the probability of failure and reliability index.

    :param setup: Dictionary containing the input settings, including:
    
        - 'variables settings': list of variable configurations with 'mean' and 'sigma' values,
        - 'objective function': function that returns a list of g values,
        - 'none variable': additional fixed parameters for the objective function.

    :return: Tuple of two DataFrames:

        - pf_dataframe: DataFrame containing the probability of failure (pf) for each limit state.
        - beta_dataframe: DataFrame containing the reliability index (β) for each limit state.
    """
    sigma = []  # 'mean'
    var = []    # 'sigma'

    for var_config in setup['variables settings']:
        mean = var_config['parameters']['mean']
        std = var_config['parameters']['sigma']
        sigma.append(mean)
        var.append(std)

    g_list = setup['objective function'](sigma, setup['none variable'])

    beta_list = []
    pf_list = []

    total_variance = sum(std ** 2 for std in var)
    sigma_total = sqrt(total_variance)

    for g_i in g_list:
        beta_i = g_i / sigma_total
        pf_i = pf_equation(beta_i)
        beta_list.append(beta_i)
        pf_list.append(pf_i)

    pf_columns = [f'pf_{i}' for i in range(len(pf_list))]
    beta_columns = [f'beta_{i}' for i in range(len(beta_list))]

    pf_dataframe = pd.DataFrame([pf_list], columns=pf_columns)
    beta_dataframe = pd.DataFrame([beta_list], columns=beta_columns)

    return pf_dataframe, beta_dataframe
