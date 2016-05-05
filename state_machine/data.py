import datetime
import os
import json

class Data( object ):
    """ Store a state machine's state """

    def __init__( self, name=None, folder='/tmp/states' ):
        if not os.path.exists( folder ):
            os.makedirs( folder, exist_ok=True )
        self.folder = folder
        self.name   = name
        uid    = ( ''.join( [ x for x in name if x.isalnum() or ( x in ( ',', '.', '_', '-' ) ) ] ) )
        self.filename = os.path.join( folder, '%s.json'%uid )

    def __getitem__(self, item):
        return self.get( item)

    def __setitem__(self, key, value):
        self.set( key, value )

    def __repr__(self):
        return 'Data:%s[%s]'%(self.name,self.filename)

    def is_new(self):
        return not os.path.exists(self.filename)

    def set(self, key, value):
        data = self._read()
        if ( key in data ) and ( data[ key ]==value ):
            # don't need to do anything
            return

        data[ key ] = value
        self._write( data )

    def set_multi(self, **kwargs ):
        data = self._read()
        data.update( kwargs )
        self._write(data)

    def _read(self):
        if os.path.exists( self.filename ):
            with open( self.filename, 'r' ) as f:
                sdata = f.read()
            if sdata:
                data = json.loads( sdata )
            else:
                data = {}
        else:
            data = {}
        return data

    def _write(self, data):
        with open( self.filename, 'w' ) as f:
            sdata = json.dumps( data )
            f.write( sdata )

    def get(self, key):
        if os.path.exists( self.filename ):
            with open( self.filename, 'r' ) as f:
                data = json.load( f )
                if key in data:
                    return data[ key ]

    def clear(self):
        if os.path.exists( self.filename ):
            os.remove( self.filename )

    def log(self, msg):
        log = self.get( 'log' )
        log = log or ''
        line = '%s %s'%(datetime.datetime.utcnow(), msg )
        log = ( log + '\n%s'%line ) if log else line
        self.set( 'log', log )