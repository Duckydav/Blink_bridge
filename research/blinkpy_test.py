"""
Test basique blinkpy pour Blink_bridge
⚠️ MODIFIEZ VOS CREDENTIALS AVANT EXÉCUTION !
"""

try:
    from blinkpy.blinkpy import Blink
    from blinkpy.auth import Auth
    import json

    def test_blink_connection():
        print("=== Test connexion Blink avec blinkpy ===\n")

        # Configuration
        blink = Blink()

        # ⚠️ ATTENTION: Remplacez par vos vraies credentials
        auth = Auth({
            "username": "d.davidfrancois@gmail.com",  # ⚠️ À modifier
            "password": "CuN8lOH6Sudk_Iin"        # ⚠️ À modifier
        })

        blink.auth = auth

        print("Tentative de connexion...")

        try:
            # Connexion
            blink.start()

            print("✅ Connexion réussie!")
            print(f"Réseaux trouvés: {len(blink.networks)}")

            # Lister les réseaux
            for network_name, network in blink.networks.items():
                print(f"\n📡 Réseau: {network_name}")
                print(f"   - ID: {network.network_id}")
                print(f"   - Statut: {'Armé' if network.arm else 'Désarmé'}")

                # Sync modules
                for sync_name, sync in network.sync_modules.items():
                    print(f"   🔄 Sync Module: {sync_name}")
                    print(f"      - ID: {sync.sync_id}")
                    print(f"      - Status: {sync.status}")

                    # Check local storage
                    if hasattr(sync, 'local_storage'):
                        print(f"      - Stockage local: {sync.local_storage}")

                # Caméras
                for camera_name, camera in network.cameras.items():
                    print(f"   📹 Caméra: {camera_name}")
                    print(f"      - ID: {camera.camera_id}")
                    print(f"      - Status: {camera.status}")
                    print(f"      - Batterie: {camera.battery}")

                    # Test thumbnail
                    try:
                        camera.snap_picture()
                        print(f"      - Thumbnail: Disponible")
                    except Exception as e:
                        print(f"      - Thumbnail: Erreur ({e})")

            # Test accès stockage local
            print("\n💾 Test accès stockage local...")
            try:
                for network_name, network in blink.networks.items():
                    for sync_name, sync in network.sync_modules.items():
                        manifest = sync.get_local_storage_manifest()
                        if manifest:
                            print(f"   ✅ Manifeste récupéré pour {sync_name}")
                            clips = manifest.get('clips', [])
                            print(f"   📹 {len(clips)} clips trouvés")

                            # Lister quelques clips
                            for i, clip in enumerate(clips[:3]):
                                print(f"      Clip {i+1}: {clip.get('name', 'unknown')}")
                        else:
                            print(f"   ❌ Pas de manifeste pour {sync_name}")
            except Exception as e:
                print(f"   ❌ Erreur stockage local: {e}")

        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            print("\n💡 Vérifiez:")
            print("   - Credentials corrects")
            print("   - Connexion internet")
            print("   - App mobile fonctionne")
            print("   - 2FA désactivé ou géré")

    def test_api_endpoints():
        """Test des endpoints API directement"""
        import requests

        print("\n=== Test endpoints API directs ===")

        base_url = "https://rest-prod.immedia-semi.com"

        # Test login endpoint
        login_url = f"{base_url}/api/v5/account/login"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "BlinkMobile_Android"
        }

        print(f"Test endpoint login: {login_url}")

        try:
            # Test simple de connectivité (sans credentials)
            response = requests.get(login_url, headers=headers, timeout=5)
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
        except Exception as e:
            print(f"   Erreur: {e}")

    if __name__ == "__main__":
        print("🚀 Démarrage tests Blink_bridge...\n")

        # Test 1: Connexion via blinkpy
        test_blink_connection()

        # Test 2: API endpoints directs
        test_api_endpoints()

        print("\n📝 Notes importantes:")
        print("   - Modifiez les credentials dans ce script")
        print("   - Le stockage local est la clé pour accéder à l'USB")
        print("   - 2FA peut compliquer l'automatisation")

except ImportError:
    print("❌ blinkpy non installé")
    print("Installation:")
    print("   pip install blinkpy")
    print("   pip install requests")