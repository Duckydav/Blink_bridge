"""
Test rapide Blink avec instructions claires pour 2FA
"""

import asyncio
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth

async def simple_blink_test():
    print("=== TEST BLINK SIMPLE ===\n")

    # Configuration
    blink = Blink()
    auth = Auth({
        "username": "d.davidfrancois@gmail.com",
        "password": "CuN8lOH6Sudk_Iin"
    })
    blink.auth = auth

    print("🔐 Connexion à Blink...")
    print("📧 Vérifiez votre email pour le code 2FA...")
    print("⚠️  Le code est composé de 6 CHIFFRES (ex: 123456)")
    print("⚠️  NE PAS taper votre mot de passe!")
    print("")

    try:
        await blink.start()

        print("✅ SUCCÈS! Connexion établie")
        print(f"📡 Réseaux Blink: {len(blink.networks)}")

        if blink.networks:
            for name, network in blink.networks.items():
                print(f"   - {name}: {len(network.cameras)} caméra(s), {len(network.sync_modules)} sync module(s)")

                # Info sync modules
                for sync_name, sync in network.sync_modules.items():
                    print(f"     🔄 Sync: {sync_name} (Status: {sync.status})")

        else:
            print("❌ Aucun réseau trouvé - problème d'authentification")

    except Exception as e:
        print(f"❌ Erreur: {e}")

    finally:
        try:
            await blink.auth.session.close()
        except:
            pass

if __name__ == "__main__":
    print("📱 IMPORTANT: Allez maintenant vérifier votre email!")
    print("   Le code 2FA arrive en quelques secondes...")
    print("   Format: 6 chiffres (ex: 234567)")
    print()

    asyncio.run(simple_blink_test())