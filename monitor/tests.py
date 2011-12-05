from django.test.client import Client
from django.test import TestCase

def newfaulty_layer(post_data):
    #insert into the database any layers that are faulty
    c = Client()
class TestFaultyLayersCmd(TestCase):
    def setUp(self):
        self.post_data = {
                'layer_name' :'NIC_0.5s_1000y',
                'error_code':'401',
                'created' : None,
                'content_type' : None, 
                'object_id' : None,
                'content_object' : None, 
                }
