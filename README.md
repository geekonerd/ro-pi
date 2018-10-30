# ro-pi
*a simple ROBOT controlled by a Raspberry Pi*

### Intro
**ro-pi** è un piccolo robottino capace di muoversi sul piano sia in maniera autonoma che controllato dall'utente, sa riconoscere eventuali ostacoli davanti a lui, può riprendere in video ciò che lo circonda ed è in grado di notificare eventi tramite LED di stato e/o mostrare messaggi via display LCD. Per maggiori dettagli rimando alla *serie* di focus ad esso dedicati pubblicati sul mio blog (https://geekonerd.blogspot.com/p/gli-esperimenti.html).

#### Contenuto
Sono presenti i file python contenenti il codice di controllo per i vari sensori collegati al robottino, la configurazione generale, uno script di reset dei PIN utilizzati, ed ovviamente il programma principale che fa da collante a tutte le librerie utilizzate.

###### Nota bene
Il codice presente in questo repository funziona su un Raspberry Pi configurato come descritto nei tutorial. Nella versione attuale, si tratta di una *demo* che funziona ma che può sicuramente essere migliorata ed integrata. Inoltre, è richiesta l'installazione della libreria AdaFruit_CharLCD per la gestione del display (si rimanda al blog per maggiori dettagli alla puntata relativa proprio a tale componente).
