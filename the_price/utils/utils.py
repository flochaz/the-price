#!/usr/bin/env python

import boto3

@staticmethod
def resolv_strategy(shop):
    """
    Static function enabling to find the corresponding strategy finder to use from a user input
    :param shop: user entry that needs to be linked to an existing finder
    :return: finder class name
    """
    #TODO: implem introspection
    return 'AmazonPriceFinder'

def encrypt_data(key,data):
    kms = boto3.client('kms')
    encrypted = kms.encrypt(KeyId=key, Plaintext=data)
    Encrpyted_Data = encrypted['CiphertextBlob']
    return Encrpyted_Data

def decrypt_data(encrypted_data):
    kms = boto3.client('kms')
    decrypted = kms.decrypt(CiphertextBlob=encrypted_data)
    Decrypted_Data = decrypted['Plaintext']
    return Decrypted_Data

