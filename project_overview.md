# Blink_bridge - Accès distant au Sync Module 2

## Objectif
Créer un pont logiciel pour accéder aux images stockées sur la clé USB du Sync Module 2 Blink sans déconnexion physique.

## Défis techniques
- Accès distant à la clé USB sans interruption du service
- Interface avec le Sync Module 2 via réseau
- Extraction et traitement des images en temps réel
- Intégration avec les capacités de détection de cam_detect

## Approches à explorer
1. **API Blink** (officielle/reverse-engineered)
2. **Accès réseau direct** au module
3. **Monitoring filesystem** via partage réseau
4. **Interception protocole** app ↔ module

## Architecture envisagée
```
Sync Module 2 → Blink_bridge → Analysis Engine → Results
     ↓              ↓               ↓              ↓
  USB Storage → Network Access → AI Detection → Alerts/Storage
```

## Technologies pressenties
- Python pour logique principale
- Networking libraries (requests, socket)
- Computer vision (OpenCV, YOLO?)
- Inspiration de cam_detect pour l'analyse

## Phases de développement
1. **Reconnaissance** - Scanner et identifier le module sur réseau
2. **Connexion** - Établir communication avec le Sync Module 2
3. **Extraction** - Accéder aux fichiers de la clé USB
4. **Analyse** - Traiter les images (détection, classification)
5. **Interface** - Dashboard pour monitoring et contrôle

## Notes
- Projet expérimental et éducatif
- Respecter les conditions d'utilisation Blink
- Priorité à la stabilité du système existant