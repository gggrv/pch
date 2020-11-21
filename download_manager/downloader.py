# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script downloader.

Contains console downloader application.
"""

# embedded in python
import os
# pip install
from PyQt5 import QtCore
import requests
# same folder
from nxd import download

class downloader( object ):
    
    # queues
    QS = {
        'next':[],
        'fail':[],
        'done':[],
        }
    
    DEST = os.getcwd() # folder for downloaded files
    
    DOWNLOADING = False # downloading allowed status
    
    def __init__( self,
                  *args, **kwargs ):
        super( downloader, self ).__init__( *args, **kwargs )
        
        self.load('next')
        self.load('fail')
        self.load('done')
        
    """---------------------------------------------------------------------+++
    Everything about i/o.
    """
    def set_destination_folder( self, path ):
        """Tries to set destination folder.
        If path is invalid, assignds dest to rootdir."""
        try:
            if not os.path.exists(path): os.makedirs(path)
            self.DEST = path
        except OSError:
            self.DEST = os.getcwd()
        
    def save( self, k ):
        """Saves queue in self.QS to text file."""
        name = '%s.txt'%k
        with open( name, 'w', encoding='utf-8' ) as f:
            f.write( '\n'.join(self.QS[k]) )
            
    def load( self, k ):
        """Loads queue to self.QS from text file."""
        name = '%s.txt'%k
        if not os.path.exists(name): return None
        with open( name, 'r', encoding='utf-8' ) as f:
            self.QS[k] = f.read().split('\n')
        
    """---------------------------------------------------------------------+++
    Everything about downloading.
    """
    def geturl( self, k, drop=False ):
        """Gets next url from specified queue. Skips empty lines."""
        for iloc, url in enumerate(self.QS[k]):
            if len(url)>0:
                # validate url
                x = requests.utils.urlparse(url)
                if x.netloc=='': # this is not a url
                    self.set_destination_folder(url)
                    continue # anyway
                
                # url is valid
                if drop:
                    self.QS[k].pop(iloc)
                    self.save(k)
                return url
            
    def moveurl( self, k_from, k_to ):
        url = self.geturl( k_from, drop=True ) # autosaves after drop
        self.QS[k_to].insert(0,url)
        self.save(k_to)
            
    def download_fromqueue( self, k ):
        while self.DOWNLOADING:
            url = self.geturl(k)
            if not url: break # got None
            
            #self.dlStart.emit(url) # emit pyqt5 signal (url)
            
            download( url, dest=self.DEST )
            self.moveurl('next','done')
            #self.dlFinish.emit(True) # emit pyqt5 signal (success)

class dthread( QtCore.QThread, downloader ):
    
    # pyqt signals
    dlStart = QtCore.pyqtSignal( str, name='dlStart' )
    dlFinish = QtCore.pyqtSignal( bool, name='dlFinish' )
    
    def __init__( self,
                  *args, **kwargs ):
        super( dthread, self ).__init__( *args, **kwargs )
        
    """---------------------------------------------------------------------+++
    Everything about subclassing downloader.
    """
            
    def download_fromqueue( self, k ):
        url = self.geturl(k)
        if not url: return None # got None
        
        self.dlStart.emit(url)
        
        download( url, dest=self.DEST )
        
        self.moveurl('next','done')
        
        self.dlFinish.emit(True)
        
    """---------------------------------------------------------------------+++
    Everything about subclassing QtCore.QThread.
    """
    def run( self ):
        while self.DOWNLOADING:
            self.download_fromqueue('next')
            self.sleep(2)
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    """
    # downloader usage example
    ob = downloader()
    ob.set_destination_folder('Downloads')
    ob.DOWNLOADING=True
    ob.download_fromqueue('next')

    # dthread usage example
    ob = dthread()
    ob.set_destination_folder('Downloads')
    ob.DOWNLOADING=True
    ob.start()
    """
    
if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2020.11.21 → 2020.11.22
