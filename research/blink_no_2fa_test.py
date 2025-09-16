"""
Test Blink sans 2FA ou avec solution alternative
"""

import asyncio
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
import requests

async def test_without_2fa():
    """Test après désactivation 2FA"""
    print("=== TEST SANS 2FA ===\n")

    blink = Blink()
    auth = Auth({
        "username": "d.davidfrancois@gmail.com",
        "password": "Dave300945/"
    })
    blink.auth = auth

    print("🔐 Connexion sans 2FA...")

    try:
        await blink.start()

        print("✅ Connexion réussie!")
        print(f"📡 Réseaux: {len(blink.networks)}")

        if blink.networks:
            for name, network in blink.networks.items():
                print(f"\n🏠 Réseau: {name}")
                print(f"   ID: {network.network_id}")
                print(f"   Caméras: {len(network.cameras)}")
                print(f"   Sync Modules: {len(network.sync_modules)}")

                # 🎯 TEST SYNC MODULES
                for sync_name, sync in network.sync_modules.items():
                    print(f"\n   🔄 Sync Module: {sync_name}")
                    print(f"      ID: {sync.sync_id}")
                    print(f"      Status: {sync.status}")

                    # Attributs disponibles
                    attrs = [attr for attr in dir(sync) if not attr.startswith('_')]
                    print(f"      Méthodes: {[a for a in attrs if 'storage' in a.lower() or 'manifest' in a.lower()]}")

                # Caméras
                for cam_name, camera in network.cameras.items():
                    print(f"\n   📹 Caméra: {cam_name}")
                    print(f"      ID: {camera.camera_id}")
                    print(f"      Status: {camera.status}")

        else:
            print("❌ Aucun réseau trouvé")

    except Exception as e:
        print(f"❌ Erreur: {e}")

    finally:
        try:
            await blink.auth.session.close()
        except:
            pass

def test_manual_api():
    """Test API manuel pour debug"""
    print("\n=== TEST API MANUEL ===")

    base_url = "https://rest-prod.immedia-semi.com"

    # Test de base
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Test login endpoint
    login_data = {
        "username": "d.davidfrancois@gmail.com",
        "password": "Dave300945/"
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Blink/3.16.0 (iPhone; iOS 15.0; Scale/2.00)"
    }

    try:
        response = requests.post(
            f"{base_url}/api/v5/account/login",
            json=login_data,
            headers=headers,
            timeout=10
        )
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Token available: {'auth_token' in data}")
        else:
            print(f"Response: {response.text[:200]}")

    except Exception as e:
        print(f"Login failed: {e}")

if __name__ == "__main__":
    print("🎯 SOLUTIONS BLINK_BRIDGE")
    print("\n1. Si 2FA DÉSACTIVÉ:")
    print("   - Testez connexion directe")
    print("\n2. Si 2FA ACTIVÉ:")
    print("   - Désactivez dans app iOS temporairement")
    print("   - Ou utilisez le VRAI code de votre email")
    print()

    # Test sans 2FA
    asyncio.run(test_without_2fa())

    # Test API manuel
    test_manual_api()

    print("\n💡 PROCHAINES ÉTAPES:")
    print("   1. Désactivez 2FA dans app Blink iOS")
    print("   2. Relancez ce test")
    print("   3. Si succès → accès stockage USB possible!")