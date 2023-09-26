@classmethod
def adr(cls, pk: 'KeyObject'):
    adr = KeyObject('Public Address')
    # getting address from public key
    # Run SHA-256 for the public key
    sha256_bpk = hashlib.sha256(pk.b)
    sha256_bpk_digest = sha256_bpk.digest()
    # Run RIPEMD-160 for the SHA-256
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')

    network_public_key_bytes = b'00' + ripemd160_bpk_hex

    # Double SHA256 to get checksum
    sha256_net_bpk = hashlib.sha256(network_public_key_bytes)
    sha256_net_bpk_digest = sha256_net_bpk.digest()
    sha256_2_net_bpk = hashlib.sha256(sha256_net_bpk_digest)
    sha256_2_net_bpk_digest = sha256_2_net_bpk.digest()
    sha256_2_hex = codecs.encode(sha256_2_net_bpk_digest, 'hex')
    checksum = sha256_2_hex[:8]

    adr.h = network_public_key_bytes + checksum
    adr.b = codecs.decode(adr.h, 'hex')
    adr.b58 = base58.b58encode(adr.b)
