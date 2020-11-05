import os   #local

dev_key = os.urandom(24)
test_key = os.urandom(24)

print('Dev key:', dev_key)
# >>>   <\xeaD\xe8*o/\xc2\xddR\xdc\xe3\xad\xf6\x04 \xd3\xfa\xe1\xb0p\xeb:!

print('Test key:', test_key)
# >>> \xc8\xaaj\xbf\x0c\xe5\xbb\xb1\xcc\x10?\x83i\x1b\x93]\x07$\xd8\xaf\xfb\xed\xa9\x0c

salt = os.urandom(24)
print('Password hashing salt:', salt)
# >>> [|1\xfa\xb7\x13\xbb^c\x9a-i7\xbb\xba`\x19\xa4\x83A\xe0U\x94]
