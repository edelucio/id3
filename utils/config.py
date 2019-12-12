import ast


def carregar_config_csv(arq_config):
    with open(arq_config, 'r') as arq:
        d_config = arq.read().replace('\n', '')

    return ast.literal_eval(d_config)