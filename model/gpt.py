# gpt 

import face_recognition
import cv2

class ReconhecimentoFacial:
    def __init__(self):
        self.codificacoes_faces_conhecidas = []
        self.nomes_faces_conhecidas = []
        self.captura_video = cv2.VideoCapture(0)

    def carregar_faces_conhecidas(self, imagens, nomes):
        """
        Carrega imagens conhecidas e seus nomes associados.

        :param imagens: Lista de caminhos para as imagens conhecidas.
        :param nomes: Lista de nomes associados às imagens.
        """
        for caminho_imagem, nome in zip(imagens, nomes):
            imagem = face_recognition.load_image_file(caminho_imagem)
            codificacao = face_recognition.face_encodings(imagem)[0]
            self.codificacoes_faces_conhecidas.append(codificacao)
            self.nomes_faces_conhecidas.append(nome)

    def reconhecer_faces(self):
        """
        Captura imagens da webcam e reconhece rostos.
        """
        while True:
            # Captura frame por frame
            ret, frame = self.captura_video.read()
            
            # Redimensiona a imagem para 1/4 do tamanho para processamento mais rápido
            pequeno_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Converte a imagem do BGR (OpenCV) para RGB (face_recognition)
            rgb_pequeno_frame = pequeno_frame[:, :, ::-1]
            
            # Encontra todos os rostos e suas codificações na imagem atual
            locais_faces = face_recognition.face_locations(rgb_pequeno_frame)
            codificacoes_faces = face_recognition.face_encodings(rgb_pequeno_frame, locais_faces)
            
            for (topo, direita, baixo, esquerda), codificacao_face in zip(locais_faces, codificacoes_faces):
                # Veja se a face encontrada corresponde a alguma face conhecida
                correspondencias = face_recognition.compare_faces(self.codificacoes_faces_conhecidas, codificacao_face)
                nome = "Desconhecido"
                
                # Se há alguma correspondência
                if True in correspondencias:
                    primeiro_indice_correspondencia = correspondencias.index(True)
                    nome = self.nomes_faces_conhecidas[primeiro_indice_correspondencia]
                
                # Desenha um retângulo ao redor da face
                topo *= 4
                direita *= 4
                baixo *= 4
                esquerda *= 4
                
                cv2.rectangle(frame, (esquerda, topo), (direita, baixo), (0, 0, 255), 2)
                fonte = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, nome, (esquerda + 6, baixo - 6), fonte, 0.5, (255, 255, 255), 1)
            
            # Exibe o resultado
            cv2.imshow('Vídeo', frame)
            
            # Pressione 'q' para sair do loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Libere os recursos
        self.captura_video.release()
        cv2.destroyAllWindows()

# Exemplo de uso
if __name__ == "__main__":
    reconhecimento = ReconhecimentoFacial()
    # Carregue imagens e nomes conhecidos
    reconhecimento.carregar_faces_conhecidas(['caminho_para_imagem1.jpg', 'caminho_para_imagem2.jpg'], ['Nome1', 'Nome2'])
    reconhecimento.reconhecer_faces()