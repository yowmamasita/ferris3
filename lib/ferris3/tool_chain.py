from .chain import Chain
from .utils import ndb, messages


class ToolChain(Chain):
    pass


ToolChain.add_chain_module(ndb)
ToolChain.add_chain_module(messages)
