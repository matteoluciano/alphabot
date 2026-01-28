import sqlite3
import subprocess
import time
import os

DB_COMMANDS = "commands.db"
MOVEMENTS_DIR = "movements"

def get_next_command():
    """Recupera il prossimo comando non eseguito"""
    conn = sqlite3.connect(DB_COMMANDS)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, command FROM commands WHERE executed = 0 ORDER BY id ASC LIMIT 1"
    )
    row = cur.fetchone()
    conn.close()
    return row

def mark_as_executed(command_id):
    """Segna un comando come eseguito"""
    conn = sqlite3.connect(DB_COMMANDS)
    cur = conn.cursor()
    cur.execute(
        "UPDATE commands SET executed = 1 WHERE id = ?",
        (command_id,)
    )
    conn.commit()
    conn.close()

def execute_movement(command):
    """Esegue il programma di movimento corrispondente"""
    script_map = {
        "circle": "circle.py",
        "square": "square.py",
        "triangle": "triangle.py"
    }
    
    script_name = script_map.get(command)
    if not script_name:
        print(f"Comando sconosciuto: {command}")
        return False
    
    script_path = os.path.join(MOVEMENTS_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f" File non trovato: {script_path}")
        return False
    
    try:
        print(f" Esecuzione: {script_path}")
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f" Comando completato con successo")
            return True
        else:
            print(f" Errore durante l'esecuzione:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f" Timeout: il comando ha impiegato troppo tempo")
        return False
    except Exception as e:
        print(f" Errore imprevisto: {e}")
        return False

def main():
    print(" Worker avviato. In attesa di comandi...")
    
    while True:
        try:
            command_data = get_next_command()
            
            if command_data:
                cmd_id, username, command = command_data
                print(f"\n Nuovo comando da {username}: {command} (ID: {cmd_id})")
                
                success = execute_movement(command)
                
                if success:
                    mark_as_executed(cmd_id)
                    print(f" Comando {cmd_id} completato e marcato come eseguito")
                else:
                    print(f" Comando {cmd_id} fallito, verrà ritentato")
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n Worker terminato dall'utente")
            break
        except Exception as e:
            print(f" Errore nel worker: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()