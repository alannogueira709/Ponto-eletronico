import sqlite3
import json
from usuario import Usuario
from pathlib import Path
import io
import numpy as np


class Banco_de_dados:
    
    def __init__(self):
        ROOT_DIR = Path(__file__).parent
        DB_NAME = 'banco_de_dados.sqlite3'
        DB_FILE = ROOT_DIR / DB_NAME
        self._tabela_nome = 'usuarios'
        self._connection = sqlite3.connect(DB_FILE)
        self._cursor = self._connection.cursor()
        self._criar_tabela()
        
    def converte_em_texto(self, array):
        out = io.BytesIO()
        np.save(out, array)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def converter_em_array(self, texto):
        out = io.BytesIO(texto)
        out.seek(0)
        return np.load(out)

    def _criar_tabela(self):
        self._cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self._tabela_nome}'
            '('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'nome TEXT,'
            'encoding TEXT'
            ')'
        )
        
        self._connection.commit()
        
    def _inserir_usuario(self, usuario):
        # Converte a lista de listas de números para uma string JSON
        print(type(usuario._encoding[0]))
        string = self.converte_em_texto(usuario._encoding[0]) # alterei coloquei o 0
        self._cursor.execute(    
            f'INSERT INTO {self._tabela_nome} '
            '(nome, encoding) '
            'VALUES (?, ?)', (usuario._nome, string))
        self._connection.commit()
        
    def retorna_usuarios(self):
        # pegar todos os dados da tabela
        usuarios = []
        self._cursor.execute(f'SELECT * FROM {self._tabela_nome}')
        for linha in self._cursor.fetchall():
            _id, nome, encoding_bd = linha
            # Converte a string JSON de volta para uma lista de listas
            encoding = self.converter_em_array(encoding_bd)
            usuarios.append(Usuario(nome, encoding))
        return usuarios
        
    def _fechar_conexao(self):
        self._cursor.close()
        self._connection.close()
