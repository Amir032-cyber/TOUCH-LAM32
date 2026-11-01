# TOUCH-LAM32
gamepad remote for windows xbox

# TOUCH-LAM32 - PC Server

Ceci est le serveur PC pour l'application Android TOUCH-LAM32. Il permet de transformer votre téléphone en manette Xbox, souris ou clavier pour votre PC.

## 🛠️ Prérequis
1. Avoir **Python** installé sur le PC (Téléchargez-le sur [python.org](https://www.python.org/downloads/) et **cochez "Add Python to PATH"** lors de l'installation).
2. **Pour le mode USB (Recommandé) :** Avoir installé les [Android Platform Tools (ADB)](https://developer.android.com/studio/releases/platform-tools) et activé le "Débogage USB" sur votre téléphone.
3. **Pilote Manette :** Le serveur installe automatiquement `vgamepad`, mais si la manette n'est pas reconnue dans les jeux, installez [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases).

## 🚀 Comment lancer le serveur
1. Téléchargez le fichier ZIP de ce dépôt (bouton vert "Code" -> "Download ZIP") ou allez dans l'onglet **Releases**.
2. Extrayez le fichier ZIP dans un dossier.
3. Double-cliquez sur **`run.bat`**.
4. Une fenêtre noire s'ouvre. Elle vous affichera votre **Adresse IP locale** (ex: `192.168.1.50`).

## 📱 Comment connecter l'application
1. Ouvrez l'application TOUCH-LAM32 sur votre téléphone.
2. **Via Wi-Fi :** Assurez-vous que le téléphone et le PC sont sur le même réseau Wi-Fi. Entrez l'adresse IP affichée sur l'écran noir du PC.
3. **Via USB (sans latence) :** Branchez le câble USB, activez le débogage USB. Sur l'application, choisissez la connexion USB (ou tapez `127.0.0.1`).

## ❓ Besoin d'aide ?
Rejoignez la communauté sur [WhatsApp](https://whatsapp.com/channel/0029VbDz9WHJJhzQEVnnu22I)ou contacter le +226 02688902 .