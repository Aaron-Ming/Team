# -*- coding:utf8 -*-

import binascii, os

gen_token = lambda :binascii.b2a_base64(os.urandom(24))[:-1]

if __name__ == "__main__":
    print gen_token()
