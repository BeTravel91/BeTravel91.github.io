import os
import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    print(f"Starte: {description}...")
    try:
        # Führt den Befehl aus und fängt den Output für die Analyse ab
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Erfolg: {description}\n{result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FEHLER bei: {description}")
        print(f"Details zum Fehler:\n{e.stderr.strip()}")
        return False

def main():
    print("Starte neuen, direkten Upload-Prozess für den Reiseblog...")
    
    # Optional: Sicherstellen, dass wir im richtigen Verzeichnis sind
    repo_path = os.getcwd()
    print(f"Aktuelles Repository-Verzeichnis: {repo_path}")

    # 1. Dateien zum Staging hinzufügen
    if not run_command(["git", "add", "."], "Dateien zum Staging hinzufügen (git add)"):
        print("Upload abgebrochen: Fehler beim Hinzufügen der Dateien.")
        sys.exit(1)

    # 2. Commit erstellen
    commit_message = f"Automatisches Blog-Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    print(f"Starte: Commit erstellen ('{commit_message}')...")
    try:
        result = subprocess.run(["git", "commit", "-m", commit_message], check=True, text=True, capture_output=True)
        print(f"Erfolg: Commit erstellt\n{result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        # Spezifische Analyse: Wenn es keine Änderungen gibt, ist das kein echter Fehler
        output = e.stdout.lower() + e.stderr.lower()
        if "nothing to commit" in output or "nichts zu committen" in output:
            print("Hinweis: Keine neuen Änderungen gefunden. Der Upload-Prozess läuft trotzdem weiter.")
        else:
            print(f"FEHLER beim Commit:\n{e.stderr.strip()}")
            sys.exit(1)

    # 3. Änderungen pushen
    if not run_command(["git", "push"], "Änderungen hochladen (git push)"):
        print("Upload abgebrochen: Fehler beim Pushen zu GitHub.")
        sys.exit(1)

    print("Upload komplett und erfolgreich abgeschlossen! Die GitHub Pages Website aktualisiert sich in wenigen Minuten.")

if __name__ == "__main__":
    main()