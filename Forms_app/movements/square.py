from AlphaBotV1 import AlphaBot
import time

def move_square():
    print("Inizio movimento: QUADRATO")
    
    Ab = AlphaBot()
    Ab.stop()
    
    try:
        # Lato 1
        Ab.forward()
        time.sleep(2)
        Ab.stop()
        Ab.right()
        time.sleep(0.28)
        Ab.stop()
        
        # Lato 2
        Ab.forward()
        time.sleep(2)
        Ab.stop()
        Ab.right()
        time.sleep(0.28)
        Ab.stop()
        
        # Lato 3
        Ab.forward()
        time.sleep(2)
        Ab.stop()
        Ab.right()
        time.sleep(0.28)
        Ab.stop()
        
        # Lato 4
        Ab.forward()
        time.sleep(2)
        Ab.stop()
        Ab.right()
        time.sleep(0.28)
        Ab.stop()
        
        
    except Exception as e:
        print(f"Errore durante il movimento: {e}")
        Ab.stop()
        raise
    finally:
        Ab.stop()

if __name__ == "__main__":
    try:
        move_square()
    except KeyboardInterrupt:
        print("\nMovimento interrotto")
        Ab = AlphaBot()
        Ab.stop()