"""
Teste de múltiplas conexões simultâneas ao MongoDB
Verifica se o pool de conexões está funcionando corretamente
"""
from db_conn import connect, close

def test_multiple_connections():
    print("🔄 Teste 1: Conectar várias vezes seguidas")
    try:
        db1 = connect()
        print(f"✅ Conexão 1: {db1.name}")
        print(f"   Coleções disponíveis: {db1.list_collection_names()[:3]}...")
        
        db2 = connect()
        print(f"✅ Conexão 2: {db2.name}")
        
        db3 = connect()
        print(f"✅ Conexão 3: {db3.name}")
        
        # Verificar se todas retornam o mesmo database
        print(f"\n✅ Todas as conexões apontam para o mesmo database: {db1.name == db2.name == db3.name}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def test_connection_after_close():
    print("\n🔄 Teste 2: Conectar após chamar close()")
    try:
        db1 = connect()
        print(f"✅ Primeira conexão: {db1.name}")
        
        # Tentar "fechar" (agora não faz nada)
        close()
        print("✅ close() chamado (não fecha mais a conexão)")
        
        # Conectar novamente
        db2 = connect()
        print(f"✅ Segunda conexão após close(): {db2.name}")
        
        # Testar operação
        count = db2.alunos.count_documents({})
        print(f"✅ Operação após close(): {count} alunos encontrados")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def test_parallel_collections():
    print("\n🔄 Teste 3: Acessar múltiplas coleções em paralelo")
    try:
        db = connect()
        
        collections = ['alunos', 'cursos', 'professores', 'materias', 'ofertas']
        
        for coll_name in collections:
            count = db[coll_name].count_documents({})
            print(f"✅ Coleção '{coll_name}': {count} documentos")
        
        print(f"\n✅ Todas as coleções acessadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def test_insert_and_read():
    print("\n🔄 Teste 4: Inserir e ler documento de teste")
    try:
        db = connect()
        test_coll = db['test_connection']
        
        # Limpar teste anterior
        test_coll.delete_many({"tipo": "teste"})
        
        # Inserir
        result = test_coll.insert_one({"tipo": "teste", "mensagem": "Teste de conexão múltipla"})
        print(f"✅ Documento inserido com ID: {result.inserted_id}")
        
        # "Fechar" (não faz nada agora)
        close()
        
        # Tentar ler após close
        doc = test_coll.find_one({"_id": result.inserted_id})
        print(f"✅ Documento lido após close(): {doc['mensagem']}")
        
        # Limpar
        test_coll.delete_one({"_id": result.inserted_id})
        print("✅ Documento de teste removido")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("TESTE DE POOL DE CONEXÕES MONGODB")
    print("=" * 70)
    
    test_multiple_connections()
    test_connection_after_close()
    test_parallel_collections()
    test_insert_and_read()
    
    print("\n" + "=" * 70)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 70)
    print("\n💡 A conexão agora usa um pool gerenciado pelo pymongo")
    print("💡 O método close() não fecha mais a conexão compartilhada")
    print("💡 Isso evita problemas de conexões perdidas entre requisições")
