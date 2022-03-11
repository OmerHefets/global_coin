import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

class BlockchainDatabaseException(Exception):
    pass

class TxDatabaseException(Exception):
    pass

class TxPoolDatabaseException(Exception):
    pass

class UtxoDatabaseException(Exception):
    pass