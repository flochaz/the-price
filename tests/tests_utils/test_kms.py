from the_price.utils import utils

import unittest
import boto3
import base64

class test_kms(unittest.TestCase):

    def test_encrypt_decrypt_no_base64(self):

        boto_master_key_id = '37778f56-196d-47aa-bc4f-20637167e230'

        AMAZON_ACCESS_KEY="AAAAAAAAAAAAAAAAAAAA"
        AMAZON_SECRET_KEY="0Aaaaaaaaa/veggegegeg4g43g33g3g33g3g3g33"
        AMAZON_ASSOC_TAG="assoctag-23"

        #I encrypt my message using boto_master_key_id
        ENCRYPTED_AMAZON_ACCESS_KEY = utils.encrypt_data(boto_master_key_id,AMAZON_ACCESS_KEY)
        ENCRYPTED_AMAZON_SECRET_KEY = utils.encrypt_data(boto_master_key_id,AMAZON_SECRET_KEY)
        ENCRYPTED_AMAZON_ASSOC_TAG = utils.encrypt_data(boto_master_key_id,AMAZON_ASSOC_TAG)

        self.assertEqual(AMAZON_ACCESS_KEY, utils.decrypt_data(ENCRYPTED_AMAZON_ACCESS_KEY))
        self.assertEqual(AMAZON_SECRET_KEY, utils.decrypt_data(ENCRYPTED_AMAZON_SECRET_KEY))
        self.assertEqual(AMAZON_ASSOC_TAG, utils.decrypt_data(ENCRYPTED_AMAZON_ASSOC_TAG))




    def test_encrypt_decrypt_base64(self):

        kms = boto3.client('kms')
        boto_master_key_id = '37778f56-196d-47aa-bc4f-20637167e230'

        AMAZON_ACCESS_KEY="AAAAAAAAAAAAAAAAAAAA"
        AMAZON_SECRET_KEY="0Aaaaaaaaa/veggegegeg4g43g33g3g33g3g3g33"
        AMAZON_ASSOC_TAG="assoctag-23"

        #I encrypt my message using boto_master_key_id
        ENCRYPTED_AMAZON_ACCESS_KEY = base64.b64encode(utils.encrypt_data(boto_master_key_id,AMAZON_ACCESS_KEY))
        ENCRYPTED_AMAZON_SECRET_KEY = base64.b64encode(utils.encrypt_data(boto_master_key_id,AMAZON_SECRET_KEY))
        ENCRYPTED_AMAZON_ASSOC_TAG = base64.b64encode(utils.encrypt_data(boto_master_key_id,AMAZON_ASSOC_TAG))

        self.assertEqual(AMAZON_ACCESS_KEY, utils.decrypt_data(base64.b64decode(ENCRYPTED_AMAZON_ACCESS_KEY)))
        self.assertEqual(AMAZON_SECRET_KEY, utils.decrypt_data(base64.b64decode(ENCRYPTED_AMAZON_SECRET_KEY)))
        self.assertEqual(AMAZON_ASSOC_TAG, utils.decrypt_data(base64.b64decode(ENCRYPTED_AMAZON_ASSOC_TAG)))
