"""
Test blinkpy CORRIGÉ pour Blink_bridge
Version async/await compatible
"""

import asyncio
try:
    from blinkpy.blinkpy import Blink
    from blinkpy.auth import Auth
    import json

    async def test_blink_connection_async():
        print("=== Test connexion Blink avec blinkpy (ASYNC) ===\n")

        # Configuration
        blink = Blink()

        # Credentials (déjà configurés)
        auth = Auth({
            "username": "d.davidfrancois@gmail.com",
            "password": "CuN8lOH6Sudk_Iin"
        })

        blink.auth = auth

        print("Tentative de connexion...")

        try:
            # Connexion ASYNC
            await blink.start()

            print("✅ Connexion réussie!")
            print(f"Réseaux trouvés: {len(blink.networks)}")

            if not blink.networks:
                print("❌ Aucun réseau trouvé. Vérifiez:")
                print("   - Credentials corrects")
                print("   - 2FA désactivé")
                print("   - Compte actif")
                return

            # Lister les réseaux
            for network_name, network in blink.networks.items():
                print(f"\n📡 Réseau: {network_name}")
                print(f"   - ID: {network.network_id}")
                print(f"   - Statut: {'Armé' if network.arm else 'Désarmé'}")

                # Sync modules
                print(f"   - Sync Modules: {len(network.sync_modules)}")
                for sync_name, sync in network.sync_modules.items():
                    print(f"   🔄 Sync Module: {sync_name}")
                    print(f"      - ID: {sync.sync_id}")
                    print(f"      - Status: {sync.status}")

                    # Check attributs disponibles
                    print(f"      - Attributs: {[attr for attr in dir(sync) if not attr.startswith('_')]}")

                # Caméras
                print(f"   - Caméras: {len(network.cameras)}")
                for camera_name, camera in network.cameras.items():
                    print(f"   📹 Caméra: {camera_name}")
                    print(f"      - ID: {camera.camera_id}")
                    print(f"      - Status: {camera.status}")

                    # Attributs battery si disponible
                    if hasattr(camera, 'battery'):
                        print(f"      - Batterie: {camera.battery}")

            # Test accès stockage local avec méthodes disponibles
            print("\n💾 Test accès stockage local...")
            try:
                for network_name, network in blink.networks.items():
                    for sync_name, sync in network.sync_modules.items():
                        print(f"   Tentative pour {sync_name}...")

                        # Essayer différentes méthodes
                        methods_to_try = [
                            'get_local_storage_manifest',
                            'local_storage_manifest',
                            'get_manifest',
                            'manifest'
                        ]

                        manifest = None
                        for method in methods_to_try:
                            if hasattr(sync, method):
                                try:
                                    print(f"      Essai méthode: {method}")
                                    func = getattr(sync, method)
                                    if asyncio.iscoroutinefunction(func):
                                        manifest = await func()
                                    else:
                                        manifest = func()

                                    if manifest:
                                        print(f"      ✅ Méthode {method} réussie!")
                                        break
                                except Exception as e:
                                    print(f"      ❌ Méthode {method}: {e}")

                        if manifest:
                            print(f"   ✅ Manifeste récupéré pour {sync_name}")
                            print(f"   Type: {type(manifest)}")
                            print(f"   Contenu: {manifest}")

                            if isinstance(manifest, dict):
                                clips = manifest.get('clips', [])
                                print(f"   📹 {len(clips)} clips trouvés")

                                # Lister quelques clips
                                for i, clip in enumerate(clips[:3]):
                                    print(f"      Clip {i+1}: {clip}")
                        else:
                            print(f"   ❌ Pas de manifeste accessible pour {sync_name}")

            except Exception as e:
                print(f"   ❌ Erreur stockage local: {e}")

        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            print(f"Type erreur: {type(e)}")
            print("\n💡 Solutions possibles:")
            print("   - Vérifier credentials")
            print("   - Désactiver 2FA temporairement")
            print("   - Vérifier que l'app mobile fonctionne")
            print("   - Essayer différents endpoints")

        finally:
            # Fermer proprement
            try:
                await blink.auth.session.close()
            except:
                pass

    def test_blinkpy_info():
        """Affiche des infos sur blinkpy"""
        print("\n=== Info blinkpy ===")
        try:
            import blinkpy
            print(f"Version blinkpy: {blinkpy.__version__}")
        except:
            print("Version blinkpy non disponible")

        # Tester importation des modules
        modules = ['blinkpy.blinkpy', 'blinkpy.auth', 'blinkpy.sync_wireless']
        for module in modules:
            try:
                __import__(module)
                print(f"✅ Module {module} disponible")
            except Exception as e:
                print(f"❌ Module {module}: {e}")

    async def main():
        print("🚀 Démarrage tests Blink_bridge (VERSION CORRIGÉE)...\n")

        # Info blinkpy
        test_blinkpy_info()

        # Test connexion
        await test_blink_connection_async()

        print("\n📝 Notes:")
        print("   - Version async/await utilisée")
        print("   - Test des différentes méthodes de stockage local")
        print("   - Affichage des attributs disponibles")

    if __name__ == "__main__":
        # Lancer en mode async
        asyncio.run(main())

except ImportError as e:
    print("❌ Erreur d'importation:")
    print(f"   {e}")
    print("\nInstallation:")
    print("   pip install blinkpy")
    print("   pip install aiohttp")
except Exception as e:
    print(f"❌ Erreur générale: {e}")
    print(f"Type: {type(e)}")