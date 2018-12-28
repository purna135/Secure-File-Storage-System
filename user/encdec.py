import threading
import base64

def encryption( filename , encno ) :
    fd = open( filename , 'rb')
    data = fd . read()
    fd . close()

    data = chr( int(encno))   + data [: : -1 ].decode ( 'latin-1')
    data = data . encode ( 'latin-1', "ignore")
    data = base64 . b64encode ( data )

    fd = open( filename , 'wb')
    fd . write( data )
    fd . close()
    return 'Success fully encrypted with key '


def decryption(filename, decno):
    fd = open(filename, 'rb')
    data= fd. read()
    fd . close()
    data = base64.b64decode(data)
    encno = data[0]
    if chr(encno) == chr(int(decno)):
        data = data.decode('latin-1')
        data = data[:0:-1].encode('latin-1')
        fd = open(filename, 'wb')
        fd . write(data)
        fd . close()
        t=threading.Thread(target=encryption, args=(filename, encno))
        t.start()
        return True
    else:
        return False
