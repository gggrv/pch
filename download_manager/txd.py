# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script txd.

Contains text aid.
"""

def chop( text, L, R ):
    """Chops the text str as instructed."""
    A, B = 0, len(text) # это соотв. iloc, изменится в будущем
    
    #если присутствует L
    if type(L)==int: A = L
    elif type(L)==str: A = text.find(L)+len(L)
    text = text[A:]
    
    #если присутствует R
    if type(R)==int: B = R
    elif type(R)==str: B = [B,text.find(R)][R in text]
    
    return text[:B].strip()

def xxx( i, total, text, w=10, ok='+', no='x' ):
    """
    Console progress bar. Call from within a loop.
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    per100 = i/total
    nfilled = int( w*per100 )
    info, bar = chop(str(100*per100),None,'.'), ok*nfilled+no*(w-nfilled)
    line = ( '\r%s %s %s' ) % ( text, bar, info+'%' )
    print( line, end='\r' )
    if i==total: print()

#---------------------------------------------------------------------------+++
# конец 2018.00.00 → 2020.11.21
