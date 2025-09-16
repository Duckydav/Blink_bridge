"""
Blink API Explorer - Découverte des nouveaux endpoints
"""

import asyncio
import requests
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth

async def explore_blink_api():
    print("=== EXPLORATION API BLINK ===\n")

    # Récupérer le token d'abord
    blink = Blink()
    auth = Auth({
        "username": "d.davidfrancois@gmail.com",
        "password": "Dave300945/"
    })
    blink.auth = auth

    print("🔐 Récupération token...")

    try:
        await blink.start()
        token = blink.auth.token if hasattr(blink.auth, 'token') else None

        if not token:
            print("❌ Impossible de récupérer le token")
            return

        print(f"✅ Token récupéré: {token[:20]}...")

        # Bases URLs à tester
        base_urls = [
            "https://rest-u056.immedia-semi.com",
            "https://rest-prod.immedia-semi.com",
            "https://rest-e31.immedia-semi.com"
        ]

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Blink/3.16.0 (iPhone; iOS 15.0; Scale/2.00)"
        }

        # Endpoints à explorer par catégorie
        endpoints_categories = {
            "Account": [
                "/account",
                "/accounts",
                "/accounts/392166",
                "/api/account",
                "/api/accounts",
                "/api/accounts/392166"
            ],
            "Networks": [
                "/networks",
                "/network",
                "/network/586048",
                "/api/networks",
                "/api/network",
                "/api/network/586048",
                "/api/v2/networks",
                "/api/v3/networks",
                "/api/v4/networks",
                "/api/v5/networks"
            ],
            "Devices": [
                "/devices",
                "/sync_modules",
                "/cameras",
                "/api/devices",
                "/api/sync_modules",
                "/api/cameras",
                "/api/v2/devices",
                "/api/v3/devices"
            ],
            "Homescreen": [
                "/homescreen",
                "/api/homescreen",
                "/api/v2/homescreen",
                "/api/v3/homescreen",
                "/api/v3/accounts/392166/homescreen",
                "/api/v4/accounts/392166/homescreen"
            ]
        }

        successful_endpoints = []

        for base_url in base_urls:
            print(f"\n🌐 Test base URL: {base_url}")

            for category, endpoints in endpoints_categories.items():
                print(f"\n   📂 Catégorie: {category}")

                for endpoint in endpoints:
                    try:
                        url = f"{base_url}{endpoint}"
                        response = requests.get(url, headers=headers, timeout=5)

                        status_icon = "✅" if response.status_code == 200 else "❌"
                        print(f"      {status_icon} {endpoint}: {response.status_code}")

                        if response.status_code == 200:
                            successful_endpoints.append((base_url, endpoint))
                            data = response.json()

                            # Analyser le contenu
                            if isinstance(data, dict):
                                keys = list(data.keys())
                                print(f"         Clés: {keys}")

                                # Rechercher des indices importants
                                important_keys = []
                                for key in keys:
                                    if any(word in key.lower() for word in ['sync', 'camera', 'device', 'module']):
                                        important_keys.append(key)

                                if important_keys:
                                    print(f"         🎯 Clés importantes: {important_keys}")

                                # Analyser les données
                                for key, value in data.items():
                                    if isinstance(value, list) and len(value) > 0:
                                        print(f"         📋 {key}: {len(value)} éléments")
                                        if len(value) > 0:
                                            print(f"            Premier élément: {str(value[0])[:100]}...")

                            elif isinstance(data, list):
                                print(f"         📋 Liste de {len(data)} éléments")
                                if len(data) > 0:
                                    print(f"            Premier: {str(data[0])[:100]}...")

                    except requests.exceptions.Timeout:
                        print(f"      ⏱️ {endpoint}: Timeout")
                    except Exception as e:
                        print(f"      ❌ {endpoint}: {str(e)[:50]}")

        # Résumé des succès
        print(f"\n🎯 ENDPOINTS FONCTIONNELS:")
        if successful_endpoints:
            for base_url, endpoint in successful_endpoints:
                print(f"   ✅ {base_url}{endpoint}")
        else:
            print("   ❌ Aucun endpoint fonctionnel trouvé")

        # Test découverte par exploration
        print(f"\n🔍 EXPLORATION LIBRE:")
        await explore_by_discovery(base_urls[0], headers)

    except Exception as e:
        print(f"❌ Erreur exploration: {e}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            await blink.auth.session.close()
        except:
            pass

async def explore_by_discovery(base_url, headers):
    """Exploration par découverte de patterns"""

    # Patterns courants dans les APIs REST
    discovery_paths = [
        "/",
        "/api",
        "/api/v1",
        "/api/v2",
        "/api/v3",
        "/v1",
        "/v2",
        "/v3",
        "/.well-known",
        "/swagger",
        "/docs"
    ]

    print("   Exploration patterns communs...")

    for path in discovery_paths:
        try:
            url = f"{base_url}{path}"
            response = requests.get(url, headers=headers, timeout=3)

            if response.status_code == 200:
                print(f"      ✅ {path}: Accessible")

                # Analyser si c'est du JSON
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'endpoints' in str(data).lower():
                        print(f"         🎯 Possible documentation API trouvée!")
                except:
                    pass

        except:
            pass

if __name__ == "__main__":
    print("🚀 EXPLORATION COMPLÈTE API BLINK")
    print("📱 Préparez le code SMS...\n")

    asyncio.run(explore_blink_api())

    print("\n💡 PROCHAINE ÉTAPE:")
    print("   Si endpoints trouvés → Accès direct aux devices")
    print("   Si aucun endpoint → Interception trafic app iOS")