from usuario import Usuario
from reconhecedor_faces import ReconhecerFaces
from banco_de_dados import Banco_de_dados


class PontoEletronico:
    
    def __init__(self):
        self._reconhecimento_facial = ReconhecerFaces()
        self._banco_de_dados = Banco_de_dados()
    
    def _cadastrar_Usuario(self, nome, caminho_foto):
        cond, rosto_encodings = self._reconhecimento_facial.carrega_face(caminho_foto)
        
        if cond:
            usuario = Usuario(nome, rosto_encodings)
            self._banco_de_dados._inserir_usuario(usuario)
        
    
    def _listar_usuarios(self):
        for usuario in self._banco_de_dados.retorna_usuarios():
                print(f"{usuario._nome}, entrou{type(usuario._encoding)}")
        
        
    def _iniciar_reconhecimento(self):
        usuarios = self._banco_de_dados.retorna_usuarios()
        nomes = []
        rostos = []
        for usuario in usuarios:
            nomes.append(usuario._nome)
            rostos.append(usuario._encoding)
        self._reconhecimento_facial.reconhecer_faces(nomes, rostos)
        
    
def main():
    pe = PontoEletronico()
    # pe._cadastrar_Usuario("Adriano", "pessoas/adriano.jpeg")
    # pe._cadastrar_Usuario("tony", "pessoas/tony.jpg")
    # pe._cadastrar_Usuario("elon", "pessoas/elon.jpg")
    pe._listar_usuarios()
    pe._iniciar_reconhecimento()

    # ele adiciona e exibe usuarios apenas não reconhece a foto
    pe._banco_de_dados._fechar_conexao()
    
    
    
if __name__ == "__main__":
    main()