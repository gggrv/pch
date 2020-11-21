# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script main.
"""

# embedded in python
import sys
# pip install
from PyQt5 import QtWidgets
# same folder
import gxd
from downloader import dthread

class centralwidget( QtWidgets.QWidget ):
    
    def __init__( self,
                  dlr,
                  parent=None,
                  *args, **kwargs ):
        super( centralwidget, self ).__init__( parent, *args, **kwargs )
        
        self.dlr = dlr # downloader pointer
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        tabber = gxd.tabber( self.dlr, self )
        
        # assemble
        lyt = QtWidgets.QVBoxLayout()
        lyt.setObjectName( 'centralwidget_lyt' )
        lyt.addWidget( tabber )
        self.setLayout( lyt )
        
    def _init( self ):
        self.setObjectName( 'centralwidget' )

class mainwindow( QtWidgets.QMainWindow ):
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( mainwindow, self ).__init__( parent, *args, **kwargs )
        
        self.dlr = dthread() # downloader pointer
        
        # downloader setup
        self.dlr.dlStart.connect( self.dlStart )
        self.dlr.dlFinish.connect( self.dlFinish )
        
        # gui
        self._init()
        self._init_staticwidgets()
        self._init_menubar()
        self._init_statusbar()
        
    """---------------------------------------------------------------------+++
    Everything about menubar.
    """
    def menubar_loadqueues( self ):
        """Reloads queues."""
        cw = self.findChild( QtWidgets.QWidget,'centralwidget' )
        tabber = cw.findChild( QtWidgets.QTabWidget,'tabber' )
        tabber.load_queues()
        
    def menubar_savequeues( self ):
        """Forces save queues."""
        cw = self.findChild( QtWidgets.QWidget,'centralwidget' )
        tabber = cw.findChild( QtWidgets.QTabWidget,'tabber' )
        tabber.save_queues()
        
    def menubar_clearqueues( self ):
        """Forces clears queues."""
        cw = self.findChild( QtWidgets.QWidget,'centralwidget' )
        tabber = cw.findChild( QtWidgets.QTabWidget,'tabber' )
        tabber.clear_queues()
        
    def _menubar_dl( self ):
        self.menubar_savequeues()
        self.dlr.start()
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    def _changestatus( self ):
        sb = self.findChild( QtWidgets.QStatusBar,'statusbar' )
        
        # change status
        if self.dlr.DOWNLOADING: self.dlr.DOWNLOADING=False
        else: self.dlr.DOWNLOADING=True
        
        text = 'Downloading' if self.dlr.DOWNLOADING else 'Paused'
        sb.bt.setText( text )
        
        # manually run method
        self._menubar_dl()
        
    def dlStart( self, url ):
        sb = self.findChild( QtWidgets.QStatusBar,'statusbar' )
        sb.l1.setText( url )
        
    def dlFinish( self, success ):
        self.menubar_loadqueues()
        sb = self.findChild( QtWidgets.QStatusBar,'statusbar' )
        
        sb.l1.setText( 'Done' )
        
    def closeEvent( self, ev ):
        ev.accept()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        w = centralwidget( self.dlr, self )
        self.setCentralWidget( w )
        
    def _init_menubar( self ):
        # menubar
        m = QtWidgets.QMenuBar( self )
        m.setObjectName( 'menubar' )
        
        # file menu actions
        #sa_act = QtWidgets.QAction( 'Save queues', self )
        #sa_act.setShortcut( 'Ctrl+S' )
        #sa_act.triggered.connect( self.menubar_savequeues )
        #lo_act = QtWidgets.QAction( 'Load queues', self )
        #lo_act.setShortcut( 'Ctrl+L' )
        #lo_act.triggered.connect( self.menubar_loadqueues )
        cl_act = QtWidgets.QAction( 'Clear queues', self )
        cl_act.setShortcut( 'Ctrl+Q' )
        cl_act.triggered.connect( self.menubar_clearqueues )
        # file menu itself
        filemenu = m.addMenu( 'File' )
        #filemenu.addAction(sa_act)
        #filemenu.addAction(lo_act)
        filemenu.addAction(cl_act)
        
        self.setMenuBar( m )
        
    def _init_statusbar( self ):
        sb = QtWidgets.QStatusBar( self )
        sb.setObjectName( 'statusbar' )
        self.setStatusBar( sb )
        
        # unnamed pushbutton that starts/stops downloading
        sb.bt = QtWidgets.QPushButton( sb )
        sb.bt.clicked.connect( self._changestatus )
        A = 'Downloading' if self.dlr.DOWNLOADING else 'Paused'
        sb.bt.setText( A )
        
        # unnamed label that shows stats
        sb.l1 = QtWidgets.QLabel( sb )
        
        sb.addWidget(sb.bt)
        sb.addWidget(sb.l1)
        
    def _init( self ):
        self.setObjectName( 'mainwindow' )
        self.setWindowTitle( 'download manager' )

class application( object ):
    
    def __init__( self,
                  *args, **kwargs ):
        super( application, self ).__init__( *args, **kwargs )
        
        # gui
        self._init()
        
        # infinite mainloop
        sys.exit( self.app.exec_() )
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.app = QtWidgets.QApplication( sys.argv )
        
        self.w = mainwindow()
        self.w.show()
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    ob = application()

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2020.11.21 → 2020.11.22
