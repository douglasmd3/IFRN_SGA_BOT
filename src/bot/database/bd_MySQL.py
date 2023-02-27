import sys

import mysql.connector as MSCNT

# import psycopg2 as MSCNT
class bd_singleton_meta(type):

    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class bd_singleton(metaclass=bd_singleton_meta):
    def criar_conexao(self):
        # banco de dados local
        connect = MSCNT.connect(
            user="",
            password="", #TODO: Colocar credenciais no .env
            host="",
            database="",
        )
        # database="dblocal"

        # banco de dados no HEROKU;
        # self.connect = MSCNT.connect(
        #    user="",
        #    password="",
        #    host="",
        #    database=""
        # )
        
        return connect

    def visualizar_sugestoes(self):
        lista_sugestao = []
        self.cnt.execute("select * from sugestao")

        show = self.cnt.cursor().fetchall()
        for linha in show:
            lista_sugestao.append("NOME: %f,MENSAGEM: %f" % (linha[0],linha[1]))
        self.cnt.commit()
        return lista_sugestao

    def gravar_sugestao(self, usuario, sugestao):
        try:
            self.cnt.cursor().execute("insert into sugestao (nome, mensagem) values %(usuario)s, %(sugestao)s",{'usuario':usuario},{'sugestao':sugestao})
            self.cnt.commit()
            print(self.visualizar_sugestoes()[-1])
            sys.stdout.flush()
            return True
        except:
            print("comentário não salvo.")
            return None

    def gravar_n_interacoes(self, n_interacoes):
        # no banco o Quser tem que iniciar com 0 e não estar vazio.
        self.cnt.cursor().execute("update interacao set quantidade_de_interacao = %(n_interacoes)s",{'n_interacoes':n_interacoes})
        self.cnt.commit()

    def gravar_n_usuarios(self, n_usuarios):
        try:
            self.cnt.cursor().execute("update register set quantidade_de_usuario = %(n_usuarios)s",{'n_usuarios':n_usuarios})
            self.cnt.commit()
        except (MSCNT.Error, MSCNT.Warning)  as e:
            print (e)
            self.cnt()

    def gravar_avaliar_bom(self, bom):
        try:
            print(f"AVALIACAO BOA {bom}")
            self.cnt.cursor().execute("update satisfacao set _bom_ = %(bom)s",{'bom':bom}) #TODO: Fazer todas as queries usando este tipo de composicao de string
            print(self.cnt.commit())
        except (MSCNT.Error, MSCNT.Warning) as e:
            print (e)
            self.cnt()

    def gravar_avaliar_ruim(self, ruim):
        try:
            self.cnt.cursor().execute("update satisfacao set _ruim_ = %(ruim)s",{'ruim':ruim})
            self.cnt.commit()
        except (MSCNT.Error, MSCNT.Warning) as e:
            print (e)
            self.cnt()

    def gravar_avaliar_normal(self, normal):
        try:
            self.cnt.cursor().execute("update satisfacao set normal = %(normal)s",{'normal':normal})
            self.cnt.commit()
        except (MSCNT.Error, MSCNT.Warning) as e:
            print (e)
            self.cnt()


    def __init__(self):
        self.cnt = self.criar_conexao()
