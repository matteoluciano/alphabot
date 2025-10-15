# Documentazione Progetto AlphaBot

## Descrizione del Progetto

Progetto di controllo e programmazione di un robot AlphaBot utilizzando Python. Il progetto include il controllo remoto tramite protocollo TCP e la navigazione autonoma con sensori di prossimità.

## Repository

Il codice sorgente del progetto è disponibile su GitHub:  
[https://github.com/matteoluciano/alphabot](https://github.com/matteoluciano/alphabot)

## Fasi di Sviluppo

### 1. Studio della Libreria AlphaBot

Inizialmente abbiamo analizzato e compreso la libreria fornita per l'AlphaBot, familiarizzando con le funzioni disponibili per il controllo del robot.

### 2. Test Iniziali

Abbiamo eseguito i primi test per verificare il corretto funzionamento dell'AlphaBot, testando i comandi base di movimento.

### 3. Implementazione Client-Server TCP

Abbiamo sviluppato un sistema client-server che permette di comandare l'AlphaBot da remoto tramite protocollo TCP:

- **Server**: eseguito sull'AlphaBot, riceve i comandi dal client
- **Client**: eseguito sul PC, invia i comandi di controllo all'AlphaBot

Questo permette di controllare il robot da remoto attraverso la rete.

### 4. Integrazione Sensori di Prossimità

Abbiamo esteso la libreria dell'AlphaBot aggiungendo il supporto per due sensori di prossimità. Questa integrazione ha permesso di implementare funzionalità avanzate.

### 5. Navigazione Autonoma

Abbiamo sviluppato un programma che permette all'AlphaBot di muoversi autonomamente evitando gli ostacoli. Il robot utilizza i sensori di prossimità per rilevare gli oggetti circostanti e modificare la propria traiettoria, evitando collisioni.

## Setup e Utilizzo

### Requisiti

- AlphaBot
- PC con Python installato
- Connessione di rete tra PC e AlphaBot
- WinSCP per il trasferimento file
- Client SSH

### Esecuzione dei Programmi

1. **Connessione SSH**: Collegarsi all'AlphaBot tramite SSH per eseguire i file Python
2. **Trasferimento File**: Utilizzare WinSCP per copiare i file Python sull'AlphaBot
3. **Esecuzione**: Lanciare i programmi Python direttamente dalla sessione SSH

### Collaborazione

Il progetto viene sviluppato in collaborazione utilizzando Git e GitHub per la condivisione del codice e il version control.

## Funzionalità Principali

- ✓ Controllo manuale tramite comandi TCP
- ✓ Movimento autonomo con evitamento ostacoli
- ✓ Integrazione sensori di prossimità
- ✓ Architettura client-server per controllo remoto