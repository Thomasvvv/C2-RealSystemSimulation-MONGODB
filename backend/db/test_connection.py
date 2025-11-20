from db_conn import get_connection, release_connection

try:
    # Conecta ao MongoDB
    db = get_connection()
    print("✅ Conexão estabelecida com sucesso!")
    
    # Lista todas as coleções
    collections = db.list_collection_names()
    print(f"📁 Coleções disponíveis: {collections if collections else 'Nenhuma coleção ainda'}")
    
    # Testa uma operação simples
    print(f"🗄️  Database: {db.name}")
    
    # Testa inserção e leitura em uma coleção de teste
    test_collection = db['test_connection']
    test_doc = {"mensagem": "Teste de conexão", "timestamp": "2025-11-20"}
    result = test_collection.insert_one(test_doc)
    print(f"📝 Documento de teste inserido com ID: {result.inserted_id}")
    
    # Lê o documento
    doc = test_collection.find_one({"_id": result.inserted_id})
    print(f"📖 Documento lido: {doc}")
    
    # Remove o documento de teste
    test_collection.delete_one({"_id": result.inserted_id})
    print("🗑️  Documento de teste removido")
    
    release_connection(db)
    print("✅ Teste concluído com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    import traceback
    traceback.print_exc()
