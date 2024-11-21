from kyber import Kyber512  



pk, sk = Kyber512.keygen()

c, key = Kyber512.enc(pk)

_key = Kyber512.dec(c, sk)

_c, key2 = Kyber512.enc(pk)

_key2 = Kyber512.dec(_c, key2)

print(len(key))

print(key == key2)

