import tkinter as tk
from PIL import Image, ImageTk
import cv2

class PontoEletronicoApp():
    def __init__(self):
        # instanciar 
        self.root = tk.Tk()
        self.root.title("Webcam Viewer")
        self.root.geometry("1000x600")
        
        # Cria um widget Label para exibir o vídeo
        self.label = tk.Label(self.root)
        self.label.pack(expand=True, fill=tk.BOTH)

        # Iniciar a captura da webcam
        self.video_source = 0  # 0 para a webcam padrão
        self.video_cap = cv2.VideoCapture(self.video_source)

        # Iniciar a atualização do vídeo
        self.update_video()

    def update_video(self):
        ret, frame = self.video_cap.read()
        if ret:
            # Converta o frame para RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Converta o frame para um objeto Image
            image = Image.fromarray(frame)
            # Converta o Image para um objeto PhotoImage
            photo = ImageTk.PhotoImage(image)
            # Atualize a label com o novo frame
            self.label.config(image=photo)
            self.label.image = photo
        # Chama o método novamente após 30 ms
        self.after(30, self.update_video)

    def on_closing(self):
        # Libere a captura da webcam e feche a aplicação
        if self.video_cap.isOpened():
            self.video_cap.release()
        self.destroy()

if __name__ == "__main__":
    app = PontoEletronicoApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Limpeza ao fechar
    app.mainloop()
