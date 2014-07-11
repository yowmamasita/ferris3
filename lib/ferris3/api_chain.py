from .chain import Chain
from .utils import ndb, messages


class ApiChain(Chain):
    pass


ApiChain.add_chain_module(ndb)
ApiChain.add_chain_module(messages)
