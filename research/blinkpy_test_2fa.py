"""
Test blinkpy avec gestion 2FA interactive
"""

import asyncio
try:
    from blinkpy.blinkpy import Blink
    from blinkpy.auth import Auth
    import json

    async def test_blink_with_2fa():
        print("=== Test connexion Blink avec 2FA ===\n")

        # Configuration
        blink = Blink()

        # Credentials
        auth = Auth({
            "username": "d.davidfrancois@gmail.com",
            "password": "CuN8lOH6Sudk_Iin"
        })

        blink.auth = auth

        print("Tentative de connexion...")
        print("⚠️ Un code 2FA sera demandé si activé")

        try:
            # Connexion avec gestion 2FA
            await blink.start()

            print("✅ Connexion réussie!")
            print(f"Réseaux trouvés: {len(blink.networks)}")

            if not blink.networks:
                print("❌ Aucun réseau trouvé")
                return

            # Afficher les informations détaillées
            for network_name, network in blink.networks.items():
                print(f"\n📡 Réseau: {network_name}")
                print(f"   - ID: {network.network_id}")
                print(f"   - Statut: {'Armé' if network.arm else 'Désarmé'}")

                # Sync modules
                print(f"   🔄 Sync Modules ({len(network.sync_modules)}):")
                for sync_name, sync in network.sync_modules.items():
                    print(f"      - {sync_name} (ID: {sync.sync_id})")
                    print(f"        Status: {sync.status}")

                    # Lister tous les attributs pour debug
                    attrs = [attr for attr in dir(sync) if not attr.startswith('_') and not callable(getattr(sync, attr, None))]
                    print(f"        Attributs: {attrs}")

                # Caméras
                print(f"   📹 Caméras ({len(network.cameras)}):")
                for camera_name, camera in network.cameras.items():
                    print(f"      - {camera_name} (ID: {camera.camera_id})")
                    print(f"        Status: {camera.status}")

                    if hasattr(camera, 'battery'):
                        print(f"        Batterie: {camera.battery}")

            # 🎯 TEST CRUCIAL : Accès stockage local
            print("\n💾 🎯 TEST STOCKAGE LOCAL USB:")
            for network_name, network in blink.networks.items():
                for sync_name, sync in network.sync_modules.items():
                    print(f"\n   Test pour Sync Module: {sync_name}")

                    # Vérifier local storage
                    if hasattr(sync, 'local_storage'):
                        print(f"      ✅ Attribut local_storage trouvé: {sync.local_storage}")

                    # Essayer les méthodes de manifeste
                    methods = ['get_local_storage_manifest', 'local_storage_manifest', 'get_manifest']

                    for method in methods:
                        if hasattr(sync, method):
                            try:
                                print(f"      Tentative {method}...")
                                func = getattr(sync, method)

                                if asyncio.iscoroutinefunction(func):
                                    result = await func()
                                else:
                                    result = func()

                                print(f"      ✅ {method} réussi!")
                                print(f"         Type: {type(result)}")
                                print(f"         Contenu: {result}")

                                if isinstance(result, dict) and 'clips' in result:
                                    clips = result['clips']
                                    print(f"         🎬 {len(clips)} clips USB trouvés!")

                                    for i, clip in enumerate(clips[:3]):
                                        print(f"            Clip {i+1}: {clip.get('name', 'unknown')}")
                                        print(f"               Size: {clip.get('size', 'unknown')}")
                                        print(f"               Date: {clip.get('created_at', 'unknown')}")

                                break

                            except Exception as e:
                                print(f"      ❌ {method}: {e}")

            print("\n🎯 RÉSULTAT: Connexion Blink établie avec succès!")
            print("   - API fonctionnelle")
            print("   - Sync modules détectés")
            print("   - Prêt pour accès USB si disponible")

        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            import traceback
            traceback.print_exc()

        finally:
            # Fermer proprement
            try:
                await blink.auth.session.close()
            except:
                pass

    if __name__ == "__main__":
        print("🚀 Test Blink_bridge avec 2FA...\n")

        print("💡 Instructions:")
        print("   1. Lancez ce script")
        print("   2. Entrez le code 2FA reçu par email quand demandé")
        print("   3. Observez les informations de vos devices")

        asyncio.run(test_blink_with_2fa())

except ImportError as e:
    print(f"❌ Erreur d'importation: {e}")
    print("Installation: pip install blinkpy aiohttp")