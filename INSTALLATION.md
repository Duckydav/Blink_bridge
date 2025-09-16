# Blink_bridge - Guide d'installation

## 🎯 Objectif
Contourner le système propriétaire Blink pour accéder aux caméras et Sync Module 2 depuis Windows 11.

## 📋 Prérequis
- Windows 11
- Python 3.8+
- Accès à votre app Blink iOS
- Credentials Blink (email/password)

## 🔧 Installation

### Étape 1: Environnement Python
```bash
cd C:\Users\David\Dev\Personal\Blink_bridge
python -m venv venv
venv\Scripts\activate
```

### Étape 2: Dépendances principales
```bash
# Librairie Blink non-officielle (clé du projet!)
pip install blinkpy

# Outils réseau et analyse
pip install requests
pip install python-nmap
pip install mitmproxy

# Traitement image/vidéo
pip install opencv-python
pip install pillow
```

### Étape 3: Configuration initiale
1. **Modifiez vos credentials** dans `research\blinkpy_test.py`
2. **Testez la connexion**:
   ```bash
   python research\blinkpy_test.py
   ```

## 🧪 Tests de base

### Test 1: Découverte réseau
```bash
python research\network_discovery.py
```
→ Trouve votre Sync Module 2 sur le réseau local

### Test 2: Analyse APIs
```bash
python research\existing_solutions_analysis.py
```
→ Documente les endpoints Blink disponibles

### Test 3: Connexion Blink
```bash
python research\blinkpy_test.py
```
→ Teste l'accès via blinkpy (⚠️ credentials requis)

## 🔍 Points critiques identifiés

### 🎯 Accès stockage local (clé USB)
**Endpoints clés:**
- `/api/v1/network/{id}/sync_modules/{id}/local_storage/manifest/request`
- `/api/v1/network/{id}/sync_modules/{id}/local_storage/manifest/clips`

### 🔐 Authentification
- **Base URL**: `https://rest-prod.immedia-semi.com`
- **Login**: `/api/v5/account/login`
- **User-Agent**: `BlinkMobile_Android` (important!)
- **Auth**: JWT Bearer token

### 📱 Limitations iOS
- Pas d'API officielle
- Reverse engineering nécessaire
- 2FA peut compliquer l'automatisation

## 🚨 Problèmes potentiels

### Authentification 2FA
Si 2FA activé sur votre compte:
- Désactiver temporairement pour tests
- Ou implémenter gestion PIN verification

### Rate limiting
- APIs Blink peuvent limiter les requêtes
- Implémenter delays entre appels

### Changements API
- Blink peut modifier leurs endpoints
- Surveillance via community GitHub

## 📈 Prochaines étapes

### Phase 1: Validation
1. ✅ Installer dépendances
2. ✅ Tester connexion basique
3. 🔄 Valider accès stockage local

### Phase 2: Développement
1. Interface Windows native
2. Monitoring automatique clips
3. Intégration cam_detect

### Phase 3: Optimisation
1. Gestion erreurs robuste
2. Cache et performance
3. Interface utilisateur

## 💡 Ressources

### Projets inspirants
- **blinkpy**: https://github.com/fronzbot/blinkpy
- **homebridge-blink**: https://github.com/khaost/homebridge-blink
- **Home Assistant Blink**: https://github.com/fronzbot/blink-homeassistant

### Outils debug
- **Wireshark**: Analyse trafic réseau
- **mitmproxy**: Interception HTTPS
- **Postman**: Test APIs manuels

---

**⚠️ Important**: Ce projet est à des fins éducatives. Respectez les conditions d'utilisation Blink.