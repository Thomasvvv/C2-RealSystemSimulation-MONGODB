"""
TESTE RÁPIDO - Criar Matéria com Curso Válido
Execute este script após iniciar o servidor Flask
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("="*60)
print("  TESTE: Criar Matéria com ID de Curso")
print("="*60)

# 1. Criar um curso primeiro
print("\n1️⃣  Criando curso de teste...")
course_response = requests.post(
    f"{BASE_URL}/courses",
    json={
        "nome": "Ciência da Computação",
        "carga_horaria_total": 3200
    }
)

print(f"   Status: {course_response.status_code}")
course_result = course_response.json()
print(f"   {json.dumps(course_result, indent=4, ensure_ascii=False)}")

if not course_result.get('success'):
    print("\n⚠️  Pegando curso existente...")
    courses = requests.get(f"{BASE_URL}/courses").json()
    if courses.get('success') and courses.get('data'):
        course_id = courses['data'][0]['id']
        print(f"   Usando curso existente ID: {course_id}")
    else:
        print("❌ Nenhum curso disponível. Crie um curso primeiro.")
        exit(1)
else:
    course_id = course_result['data']['id']
    print(f"   ✅ Curso criado com ID: {course_id}")

# 2. Criar matéria usando o ID do curso
print(f"\n2️⃣  Criando matéria para o curso ID {course_id}...")

subject_response = requests.post(
    f"{BASE_URL}/subjects",
    json={
        "id_curso": course_id,  # Pode ser int ou string
        "periodo": 1,
        "nome": "Programação Orientada a Objetos",
        "carga_horaria": 80
    }
)

print(f"   Status: {subject_response.status_code}")
subject_result = subject_response.json()
print(f"   {json.dumps(subject_result, indent=4, ensure_ascii=False)}")

if subject_result.get('success'):
    print("\n✅ SUCESSO! A matéria foi criada corretamente!")
    print(f"   ID da Matéria: {subject_result['data']['id_materia']}")
    print(f"   ID do Curso: {subject_result['data']['id_curso']}")
else:
    print(f"\n❌ ERRO: {subject_result.get('message')}")

# 3. Testar com ID inválido
print(f"\n3️⃣  Testando validação com ID de curso INVÁLIDO (999)...")

invalid_response = requests.post(
    f"{BASE_URL}/subjects",
    json={
        "id_curso": 999,
        "periodo": 2,
        "nome": "Matéria Teste Inválida",
        "carga_horaria": 60
    }
)

print(f"   Status: {invalid_response.status_code}")
invalid_result = invalid_response.json()
print(f"   {json.dumps(invalid_result, indent=4, ensure_ascii=False)}")

if not invalid_result.get('success') and invalid_response.status_code == 404:
    print("\n✅ VALIDAÇÃO OK! Curso inválido foi rejeitado corretamente!")
else:
    print("\n⚠️  A validação deveria ter rejeitado o ID inválido")

print("\n" + "="*60)
print("  TESTE CONCLUÍDO")
print("="*60)
