import tkinter as tk
import requests

venster = tk.Tk()
venster.geometry("600x450")

voer_modelnaam = tk.Entry()
voer_modelnaam.pack()

voer_dagprijs = tk.Entry()
voer_dagprijs.pack()

voer_aantal = tk.Entry()
voer_aantal.pack()


def sla():
    modelnaam = voer_modelnaam.get()
    dagprijs = int(voer_dagprijs.get())
    aantal = int(voer_aantal.get())

    antwoord =requests.post("http://127.0.0.1:8000/voeg_toe", json={"modelnaam": modelnaam, "dagprijs": dagprijs, "aantal": aantal}).json()
    if antwoord['status'] == True:
        label.config(text=f"{antwoord['bericht']}")
    else:
        label.config(text=f"{antwoord['bericht']}")

label = tk.Label()
label.pack()

knop = tk.Button(venster,text="sla op", command=sla)
knop.pack()


voer_klantnaam = tk.Entry()
voer_klantnaam.pack()

voer_automodel = tk.Entry()
voer_automodel.pack()

voer_dagen = tk.Entry()
voer_dagen.pack()

def huur():
    klantnaam = voer_klantnaam.get()
    automodel = voer_automodel.get()
    dagen = (voer_dagen.get())

    antwoord = requests.post("http://127.0.0.1:8000/huur", json={"klantnaam": klantnaam, "automodel": automodel, "dagen": dagen}).json()
    if antwoord["status"] == True:
        label1.config(text=f"{antwoord['bericht']}", bg="green")
    else:
        label1.config(text=f"{antwoord['bericht']}", bg="red")

label1 = tk.Label()
label1.pack()

knop1 = tk.Button(venster, text="huur", command=huur)
knop1.pack()


def kijken():
    antwoord = requests.get("http://127.0.0.1:8000/kijk").json()
    clean = ''
    for k in antwoord:
        clean += f"{k}\n"
    label2.config(text=clean)

label2 = tk.Label()
label2.pack()

knop2 = tk.Button(venster, text="kijk", command=kijken)
knop2.pack()

venster.mainloop()