import hashlib
import os
import unittest


import src.user_mgmt.authentication as auth


class TestAuthentication(unittest.TestCase):

    def test_hashes_password_using_salt(self):
        plaintext_password = 'a_password'
        salt = os.urandom(32)
        hashed_password = auth.hash_password(plaintext_password, salt)
        sha256 = hashlib.sha256(plaintext_password.encode())
        sha256.update(salt)
        self.assertEqual(hashed_password, sha256.hexdigest())