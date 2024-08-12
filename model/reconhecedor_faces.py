from usuario import Usuario
import cv2
import face_recognition as fr
import numpy as np

class ReconhecerFaces:
    
    def __init__(self):
        self._banco_de_dados = None
        self._captura_video = cv2.VideoCapture(0)
        
    def carrega_face(self, caminho_foto):
        foto = fr.load_image_file(caminho_foto)
        rosto_codificacao = fr.face_encodings(foto)
        
        if len(rostos) > 0:
            return True, rosto_codificacao
        
        return False, []
    
    def reconhecer_faces(self):
        
        while True:
            ret, frame = self._captura_video.read()
            
            # Redimensiona a imagem para 1/4 do tamanho para melhor processamento
            frame_diminuido = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # converte a imagem de BGR para RGB
            rgb_frame = frame_diminuido[:, :, ::-1]
            
            localizacao_rosto = fr.face_locations(rgb_frame)
            rostos_desconhecidos = fr.face_encodings(rgb_frame, localizacao_rosto)
            
            for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_rosto, rostos_desconhecidos):
                # colocar os rostos salvos no banco de dados
                resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)
                
                face_distances = fr.face_distance(rostos_conhecidos, rosto_desconhecido)
                
                maior_id = np.argmin(face_distances)
                nome = "desconhecido"
                if resultados[maior_id]:
                    nome = nome_rostos[maior_id]
                    
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, nome, (left +6, bottom - 6),cv2.FONT_HERSHEY_COMPLEX, 1.0, (255,255,255), 1)
            
            cv2.imshow("reconhecimento facial", frame)
            
            if cv2.waitKey(1) & 0XFF == ord("q"):
                break
            
        self.captura_video.release()
        cv2.destroyAllWindows()
    
    
        
        
        
        
        
        
        
        
        





