class Pedido(object):
    def __init__(self, pedido=None, quantidade=0):
        self.pedido = pedido
        self.quantidade = quantidade

    @property
    def pedido(self):
        return self._pedido
    
    @pedido.setter
    def pedido(self, pedido):
        self._pedido = pedido


    @property
    def quantidade(self):
        return self._quantidade
    
    @quantidade.setter
    def quantidade(self, quantidade):
        self._quantidade = quantidade

