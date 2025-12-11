"""
Script de test pour vérifier l'accès de l'API à la base de données SQLite.
Ce script teste la connectivité à la base de données et effectue des opérations CRUD.
"""

import requests
import json
import sys
import time

# Configuration
API_URLS = {
    "basic": "http://localhost:5000",
    "with_logging": "http://localhost:5001"
}

def print_section(title):
    """Affiche un séparateur de section"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_database_connection(base_url, api_name):
    """Teste la connexion à la base de données via l'API"""
    print(f"\n🔍 Test de connexion à la base de données via {api_name}")
    
    try:
        # Test health check
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ API {api_name} est en ligne")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Échec du health check: {response.status_code}")
            return False
        
        # Test lecture des livres (teste l'accès BD)
        response = requests.get(f"{base_url}/books", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Accès à la base de données réussi")
            print(f"   Nombre de livres: {data.get('count', 0)}")
            return True
        else:
            print(f"❌ Échec de l'accès à la BD: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_database_crud_operations(base_url, api_name):
    """Teste les opérations CRUD sur la base de données"""
    print(f"\n📝 Test des opérations CRUD via {api_name}")
    
    # 1. CREATE - Ajouter un nouveau livre
    print("\n1️⃣  CREATE - Ajout d'un nouveau livre")
    new_book = {
        "title": "Database Test Book",
        "author": "Test Author",
        "year": 2025
    }
    
    try:
        response = requests.post(f"{base_url}/books", json=new_book, timeout=5)
        if response.status_code == 201:
            created_book = response.json()
            book_id = created_book.get('id')
            print(f"✅ Livre ajouté avec succès - ID: {book_id}")
            print(f"   {json.dumps(created_book, indent=2)}")
        else:
            print(f"❌ Échec de l'ajout: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout: {e}")
        return False
    
    # 2. READ - Lire le livre créé
    print(f"\n2️⃣  READ - Lecture du livre ID: {book_id}")
    try:
        response = requests.get(f"{base_url}/books/{book_id}", timeout=5)
        if response.status_code == 200:
            print(f"✅ Livre lu avec succès")
            print(f"   {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Échec de la lecture: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture: {e}")
        return False
    
    # 3. UPDATE - Mettre à jour le livre
    print(f"\n3️⃣  UPDATE - Mise à jour du livre ID: {book_id}")
    update_data = {
        "title": "Updated Database Test Book",
        "year": 2024
    }
    
    try:
        response = requests.put(f"{base_url}/books/{book_id}", json=update_data, timeout=5)
        if response.status_code == 200:
            updated_book = response.json()
            print(f"✅ Livre mis à jour avec succès")
            print(f"   {json.dumps(updated_book, indent=2)}")
        else:
            print(f"❌ Échec de la mise à jour: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False
    
    # 4. DELETE - Supprimer le livre
    print(f"\n4️⃣  DELETE - Suppression du livre ID: {book_id}")
    try:
        response = requests.delete(f"{base_url}/books/{book_id}", timeout=5)
        if response.status_code == 200:
            print(f"✅ Livre supprimé avec succès")
            print(f"   {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Échec de la suppression: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        return False
    
    # 5. Vérifier que le livre n'existe plus
    print(f"\n5️⃣  VERIFY - Vérification de la suppression")
    try:
        response = requests.get(f"{base_url}/books/{book_id}", timeout=5)
        if response.status_code == 404:
            print(f"✅ Livre correctement supprimé de la BD")
        else:
            print(f"❌ Le livre existe encore: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    
    return True

def test_database_persistence(base_url, api_name):
    """Teste la persistance des données dans la base de données"""
    print(f"\n💾 Test de persistance des données via {api_name}")
    
    # Ajouter un livre de test
    test_book = {
        "title": "Persistence Test Book",
        "author": "Persistence Tester",
        "year": 2025
    }
    
    try:
        # Créer le livre
        response = requests.post(f"{base_url}/books", json=test_book, timeout=5)
        if response.status_code == 201:
            book_id = response.json().get('id')
            print(f"✅ Livre de test créé - ID: {book_id}")
        else:
            print(f"❌ Échec de la création du livre de test")
            return False
        
        # Compter les livres actuels
        response = requests.get(f"{base_url}/books", timeout=5)
        initial_count = response.json().get('count', 0)
        print(f"📊 Nombre de livres actuel: {initial_count}")
        
        # Attendre un peu
        time.sleep(1)
        
        # Vérifier que le livre existe toujours
        response = requests.get(f"{base_url}/books/{book_id}", timeout=5)
        if response.status_code == 200:
            print(f"✅ Les données persistent dans la base SQLite")
            return True
        else:
            print(f"❌ Les données ne persistent pas")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de persistance: {e}")
        return False

def main():
    """Fonction principale"""
    print_section("🚀 TEST D'ACCÈS À LA BASE DE DONNÉES SQLite")
    
    print("\n📌 Ce script teste:")
    print("   1. La connexion à la base de données via l'API")
    print("   2. Les opérations CRUD (Create, Read, Update, Delete)")
    print("   3. La persistance des données")
    
    # Sélectionner l'API à tester
    print("\n🔧 APIs disponibles:")
    print("   1. API basique (port 5000)")
    print("   2. API avec logging (port 5001)")
    print("   3. Les deux")
    
    choice = input("\nChoisissez une option (1/2/3) [défaut: 3]: ").strip()
    
    apis_to_test = []
    if choice == "1":
        apis_to_test = [("basic", API_URLS["basic"])]
    elif choice == "2":
        apis_to_test = [("with_logging", API_URLS["with_logging"])]
    else:
        apis_to_test = [("basic", API_URLS["basic"]), ("with_logging", API_URLS["with_logging"])]
    
    results = {}
    
    for api_name, base_url in apis_to_test:
        print_section(f"TEST DE L'API: {api_name.upper()}")
        
        # Test 1: Connexion
        conn_result = test_database_connection(base_url, api_name)
        
        if conn_result:
            # Test 2: Opérations CRUD
            crud_result = test_database_crud_operations(base_url, api_name)
            
            # Test 3: Persistance
            persist_result = test_database_persistence(base_url, api_name)
            
            results[api_name] = {
                "connection": conn_result,
                "crud": crud_result,
                "persistence": persist_result
            }
        else:
            results[api_name] = {
                "connection": False,
                "crud": False,
                "persistence": False
            }
    
    # Résumé final
    print_section("📊 RÉSUMÉ DES TESTS")
    
    all_passed = True
    for api_name, tests in results.items():
        print(f"\n🔸 {api_name.upper()}:")
        print(f"   Connexion BD:  {'✅' if tests['connection'] else '❌'}")
        print(f"   Opérations CRUD: {'✅' if tests['crud'] else '❌'}")
        print(f"   Persistance:   {'✅' if tests['persistence'] else '❌'}")
        
        if not all(tests.values()):
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ TOUS LES TESTS SONT PASSÉS!")
        print("La base de données SQLite fonctionne correctement avec l'API.")
        sys.exit(0)
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez que les conteneurs Docker sont en cours d'exécution:")
        print("   docker-compose up -d")
        sys.exit(1)

if __name__ == "__main__":
    main()
