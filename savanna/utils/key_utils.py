__author__ = 'akuznetsov'

from Crypto.PublicKey import RSA
from Crypto import Random
import paramiko
import StringIO


def get_user_public_key(nova_client, user_key):
    return nova_client.keypairs.find(name=user_key)


def generate_private_key(length=2048):
    random_generator = Random.new().read
    rsa = RSA.generate(length, random_generator)
    return rsa.exportKey('PEM')


def read_private_key(key):
    return paramiko.RSAKey(file_obj=StringIO.StringIO(key))


def get_public_key_openssh(key):
    return RSA.importKey(key).exportKey('OpenSSH')
