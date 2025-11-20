import pymongo
from urllib.parse import quote_plus
import os

class MongoQueries:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoQueries, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.host = "localhost"
        self.port = 27017
        self.service_name = 'labdatabase'

        auth_file = os.path.join("backend", "db", "conexion", "passphrase", "authentication.mongo")
        if os.path.exists(auth_file):
            with open(auth_file, "r") as f:
                self.user, self.passwd = f.read().split(',')
        else:
            # Fallback para variáveis de ambiente
            self.user = os.getenv('MONGO_USER', 'labdatabase')
            self.passwd = os.getenv('MONGO_PASS', 'lab@Database2025')
        
        self._initialized = True

    def connect(self):
        if MongoQueries._client is None:
            MongoQueries._client = pymongo.MongoClient(
                f"mongodb://{self.user}:{quote_plus(self.passwd)}@{self.host}:{self.port}/"
            )
        return MongoQueries._client[self.service_name]

    def close(self):
        if MongoQueries._client is not None:
            MongoQueries._client.close()
            MongoQueries._client = None

def get_connection():
    mongo = MongoQueries()
    return mongo.connect()

def release_connection(conn):
    # Para MongoDB, não fechamos a conexão a cada chamada
    # O pool de conexões do pymongo gerencia isso automaticamente
    pass

def connect():
    mongo = MongoQueries()
    return mongo.connect()

def close():
    # Para MongoDB, NÃO fechamos a conexão após cada requisição
    # O pool de conexões do pymongo gerencia isso automaticamente
    # Isso evita fechar a conexão compartilhada entre requisições
    pass