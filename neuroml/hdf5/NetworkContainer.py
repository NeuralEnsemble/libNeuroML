'''
Work in progress..

'''


import neuroml

class NetworkContainer(neuroml.Network):

    def info(self):
        return "%s: id=%s"%(self.__class__(),self.id)
    
        

if __name__ == '__main__':
    
    nc = NetworkContainer(id="testnet")
    
    print(nc.info())
    
    print nc.populations