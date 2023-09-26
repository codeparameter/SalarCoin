from src.node.wallet import Boot
from src.node.wallet import Node


class Mutable:
    # var = default_val
    pass


# Immutables:

# VAR = 'default_val'

SECONDS_PER_CRAWL = 20


ROUTES = {
    'node/register': (Boot, 'register_node'),
    'node/crawl': (Node, 'crawl'),
}
