"""
Diagnostic approfondi - Pourquoi pas de devices ?
"""

import asyncio
import requests
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth

async def debug_missing_devices():
    print("=== DIAGNOSTIC DEVICES MANQUANTS ===\n")

    blink = Blink()
    auth = Auth({
        "username": "d.davidfrancois@gmail.com",
        "password": "Dave300945/"
    })
    blink.auth = auth

    print("🔐 Connexion pour diagnostic...")

    try:
        await blink.start()

        print("✅ Connexion établie")

        # 1. Vérifier les tokens
        print(f"\n🔑 Token info:")
        if hasattr(blink.auth, 'token'):
            print(f"   Token présent: {bool(blink.auth.token)}")
            print(f"   Token type: {type(blink.auth.token)}")

        # 2. Vérifier les méthodes blink
        print(f"\n🔧 Méthodes blink:")
        methods = [m for m in dir(blink) if not m.startswith('_')]
        important_methods = [m for m in methods if any(word in m.lower() for word in ['sync', 'camera', 'device', 'refresh', 'update'])]
        print(f"   Méthodes importantes: {important_methods}")

        # 3. Forcer refresh/update
        refresh_methods = ['refresh', 'update', 'setup_sync_module']
        for method in refresh_methods:
            if hasattr(blink, method):
                try:
                    print(f"   Tentative {method}...")
                    func = getattr(blink, method)
                    if asyncio.iscoroutinefunction(func):
                        await func()
                    else:
                        func()
                    print(f"   ✅ {method} réussi")
                except Exception as e:
                    print(f"   ❌ {method}: {e}")

        # 4. Re-vérifier après refresh
        print(f"\n📡 Après refresh:")
        print(f"   Réseaux: {len(blink.networks)}")
        for name, net in blink.networks.items():
            print(f"   Réseau {name}: {net}")

        # 5. Accès API direct pour comparaison
        print(f"\n🌐 Test API direct:")
        await test_direct_api(blink.auth.token if hasattr(blink.auth, 'token') else None)

    except Exception as e:
        print(f"❌ Erreur diagnostic: {e}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            await blink.auth.session.close()
        except:
            pass

async def test_direct_api(token):
    """Test API direct avec token récupéré"""

    if not token:
        print("   ❌ Pas de token disponible")
        return

    base_url = "https://rest-u056.immedia-semi.com"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Blink/3.16.0 (iPhone; iOS 15.0; Scale/2.00)"
    }

    # Test endpoints
    endpoints = [
        "/api/v1/networks",
        "/api/v1/account/sync_modules",
        "/api/v3/accounts/392166/homescreen",
        "/api/v1/network/586048/sync_modules",
        "/api/v1/network/586048/cameras"
    ]

    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"   Test: {endpoint}")

            response = requests.get(url, headers=headers, timeout=10)
            print(f"      Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"      Données: {type(data)} - {str(data)[:100]}...")

                # Analyser les données importantes
                if 'sync_modules' in str(data):
                    print(f"      🎯 SYNC MODULES TROUVÉS!")
                if 'cameras' in str(data):
                    print(f"      🎯 CAMÉRAS TROUVÉES!")

            else:
                print(f"      Erreur: {response.text[:100]}")

        except Exception as e:
            print(f"      ❌ {endpoint}: {e}")

def verify_app_blink():
    """Vérifications à faire dans l'app Blink"""
    print("\n📱 VÉRIFICATIONS APP BLINK:")
    print("   1. Ouvrez l'app Blink sur votre iPhone")
    print("   2. Vérifiez que vous voyez:")
    print("      - Vos 2 sonnettes")
    print("      - Votre Sync Module 2")
    print("      - Statut 'En ligne' pour tous")
    print("   3. Vérifiez les permissions:")
    print("      - Compte → Partage → Pas de restrictions")
    print("      - Tous les devices bien associés au compte principal")
    print("   4. Test clé USB:")
    print("      - Paramètres Sync Module → Stockage local")
    print("      - Vérifiez que la clé USB est détectée")

if __name__ == "__main__":
    print("🚀 DIAGNOSTIC COMPLET BLINK_BRIDGE\n")

    # Vérifications préliminaires
    verify_app_blink()

    # Test diagnostic
    asyncio.run(debug_missing_devices())

    print("\n💡 SOLUTIONS POSSIBLES:")
    print("   1. Compte limité/secondaire → Utiliser compte principal")
    print("   2. Devices non associés → Re-setup dans app Blink")
    print("   3. API version différente → Tester endpoints alternatifs")
    print("   4. blinkpy obsolète → Mettre à jour ou API directe")