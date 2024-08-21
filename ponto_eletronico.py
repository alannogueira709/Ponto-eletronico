from usuario import Usuario
from reconhecedor_faces import ReconhecerFaces
from banco_de_dados import Banco_de_dados
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class PontoEletronico:
    def __init__(self, root):
        self._reconhecimento_facial = ReconhecerFaces()
        self._banco_de_dados = Banco_de_dados()
        
        self.root = root
        self.root.title("Sistema de Reconhecimento Facial")
        
        
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.cap = cv2.VideoCapture(0)
        self.update_video()
        
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        ##self.add_button = tk.Button(self.root, text="Adicionar Usuário", command=self._adicionar_usuario)
        ##self.add_button.pack()

        self.view_button = tk.Button(self.root, text="Visualizar Usuários", command=self._listar_usuarios)
        self.view_button.pack()
       

    def update_video(self):
        ret, frame = self.cap.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            tk_image = ImageTk.PhotoImage(image=image)
            self.video_label.configure(image=tk_image)
            self.video_label.image = tk_image
            

            

        self.root.after(30, self.update_video)

    def _adicionar_usuario(self):
        nome = self.name_entry.get()
        caminho_foto = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        
        if not nome or not caminho_foto:
            messagebox.showerror("Erro", "Nome ou caminho da foto não fornecidos")
            return
        
        cond, rosto_encodings = self._reconhecimento_facial.carrega_face(caminho_foto)
        
        if cond:
            usuario = Usuario(nome, rosto_encodings)
            self._banco_de_dados._inserir_usuario(usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso")
        else:
            messagebox.showerror("Erro", "Não foi possível carregar o rosto da foto")
        
    def _listar_usuarios(self):
        usuarios = self._banco_de_dados.retorna_usuarios()
        lista_usuarios = "\n".join([f"{usuario._nome}" for usuario in usuarios])
        messagebox.showinfo("Usuários", lista_usuarios)
        
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self._banco_de_dados._fechar_conexao()

def main():
    root = tk.Tk()
    app = PontoEletronico(root)
    root.mainloop()

if __name__ == "__main__":
    main()
