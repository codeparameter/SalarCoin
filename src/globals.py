from .nodes.boot import Boot
from .nodes.node import Node


class Mutable:
    g_args = None


# Immutables:
SECONDS_PER_CRAWL = 20


ROUTES = {
    'node/register': (Boot, 'register_node'),
    'node/crawl': (Node, 'crawl'),
}
