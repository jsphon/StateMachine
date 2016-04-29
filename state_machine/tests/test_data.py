import unittest
from state_machine.data import Data
import os

class DataTests(unittest.TestCase):

    def setUp(self):
        name = 'test'
        d    = Data( name )
        d.clear()
        self.assertFalse( os.path.exists( d.filename ) )

    def test___init__(self):
        name = 'test'
        d    = Data( name )

    def test_set_get(self):
        '''
        Test set and get at the same time
        '''
        name = 'test'
        d    = Data( name )
        d.set( 'hello', 'world' )
        self.assertEqual( 'world', d.get( 'hello' ) )

    def test_set_multi(self):
        '''
        Test set and get at the same time
        '''
        name = 'test'
        d    = Data( name )
        d.set_multi( hello='world', foo='bar' )
        self.assertEqual( 'world', d.get( 'hello' ) )
        self.assertEqual( 'bar', d.get( 'foo' ) )


    def test___setitem____getitem__(self):

        name = 'test'
        d    = Data( name )
        d[ 'hello' ] = 'world'
        self.assertEqual( 'world', d[ 'hello' ] )


    def test_log(self):
        d = Data('test')
        d.log( 'hello world' )