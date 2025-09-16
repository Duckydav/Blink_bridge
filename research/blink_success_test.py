"""
Test Blink SUCCÈS - Version corrigée pour accès stockage local
"""

import asyncio
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth

async def test_blink_success():
    print("=== BLINK_BRIDGE - TEST FINAL ===\n")

    blink = Blink()
    auth = Auth({
        "username": "d.davidfrancois@gmail.com",
        "password": "Dave300945/"
    })
    blink.auth = auth

    print("🔐 Connexion à Blink...")
    print("📱 Code SMS sera demandé...")

    try:
        await blink.start()

        print("✅ CONNEXION RÉUSSIE!")
        print(f"📡 Réseaux détectés: {len(blink.networks)}")

        if not blink.networks:
            print("❌ Aucun réseau trouvé")
            return

        # Parcourir les réseaux avec gestion d'erreur
        for network_name, network_data in blink.networks.items():
            print(f"\n🏠 Réseau: {network_name}")

            # Vérifier le type de données
            if isinstance(network_data, dict):
                print("   Type: dictionnaire")
                print(f"   Clés: {list(network_data.keys())}")

                # Rechercher ID réseau
                network_id = network_data.get('network_id') or network_data.get('id') or network_name
                print(f"   ID: {network_id}")

                # Sync modules
                sync_modules = network_data.get('sync_modules', {})
                print(f"   🔄 Sync Modules: {len(sync_modules)}")

                for sync_name, sync_data in sync_modules.items():
                    print(f"      - {sync_name}")
                    if isinstance(sync_data, dict):
                        print(f"        ID: {sync_data.get('id', 'unknown')}")
                        print(f"        Status: {sync_data.get('status', 'unknown')}")
                    else:
                        print(f"        Status: {getattr(sync_data, 'status', 'unknown')}")

                # Caméras
                cameras = network_data.get('cameras', {})
                print(f"   📹 Caméras: {len(cameras)}")

                for cam_name, cam_data in cameras.items():
                    print(f"      - {cam_name}")
                    if isinstance(cam_data, dict):
                        print(f"        ID: {cam_data.get('id', 'unknown')}")
                        print(f"        Status: {cam_data.get('status', 'unknown')}")

            else:
                # Format objet (ancien)
                print("   Type: objet")
                print(f"   ID: {getattr(network_data, 'network_id', 'unknown')}")

                sync_modules = getattr(network_data, 'sync_modules', {})
                print(f"   🔄 Sync Modules: {len(sync_modules)}")

                for sync_name, sync in sync_modules.items():
                    print(f"      - {sync_name} (ID: {sync.sync_id})")
                    print(f"        Status: {sync.status}")

                cameras = getattr(network_data, 'cameras', {})
                print(f"   📹 Caméras: {len(cameras)}")

        # 🎯 TEST STOCKAGE LOCAL AVANCÉ
        print("\n💾 🎯 TEST ACCÈS STOCKAGE LOCAL:")

        # Accès via l'objet blink principal
        print("   Méthodes blink disponibles:")
        blink_methods = [method for method in dir(blink) if 'storage' in method.lower() or 'sync' in method.lower()]
        print(f"      {blink_methods}")

        # Test via sync modules
        for network_name, network_data in blink.networks.items():
            print(f"\n   📡 Test stockage pour réseau: {network_name}")

            # Gérer les deux formats
            if isinstance(network_data, dict):
                sync_modules = network_data.get('sync_modules', {})
            else:
                sync_modules = getattr(network_data, 'sync_modules', {})

            for sync_name, sync_obj in sync_modules.items():
                print(f"      🔄 Test {sync_name}...")

                # Lister toutes les méthodes disponibles
                if hasattr(sync_obj, '__dict__'):
                    methods = [m for m in dir(sync_obj) if not m.startswith('_')]
                    storage_methods = [m for m in methods if 'storage' in m.lower() or 'manifest' in m.lower() or 'clip' in m.lower()]
                    print(f"         Méthodes stockage: {storage_methods}")

                    # Tester chaque méthode
                    for method in storage_methods:
                        try:
                            func = getattr(sync_obj, method)
                            print(f"         Tentative {method}...")

                            if callable(func):
                                if asyncio.iscoroutinefunction(func):
                                    result = await func()
                                else:
                                    result = func()

                                print(f"         ✅ {method} réussi!")
                                print(f"            Type: {type(result)}")
                                print(f"            Contenu: {str(result)[:200]}...")

                                # Si c'est un manifeste avec clips
                                if isinstance(result, dict) and 'clips' in result:
                                    clips = result['clips']
                                    print(f"         🎬 {len(clips)} CLIPS USB TROUVÉS!")

                                    for i, clip in enumerate(clips[:3]):
                                        print(f"            Clip {i+1}:")
                                        print(f"               Nom: {clip.get('name', 'unknown')}")
                                        print(f"               Taille: {clip.get('size', 'unknown')}")
                                        print(f"               Date: {clip.get('created_at', 'unknown')}")

                                break  # Une méthode qui marche suffit

                        except Exception as e:
                            print(f"         ❌ {method}: {e}")

        print("\n🎯 RÉSUMÉ:")
        print("   ✅ Connexion Blink établie")
        print("   ✅ Réseaux détectés")
        print("   ✅ Sync modules identifiés")
        print("   🎯 Prêt pour accès stockage USB!")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            await blink.auth.session.close()
        except:
            pass

if __name__ == "__main__":
    print("🚀 BLINK_BRIDGE - VERSION FINALE")
    print("📱 Préparez votre téléphone pour le code SMS...")
    print()

    asyncio.run(test_blink_success())