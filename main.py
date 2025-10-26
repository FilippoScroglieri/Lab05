import flet as ft
from flet.core.types import MainAxisAlignment, TextAlign

from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    text_Aggiungi= ft.Text('Aggiungi Nuova Automobile',size=20,text_align= ft.TextAlign.CENTER)

    text_Marca= ft.TextField(value= 'Marca',width=200,text_size=15)

    text_Modello = ft.TextField(value='Modello', width=200, text_size=15)

    text_Anno = ft.TextField(value='Anno', width=200, text_size=15)

    contatore= ft.TextField(width= 60, text_size=15)
    contatore.value= 0






    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def HandlerMinus(e):
        current_Val= contatore.value
        if current_Val > 0:
            current_Val= current_Val - 1
            contatore.value= current_Val
            page.update()

    def HandlerPlus(e):
        current_Val= contatore.value
        current_Val= current_Val + 1
        contatore.value= current_Val
        page.update()

    def Handler_aggiungi_auto(e):

            if text_Anno.value.isdigit():
                marca= text_Marca.value
                modello= text_Modello.value
                anno= int(text_Anno.value)
                posti= contatore.value
                autonoleggio.aggiungi_automobile(marca, modello, anno, posti)

                text_Marca.value = ""
                text_Modello.value = ""
                text_Anno.value = ""
                contatore.value = 0

                aggiorna_lista_auto()
                page.update()

            else:
                alert.show_alert('INSERISCI VALORI NUMERICI PER ANNO E POSTI')





    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btnMinus= ft.IconButton(icon= ft.Icons.REMOVE,icon_size= 20, icon_color='red',on_click= HandlerMinus)
    btnPlus = ft.IconButton(icon=ft.Icons.ADD, icon_size=20, icon_color='green', on_click=HandlerPlus)
    bottone= ft.ElevatedButton('Aggiungi Automobile',animate_size= 24,on_click= Handler_aggiungi_auto)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        text_Aggiungi, ft.Row([text_Marca, text_Modello, text_Anno,btnMinus,contatore,btnPlus],alignment=MainAxisAlignment.CENTER),
        bottone,
        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
