
<a href='#AboutMe'>navigate down</a>
# Table.of.Contents
SalarCoin whitepaper concepts:

# 1.Nodes.Peering:

the general steps and components involved in creating a basic blockchain node discovery system:

1. Bootstrap Nodes: Blockchain networks often have a set of well-known "bootstrap nodes" that serve as entry points for new nodes to join the network. These nodes are maintained by the community and have fixed addresses.

2. Peer-to-Peer Protocol: we'll need to implement a peer-to-peer (P2P) communication protocol that allows nodes to exchange information. Common P2P protocols include Bitcoin's TCP-based protocol and Ethereum's Devp2p protocol.

3. Node Registration: Nodes, when they start up, need to register themselves with the network. They send a message to one or more bootstrap nodes to announce their presence.

4. Discovery Messages: Nodes send periodic "discovery" messages to peers they know about. These messages contain information about their own identity, IP address, and port.

5. Neighbor Management: Nodes keep a list of known peers and regularly exchange information about the state of the network. If they receive a discovery message from an unknown node, they add it to their list of peers.

6. Network Crawling: Nodes can perform network crawling by randomly selecting peers from their list and requesting information about their peers. This helps in expanding the network view.

<pre>
Note: for simplicity I handled crawling and discovery together in one process, as following instructor:
    
    When a node is crawling toward random neighbor nodes, 
    it's identity would be treated as discovery message.
    So if target node would add the origin node in its neighbors list if it hasn't before. 
    Then, for crawling response, it would send its neighbors to origin node.
</pre>

2. Security: Implement security measures to prevent spam and malicious behavior, such as rate limiting, IP banning, and handshake procedures.


2) Kademlia

Ensuring that there is always a route between nodes without registering them
to all bootstrap nodes can be achieved by implementing a routing algorithm.
One popular algorithm used in many blockchain networks is Kademlia.

Addressing and Node Discovery:
Kademlia uses a unique identifier (Node ID) for each node in the network,
typically based on a cryptographic hash of the node's public key.
In a blockchain, these Node IDs can be used as addresses for nodes or data.
When a node needs to find a specific piece of data or locate
another node (e.g., for transaction propagation or block validation),
it can use the Kademlia algorithm to efficiently discover the closest nodes based on their Node IDs.

# About.Me
references:
<a>navigate top</a>
<footer>margin top</footer>