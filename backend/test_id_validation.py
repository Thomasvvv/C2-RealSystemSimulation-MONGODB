"""
Script para testar a validação de IDs e relacionamentos entre entidades
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_create_course():
    print_section("TESTE 1: Criar Curso")
    
    course_data = {
        "nome": "Engenharia de Software",
        "carga_horaria_total": 3600
    }
    
    response = requests.post(f"{BASE_URL}/courses", json=course_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get('success'):
        return result['data']['id']
    return None

def test_create_subject_with_valid_course(course_id):
    print_section(f"TESTE 2: Criar Matéria com ID de Curso VÁLIDO ({course_id})")
    
    # Testar com diferentes tipos de entrada
    test_cases = [
        {"tipo": "ID como inteiro", "id_curso": course_id},
        {"tipo": "ID como string", "id_curso": str(course_id)},
    ]
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n  Caso {idx}: {test_case['tipo']}")
        
        subject_data = {
            "id_curso": test_case["id_curso"],
            "periodo": 1,
            "nome": f"Algoritmos e Estruturas de Dados {idx}",
            "carga_horaria": 80
        }
        
        response = requests.post(f"{BASE_URL}/subjects", json=subject_data)
        print(f"  Status: {response.status_code}")
        result = response.json()
        print(f"  Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('success'):
            print(f"  ✅ Sucesso! id_materia={result['data']['id_materia']}")
        else:
            print(f"  ❌ Falhou: {result.get('message')}")

def test_create_subject_with_invalid_course():
    print_section("TESTE 3: Criar Matéria com ID de Curso INVÁLIDO (999)")
    
    subject_data = {
        "id_curso": 999,  # ID que não existe
        "periodo": 1,
        "nome": "Matéria Teste Inválida",
        "carga_horaria": 60
    }
    
    response = requests.post(f"{BASE_URL}/subjects", json=subject_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if not result.get('success'):
        print(f"✅ Validação funcionou corretamente: {result.get('message')}")
    else:
        print(f"❌ ERRO: Deveria ter rejeitado o ID de curso inválido!")

def test_create_subject_with_invalid_type():
    print_section("TESTE 4: Criar Matéria com ID de Curso tipo INVÁLIDO")
    
    test_cases = [
        {"tipo": "String não numérica", "id_curso": "abc"},
        {"tipo": "Null", "id_curso": None},
        {"tipo": "Objeto", "id_curso": {"id": 1}},
    ]
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n  Caso {idx}: {test_case['tipo']}")
        
        subject_data = {
            "id_curso": test_case["id_curso"],
            "periodo": 1,
            "nome": "Matéria Teste",
            "carga_horaria": 60
        }
        
        try:
            response = requests.post(f"{BASE_URL}/subjects", json=subject_data)
            print(f"  Status: {response.status_code}")
            result = response.json()
            print(f"  Resposta: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if not result.get('success'):
                print(f"  ✅ Validação funcionou: {result.get('message')}")
            else:
                print(f"  ❌ ERRO: Deveria ter rejeitado!")
        except Exception as e:
            print(f"  ⚠️ Exceção: {e}")

def test_list_subjects():
    print_section("TESTE 5: Listar Matérias")
    
    response = requests.get(f"{BASE_URL}/subjects")
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get('success'):
        subjects = result.get('data', [])
        print(f"Total de matérias: {len(subjects)}")
        for subject in subjects[:3]:  # Mostrar apenas as 3 primeiras
            print(f"  - {subject['nome']} (Curso: {subject.get('curso_nome', 'N/A')})")
    else:
        print(f"Erro: {result}")

def test_course_type_consistency():
    print_section("TESTE 6: Verificar Consistência de Tipos no Banco")
    
    response = requests.get(f"{BASE_URL}/courses")
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            courses = result.get('data', [])
            if courses:
                first_course = courses[0]
                print(f"Curso exemplo: {first_course['nome']}")
                print(f"  ID: {first_course['id']} (tipo: {type(first_course['id']).__name__})")
                
                if isinstance(first_course['id'], int):
                    print(f"  ✅ ID está armazenado como inteiro")
                else:
                    print(f"  ⚠️ ID está armazenado como {type(first_course['id']).__name__}")

if __name__ == "__main__":
    print("="*70)
    print("  TESTE DE VALIDAÇÃO DE IDs E RELACIONAMENTOS")
    print("="*70)
    print("\n⚠️ CERTIFIQUE-SE DE QUE O SERVIDOR ESTÁ RODANDO EM http://localhost:5000")
    
    input("\nPressione ENTER para continuar...")
    
    try:
        # Criar um curso para testar
        course_id = test_create_course()
        
        if course_id:
            # Testar criação de matéria com curso válido
            test_create_subject_with_valid_course(course_id)
        else:
            print("\n⚠️ Não foi possível criar curso. Verifique se há cursos no banco.")
            # Tentar pegar ID de curso existente
            response = requests.get(f"{BASE_URL}/courses")
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('data'):
                    course_id = result['data'][0]['id']
                    print(f"✅ Usando curso existente: ID {course_id}")
                    test_create_subject_with_valid_course(course_id)
        
        # Testar com ID inválido
        test_create_subject_with_invalid_course()
        
        # Testar com tipos inválidos
        test_create_subject_with_invalid_type()
        
        # Listar matérias
        test_list_subjects()
        
        # Verificar consistência de tipos
        test_course_type_consistency()
        
        print("\n" + "="*70)
        print("  ✅ TODOS OS TESTES CONCLUÍDOS")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao servidor")
        print("   Certifique-se de que o Flask está rodando em http://localhost:5000")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
