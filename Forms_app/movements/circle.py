from AlphaBotV1 import AlphaBot
import time

def move_circle():

    print(" Inizio movimento: CERCHIO")
    
    Ab = AlphaBot()
    Ab.stop()
    
    try:
        for i in range(16):  
            Ab.forward()
            time.sleep(0.3)
            Ab.stop()
            Ab.right()
            time.sleep(0.1)  
            Ab.stop()
            print(f"  Segmento {i+1}/16 del cerchio...")
        
        print("Cerchio completato!")
        
    except Exception as e:
        print(f"Errore durante il movimento: {e}")
        Ab.stop()
        raise
    finally:
        Ab.stop()

if __name__ == "__main__":
    try:
        move_circle()
    except KeyboardInterrupt:
        print("\nMovimento interrotto")
        Ab = AlphaBot()
        Ab.stop()