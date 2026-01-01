from backend.wg.keys import generate_keypair
from backend.wg.peers import add_peer, remove_peer

priv, pub = generate_keypair()

print("PRIVATE:", priv)
print("PUBLIC:", pub)

add_peer(pub, "10.10.0.2")
print("Peer added")

input("Press Enter to remove peer...")
remove_peer(pub)
print("Peer removed")
