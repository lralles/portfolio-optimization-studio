from . import IndexData
from .consume_bovespa import consume_bovespa
from .consume_bovespa_dividend import consume_bovespa_dividend
from .consume_ifix import consume_ifix
from .consume_idkaipca10 import consume_idkaipca10
from .consume_idkaipca15 import consume_idkaipca15
from .consume_idkaipca20 import consume_idkaipca20
from .consume_idkaipca2 import consume_idkaipca2
from .consume_idkaipca3 import consume_idkaipca3
from .consume_idkaipca5 import consume_idkaipca5
from .consume_idkaipca30 import consume_idkaipca30
from .consume_idkapre1 import consume_idkapre1
from .consume_idkapre2 import consume_idkapre2
from .consume_idkapre3 import consume_idkapre3
from .consume_idkapre5 import consume_idkapre5
from .consume_imab import consume_imab
from .consume_imab5 import consume_imab5
from .consume_imab5mais import consume_imab5mais
from .consume_imas import consume_imas
from .consume_ipca import consume_ipca
from .consume_irfm import consume_irfm
from .consume_irfm1 import consume_irfm1
from .consume_irfm1mais import consume_irfm1mais
from .consume_msci import consume_msci
from .consume_mscibrl import consume_mscibrl
from .consume_sp500 import consume_sp500
from .consume_sp500brl import consume_sp500brl
from .consume_usdbrl import consume_usdbrl

CONSUMERS = {
    'bovespa': consume_bovespa,
    'bovespa_dividend': consume_bovespa_dividend,
    'ifix': consume_ifix,
    'idkaipca10': consume_idkaipca10,
    'idkaipca15': consume_idkaipca15,
    'idkaipca20': consume_idkaipca20,
    'idkaipca2': consume_idkaipca2,
    'idkaipca3': consume_idkaipca3,
    'idkaipca5': consume_idkaipca5,
    'idkaipca30': consume_idkaipca30,
    'idkapre1': consume_idkapre1,
    'idkapre2': consume_idkapre2,
    'idkapre3': consume_idkapre3,
    'idkapre5': consume_idkapre5,
    'imab': consume_imab,
    'imab5': consume_imab5,
    'imab5mais': consume_imab5mais,
    'imas': consume_imas,
    'ipca': consume_ipca,
    'irfm': consume_irfm,
    'irfm1': consume_irfm1,
    'irfm1mais': consume_irfm1mais,
    'msci': consume_msci,
    'mscibrl': consume_mscibrl,
    'sp500': consume_sp500,
    'sp500brl': consume_sp500brl,
    'usdbrl': consume_usdbrl,
}


def consume(index_name: str) -> IndexData:
    consumer = CONSUMERS.get(index_name)
    if consumer is None:
        available_indexes = ', '.join(sorted(CONSUMERS.keys()))
        raise ValueError(f"Unknown index '{index_name}'. Available indexes: {available_indexes}")
    return consumer()
