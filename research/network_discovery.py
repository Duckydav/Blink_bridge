"""
Blink_bridge - Network Discovery Module
Recherche et identification du Sync Module 2 sur le réseau local
"""

import socket
import subprocess
import ipaddress
from typing import List, Dict, Optional
import time

class SyncModuleDiscovery:
    """
    Classe pour découvrir et identifier le Sync Module 2 Blink sur le réseau
    """

    def __init__(self):
        self.known_ports = [80, 443, 8080, 22, 23]  # Ports communs à tester
        self.blink_signatures = [
            "blink", "sync", "immedia", "amazon"  # Signatures possibles
        ]

    def get_local_network(self) -> Optional[str]:
        """Détermine le réseau local"""
        try:
            # Obtenir l'IP locale
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            sock.close()

            # Calculer le réseau /24
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            return str(network)
        except Exception as e:
            print(f"Erreur détection réseau: {e}")
            return None

    def scan_port(self, ip: str, port: int, timeout: float = 1.0) -> bool:
        """Test si un port est ouvert sur une IP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def scan_device(self, ip: str) -> Dict:
        """Scan complet d'un device"""
        device_info = {
            "ip": ip,
            "open_ports": [],
            "hostname": None,
            "mac_address": None,
            "is_potential_sync": False
        }

        # Test des ports
        for port in self.known_ports:
            if self.scan_port(ip, port):
                device_info["open_ports"].append(port)

        # Tentative résolution hostname
        try:
            device_info["hostname"] = socket.gethostbyaddr(ip)[0].lower()
        except:
            pass

        # Vérification signatures Blink
        hostname = device_info["hostname"] or ""
        for signature in self.blink_signatures:
            if signature in hostname:
                device_info["is_potential_sync"] = True
                break

        return device_info

    def discover_devices(self) -> List[Dict]:
        """Découvre tous les devices sur le réseau local"""
        network = self.get_local_network()
        if not network:
            return []

        print(f"Scan du réseau {network}...")
        devices = []

        net = ipaddress.IPv4Network(network)
        for ip in net.hosts():
            ip_str = str(ip)
            print(f"Test {ip_str}...", end=" ")

            # Test ping rapide
            if self.ping_host(ip_str):
                print("UP - Analyse...")
                device = self.scan_device(ip_str)
                devices.append(device)
            else:
                print("DOWN")

        return devices

    def ping_host(self, ip: str) -> bool:
        """Test ping rapide"""
        try:
            # Windows
            result = subprocess.run(
                ["ping", "-n", "1", "-w", "1000", ip],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False

    def find_sync_modules(self) -> List[Dict]:
        """Trouve les modules Sync potentiels"""
        devices = self.discover_devices()
        candidates = []

        for device in devices:
            score = 0
            reasons = []

            # Scoring basé sur différents critères
            if device["is_potential_sync"]:
                score += 50
                reasons.append("Hostname suspect")

            if 80 in device["open_ports"]:
                score += 20
                reasons.append("Port HTTP ouvert")

            if 443 in device["open_ports"]:
                score += 20
                reasons.append("Port HTTPS ouvert")

            if len(device["open_ports"]) > 0:
                score += 10
                reasons.append(f"{len(device['open_ports'])} ports ouverts")

            if score > 0:
                device["score"] = score
                device["reasons"] = reasons
                candidates.append(device)

        # Trier par score décroissant
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates

if __name__ == "__main__":
    discovery = SyncModuleDiscovery()

    print("=== Blink_bridge - Découverte Sync Module 2 ===\n")

    candidates = discovery.find_sync_modules()

    if not candidates:
        print("Aucun module Sync potentiel trouvé.")
    else:
        print(f"Trouvé {len(candidates)} candidat(s):\n")

        for i, device in enumerate(candidates, 1):
            print(f"{i}. {device['ip']} (Score: {device['score']})")
            print(f"   Hostname: {device['hostname'] or 'Inconnu'}")
            print(f"   Ports ouverts: {device['open_ports']}")
            print(f"   Raisons: {', '.join(device['reasons'])}")
            print()