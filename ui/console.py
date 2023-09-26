import argparse
from globals import Mutable
from src.node.types.block_makers.miner import Miner
from src.node.types.node import Node


class Console:

    # handling user inputs
    @staticmethod
    def input():
        pass

    @staticmethod
    def start():
        # TODO
        #  node can be shut down and run again with their previous wallet and connection graph
        parser = argparse.ArgumentParser(description="Salar Blockchain Network")
        parser.add_argument("-t", "--test", action="store_true", help="Start a fake blockchain network")
        parser.add_argument("-u", "--user", action="store_true", help="Run in user mode")
        parser.add_argument("-n", "--node", action="store_true", help="Run in node mode")
        parser.add_argument("-m", "--miner", action="store_true", help="Run in miner mode")
        # test mode is for network to act randomly
        args = parser.parse_args()
        Mutable.g_args = args

        if args.user:
            # TODO
            pass
        elif args.node:
            # TODO
            Node.run()
        elif args.miner:
            # TODO
            Miner.run()
        elif args.test:
            # TODO
            pass
        else:
            print("Please specify either --user -u --node -n or --miner -m or --test -t mode.")
            print("note: test would create a fake network")
