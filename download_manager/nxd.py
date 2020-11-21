# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script nxd.

Contains downloading aid.
"""

# embedded in python
import os
import datetime as dt
# pip install
import requests
# same folder
            
def _dl_bychunks( r, url, path, chunk_size=512 ):
    """One of possible download methods."""
    with open( path, 'wb' ) as f:
        for chunk in r.iter_content( chunk_size=chunk_size ):
            if not chunk: break # no need for new keep-alive chunks
            f.write(chunk)
            f.flush() # force the buffer content in f without closing it
            
def _foolcheck( url ):
    url = url.strip()
    return url

def _getname( url ):
    dest = os.path.split(url)[1]
    forbidden = list(':?|\\/')
    for c in forbidden: dest=dest.replace(c,'_')
    if dest=='': dest=_getname( str(dt.datetime.now()) )
    return dest

def download( url, dest='.', name='', chunk_size=512 ):
    """Chooses the best method to download a file,
    makes sure to close everything afterwards."""
    url = _foolcheck(url)
    with requests.get( url, stream=True ) as r:
        
        # destination
        if name=='': name=_getname(url)
        dest = os.path.join( dest,name )
        
        # file size, might be invalid
        k = 'Content-Length'
        data_len = r.headers[k] if k in r.headers else '0'
        data_len = int(data_len) if data_len.isdecimal() else 0
        
        _dl_bychunks( r, url, dest, chunk_size=chunk_size )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    pass

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2020.11.21 → 2020.11.21
