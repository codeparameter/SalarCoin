import argparse
from src.nodes.node import Node
from src.nodes.boot import Boot
from src.nodes.miner import Miner
from src.globals import Mutable

if __name__ == "__main__":
    # TODO
    #  nodes can be shut down and run again with their previous wallet and connection graph
    parser = argparse.ArgumentParser(description="Salar Blockchain Network")
    parser.add_argument("-N", "--network", action="store_true", help="Start a fake blockchain network")
    parser.add_argument("-n", "--node", action="store_true", help="Run in node mode")
    parser.add_argument("-m", "--miner", action="store_true", help="Run in miner mode")
    parser.add_argument("-t", "--test", action="store_true", help="Run in test mode")
    # test mode is for network to act randomly
    args = parser.parse_args()
    Mutable.g_args = args

    Boot.run()

    if args.network:
        # TODO
        #  threads
        pass
    elif args.node:
        Node.run()
    elif args.miner:
        Miner.run()
    elif args.test:
        # TODO
        #  threads
        pass
    else:
        print("Please specify either --network -N or --node -n or --miner -m or --test -t mode.")
