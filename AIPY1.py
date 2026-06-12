import pandas as pd
import sys

def ucitaj_bazu_namirnica(filepath):
    try:
        # Čitamo Excel fajl bez naslova
        df = pd.read_excel(filepath, header=None, engine='openpyxl')
        
        # Uzimamo prve 3 kolone (A, B i C sa Vaše slike)
        df = df.iloc[:, :3]
        df.columns = ['Namirnica', 'Kalijum', 'Fosfor']
        
        # Čistimo prazne redove i tekst
        df = df.dropna(subset=['Namirnica'])
        df['Namirnica'] = df['Namirnica'].astype(str).str.strip()
        
        # Uklanjamo naslove grupa
        df = df[~df['Namirnica'].str.contains('SVEŽE|SVEŽA|SVEŽI|GOVEDE|SVINJSKO|Kalijum|Fosfor', case=False, na=False)]
        
        # Pretvaramo vrednosti u brojeve
        for col in ['Kalijum', 'Fosfor']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        df['Namirnica_Id'] = df['Namirnica'].str.lower()
        df = df.drop_duplicates(subset=['Namirnica_Id'])
        df.set_index('Namirnica_Id', inplace=True)
        return df
    except Exception as e:
        print("Greska pri ucitavanju tabele!")
        print(e)
        sys.exit()

def pretrazi_namirnice(df, pojam):
    rezultati = df[df['Namirnica'].str.contains(pojam, case=False, na=False)]
    return rezultati[['Namirnica']]

def glavni_program():
    fajl_putanja = r'KPH-AI.xlsx'
    print("Ucitavanje baze namirnica...")
    baza = ucitaj_bazu_namirnica(fajl_putanja)
    print("Uspesno ucitano!")
    
    dnevnik_ishrane = []
    while True:
        print("-" * 50)
        print("1. Dodaj namirnicu u dnevni unos")
        print("2. Prikazi trenutni presek")
        print("3. Zavrsi i izadi")
        izbor = input("Izaberi opciju (1-3): ").strip()
        
        if izbor == '1':
            pojam = input("\nUnesi naziv namirnice: ").strip()
            if len(pojam) < 2:
                print("Unesi bar 2 karaktera.")
                continue
            rezultati = pretrazi_namirnice(baza, pojam)
            if rezultati.empty:
                print("Nema rezultata.")
                continue
            print("\nPronadjene namirnice:")
            lista_rezultata = []
            for i, (idx, row) in enumerate(rezultati.iterrows(), start=1):
                print("{0}. {1}".format(i, row['Namirnica']))
                lista_rezultata.append((idx, row['Namirnica']))
            try:
                redni_broj = int(input("\nIzaberi broj: "))
                if 1 <= redni_broj <= len(lista_rezultata):
                    izabrani_id, tacan_naziv = lista_rezultata[redni_broj - 1]
                    grama = float(input("Unesi grame: "))
                    podaci = baza.loc[izabrani_id]
                    faktor = grama / 100.0
                    unos = {
                        'namirnica': tacan_naziv,
                        'grama': grama,
                        'kalijum': podaci['Kalijum'] * faktor,
                        'fosfor': podaci['Fosfor'] * faktor
                    }
                    dnevnik_ishrane.append(unos)
                    print("Dodato: {0}".format(tacan_naziv))
            except Exception as e:
                print("Greska pri unosu.")
        elif izbor == '2':
            if not dnevnik_ishrane:
                print("Dnevnik je prazan.")
                continue
            ukp_kal = 0
            ukp_fos = 0
            print("\nTrenutni unos:")
            for stavka in dnevnik_ishrane:
                print("- {0} ({1}g)".format(stavka['namirnica'], stavka['grama']))
                ukp_kal += stavka['kalijum']
                ukp_fos += stavka['fosfor']
            print("-" * 30)
            print("UKUPNO -> Kalijum: {0:.1f}mg | Fosfor: {1:.1f}mg".format(ukp_kal, ukp_fos))
        elif izbor == '3':
            break

if __name__ == "__main__":
    glavni_program()