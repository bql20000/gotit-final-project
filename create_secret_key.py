import os

dev_key = os.urandom(24)
test_key = os.urandom(24)

print('Dev key:', dev_key)
# >>>   <\xeaD\xe8*o/\xc2\xddR\xdc\xe3\xad\xf6\x04 \xd3\xfa\xe1\xb0p\xeb:!

print('Test key:', test_key)
# >>>
