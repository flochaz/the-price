#!/usr/bin/env python

import boto3

def encrypt_data(key,data):
    kms = boto3.client('kms', region_name='us-east-1')
    encrypted = kms.encrypt(KeyId=key, Plaintext=data)
    Encrpyted_Data = encrypted['CiphertextBlob']
    return Encrpyted_Data

def decrypt_data(encrypted_data):
    kms = boto3.client('kms', region_name='us-east-1')
    decrypted = kms.decrypt(CiphertextBlob=encrypted_data)
    Decrypted_Data = decrypted['Plaintext']
    return Decrypted_Data

