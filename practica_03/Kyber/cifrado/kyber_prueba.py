from kyber import Kyber512  



pk, sk = Kyber512.keygen()

c, key = Kyber512.enc(pk)

_c, key2 = Kyber512.enc(pk)

print(len(key))

print(c == _c)