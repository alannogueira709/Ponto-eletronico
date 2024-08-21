class Usuario():
    
    def __init__(self, nome, foto_encoding):
        self._nome = nome
        #self._foto = foto
        self._encoding = foto_encoding
        
    def __str__(self):
        return f"{self._nome} cadastrado"
        
    
