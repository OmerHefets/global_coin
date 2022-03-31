import sys
sys.path.append("")

from blockchain.miner.mining.block_assembler import BlockAssembler
from blockchain.miner.mining.mining_alg import Miner
from blockchain.node.bl.unified_block import UnifiedBlock
import json
import yaml
import requests

#TODO: REFACTOR ALL OF THIS LATER

DIFF_ROUTE = '/node/difficulty'
BLOCK_INSERTION_ROUTE = '/insert/block/'

def config_miner():
    with open(r'blockchain/miner/client/config.yaml') as file:
        document = yaml.full_load(file)

    miner_addr = document['miner_addr']
    node_url = document['node_url']
    node_difficulty = requests.get(url=(node_url+DIFF_ROUTE)).json()['difficulty']

    return (miner_addr, node_url, node_difficulty)


miner_addr, node_url, node_difficulty = config_miner()


miner = Miner()
ba = BlockAssembler(miner_addr=miner_addr, node_url=node_url, difficulty=node_difficulty)


try:
    while True:
        print("Starting computation on a new block...")

        pre_hash_unified_block = ba.assemble_pre_hash_unified_block()
        print(f"New assembled block: {pre_hash_unified_block}\n")

        after_hash_unified_block = miner.mine_block(unified_block=pre_hash_unified_block)
        print(f"Mined new block's hash: {after_hash_unified_block.hash}")

        ba.update_unified_block_txs_hash(unified_block=after_hash_unified_block)

        print()

        res = requests.post(url=(node_url+BLOCK_INSERTION_ROUTE), 
                    data=json.dumps(UnifiedBlock.convert_unified_block_to_dict(after_hash_unified_block)))

        print(res.json())
except KeyboardInterrupt:
    print('exit miner...')