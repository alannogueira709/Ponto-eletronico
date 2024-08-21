from usuario import Usuario
from banco_de_dados import Banco_de_dados
import cv2
import face_recognition as fr
import numpy as np

class ReconhecerFaces:
    
    def __init__(self):
        self._captura_video = cv2.VideoCapture(0)
        self._rostos_salvos = []
        self._nomes_salvos = []
        
    def carrega_face(self, caminho_foto):
        foto = fr.load_image_file(caminho_foto)
        rosto_codificacao = fr.face_encodings(foto)
        
        if len(rosto_codificacao) > 0:
            return True, rosto_codificacao
        
        return False, []
    
    def encerrar_reconhecimento(self):
        self._captura_video.release()
        cv2.destroyAllWindows()
    
    def reconhecer_faces(self, nomes, rostos):
        self._nomes_salvos = nomes
        self._rostos_salvos = rostos
        while True:
            ret, frame = self._captura_video.read()
            
            localizacao_rostos = fr.face_locations(frame)
            rostos_desconhecidos = fr.face_encodings(frame, localizacao_rostos)
            
            for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_rostos, rostos_desconhecidos):
                    resultados = fr.compare_faces(self._rostos_salvos, rosto_desconhecido)
                    face_distances = fr.face_distance(self._rostos_salvos, rosto_desconhecido)
                    
                    maior_id = np.argmin(face_distances)
                    
                    if resultados[maior_id]:
                        nome = self._nomes_salvos[maior_id]
                    else:
                        nome = "desconhecido"
                        
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, nome, (left +6, bottom - 6),cv2.FONT_HERSHEY_COMPLEX, 1.0, (255,255,255), 1)
                    
            cv2.imshow("reconhecimento facial", frame)
            
            if cv2.waitKey(1) & 0XFF == ord("q"):
                self.encerrar_reconhecimento()
            
