import socket
import threading
import json
import subprocess
import sys
import time

# --- IMPORTS DE CONTRÔLE ---
try:
    import vgamepad as vg
    import pyautogui
    from pynput.mouse import Button, Controller as MouseController
    from pynput.keyboard import Key, Controller as KeyboardController
except ImportError:
    print("Erreur : Bibliothèques manquantes. Veuillez lancer 'run.bat' ou faire 'pip install -r requirements.txt'")
    sys.exit(1)

# --- INITIALISATION DES PÉRIPHÉRIQUES VIRTUELS ---
print("[INFO] Initialisation de la manette Xbox virtuelle...")
gamepad = vg.VX360Gamepad()

print("[INFO] Initialisation de la souris et du clavier virtuels...")
mouse = MouseController()
keyboard = KeyboardController()

# --- CONFIGURATION RÉSEAU ---
PORT = 8080
HOST = "0.0.0.0"

def get_local_ip():
    """Récupère l'adresse IP locale du PC pour l'afficher à l'utilisateur."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def setup_adb_usb():
    """Configure automatiquement l'ADB pour la connexion USB."""
    print("[INFO] Tentative de configuration du mode USB (ADB)...")
    try:
        # Cette commande redirige le port du PC vers le téléphone via USB
        subprocess.run(["adb", "forward", f"tcp:{PORT}", f"tcp:{PORT}"], 
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[SUCCÈS] Connexion USB configurée. (Port {PORT} redirigé)")
    except FileNotFoundError:
        print("[AVERTISSEMENT] ADB n'est pas installé ou pas dans le PATH. Le mode USB ne fonctionnera pas.")
        print("                Veuillez installer Android Platform Tools pour utiliser l'USB.")
    except subprocess.CalledProcessError:
        print("[AVERTISSEMENT] Échec de la configuration ADB. Vérifiez que le débogage USB est activé sur le téléphone.")

def handle_client(client_socket, addr):
    """Gère la réception des données d'un client (téléphone)."""
    print(f"[CONNEXION] Appareil connecté depuis : {addr}")
    buffer = ""
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            buffer += data.decode('utf-8')
            
            # Séparation des messages JSON (si plusieurs messages arrivent collés)
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if not line.strip():
                    continue
                
                try:
                    msg = json.loads(line)
                    process_input(msg)
                except json.JSONDecodeError:
                    print(f"[ERREUR] Message JSON invalide : {line}")
                    
    except ConnectionResetError:
        pass
    finally:
        print(f"[DÉCONNEXION] Appareil déconnecté : {addr}")
        client_socket.close()

def process_input(msg):
    """Traite les commandes reçues du téléphone."""
    action = msg.get("action")
    value = msg.get("value")
    state = msg.get("state", "press")

    # --- GESTION DE LA MANETTE XBOX ---
    if action == "xbox_btn":
        btn = getattr(vg.XUSB_BUTTON, f"XUSB_GAMEPAD_{value.upper()}", None)
        if btn:
            if state == "press":
                gamepad.press_button(button=btn)
            else:
                gamepad.release_button(button=btn)
            gamepad.update()

    elif action == "xbox_trigger":
        # value = "LEFT" ou "RIGHT", state = valeur entre 0 et 255
        if value.upper() == "LEFT":
            gamepad.left_trigger(int(state))
        elif value.upper() == "RIGHT":
            gamepad.right_trigger(int(state))
        gamepad.update()

    elif action == "xbox_joystick":
        # value = "LEFT" ou "RIGHT", x et y entre -1.0 et 1.0
        x = int(msg.get("x", 0) * 32767)
        y = int(msg.get("y", 0) * 32767)
        if value.upper() == "LEFT":
            gamepad.left_joystick(x_value=x, y_value=y)
        elif value.upper() == "RIGHT":
            gamepad.right_joystick(x_value=x, y_value=y)
        gamepad.update()

    # --- GESTION SOURIS / CLAVIER ---
    elif action == "mouse_move":
        # value_x et value_y sont les déplacements relatifs
        mouse.move(msg.get("dx", 0), msg.get("dy", 0))

    elif action == "mouse_click":
        btn = Button.left if value == "left" else Button.right
        if state == "press":
            mouse.press(btn)
        else:
            mouse.release(btn)

    elif action == "keyboard":
        # value = la touche (ex: 'a', 'space', 'shift')
        try:
            k = getattr(Key, value) if hasattr(Key, value) else value
            if state == "press":
                keyboard.press(k)
            else:
                keyboard.release(k)
        except Exception as e:
            print(f"Touche non reconnue : {value}")

def start_server():
    """Démarre le serveur TCP."""
    ip = get_local_ip()
    
    print("="*55)
    print("           SERVEUR TOUCH-LAM32 ACTIF")
    print("="*55)
    print(f"Adresse IP locale (Wi-Fi) : {ip}")
    print(f"Port : {PORT}")
    print("Pour vous connecter via Wi-Fi, entrez cette IP dans l'app.")
    print("Pour vous connecter via USB, activez le débogage USB.")
    print("-" * 55)
    
    setup_adb_usb()
    
    print("-" * 55)
    print("[EN ATTENTE] En attente de connexion du téléphone...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    try:
        while True:
            client, addr = server.accept()
            # Lance un thread pour chaque client (permet plusieurs téléphones en même temps)
            thread = threading.Thread(target=handle_client, args=(client, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt du serveur...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()