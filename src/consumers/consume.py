from . import IndexData
from .consume_bovespa import consume_bovespa
from .consume_bovespa_dividend import consume_bovespa_dividend
from .consume_ifix import consume_ifix
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
