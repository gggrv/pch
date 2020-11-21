# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script gxd.

Provides additional gui classes.
"""

# pip install
from PyQt5 import QtWidgets

class _sampletab( QtWidgets.QWidget ):
    """Sample tab for QtWidgets.QTableWidget."""
    
    def __init__( self,
                  dlr,
                  k,
                  parent=None,
                  *args, **kwargs ):
        super( _sampletab, self ).__init__( parent, *args, **kwargs )
        
        self.dlr = dlr # downloader pointer
        self.k = k # downloader queue key
        
        # gui
        self._init_staticwidgets()
        
        self.pull_text()
        
    """---------------------------------------------------------------------+++
    Everything about self.dlr.
    """
    def push_text( self ):
        """Pushes data to specified self.dlr queue."""
        ta = self.findChild( QtWidgets.QTextEdit,'sampletab_textarea' )
        lines = ta.toPlainText().split('\n')
        self.dlr.QS[self.k] = lines
        self.dlr.save( self.k )
        
    def pull_text( self ):
        """Pull data from specified self.dlr queue."""
        ta = self.findChild( QtWidgets.QTextEdit,'sampletab_textarea' )
        text = '\n'.join( self.dlr.QS[self.k] )
        ta.setText(text)
        
    def clear_text( self ):
        """Clears data in specified self.dlr queue."""
        ta = self.findChild( QtWidgets.QTextEdit,'sampletab_textarea' )
        ta.setText('')
        self.push_text()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        ta = QtWidgets.QTextEdit( self )
        ta.setObjectName( 'sampletab_textarea' )
        ta.setFontFamily('consolas')
        
        # assemble
        lyt = QtWidgets.QVBoxLayout()
        lyt.setObjectName( 'sampletab_lyt' )
        lyt.addWidget( ta )
        self.setLayout( lyt )

class tabber( QtWidgets.QTabWidget ):
    
    # programmatic tabnames, currently match self.dlr.QS keys
    # gui tabnames are hardcoded in self._init_staticwidgets()
    tabnames = [
        'fail',
        'done',
        'next',
        ]
    
    def __init__( self,
                  dlr,
                  parent=None,
                  *args, **kwargs ):
        super( tabber, self ).__init__( parent, *args, **kwargs )
        
        self.dlr = dlr # downloader pointer
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about tabs.
    """
    def gettab( self, tabname ):
        tab = self.findChild( _sampletab,'tabber_'+tabname )
        return tab
    
    def save_queues( self ):
        """Manually pushes text from tabs to self.dlr and saves it."""
        for tabname in self.tabnames:
            tab = self.gettab(tabname)
            tab.push_text()
    
    def load_queues( self ):
        """Manually pulls text from self.dlr to tabs."""
        for tabname in self.tabnames:
            tab = self.gettab(tabname)
            tab.pull_text()
    
    def clear_queues( self ):
        """Manually clears text in self.dlr and tabs."""
        for tabname in self.tabnames:
            tab = self.gettab(tabname)
            tab.clear_text()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        # tab with failed
        tabf = _sampletab( self.dlr, self.tabnames[0], self )
        tabf.setObjectName( 'tabber_'+self.tabnames[0] )
        
        # tab with done
        tabd = _sampletab( self.dlr, self.tabnames[1], self )
        tabd.setObjectName( 'tabber_'+self.tabnames[1] )
        
        # tab with next
        tabn = _sampletab( self.dlr, self.tabnames[2], self )
        tabn.setObjectName( 'tabber_'+self.tabnames[2] )
        
        # assemble
        self.addTab( tabn,'next' )
        self.addTab( tabf,'fail' )
        self.addTab( tabd,'done' )
        
    def _init( self ):
        self.setObjectName( 'tabber' )
    
#---------------------------------------------------------------------------+++
# конец 2020.10.24 → 2020.11.22
