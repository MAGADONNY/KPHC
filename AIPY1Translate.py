import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Bezbedan CSS stil za tamnu temu, ZELENO DUGME i prostor za futer na telefonima
st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;padding-bottom:200px!important;} footer {visibility: hidden!important;} [data-testid='stActionButton'] {display: none!important;} [data-testid='stStatusWidget'] {display: none!important;} div[data-baseweb='select'] font-size:18px!important; font-weight:bold!important;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:6px!important; height:50px!important;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important; font-size:18px!important; font-weight:bold!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#2ECC71!important; border:none!important; width:100%!important; text-shadow:none!important; padding: 12px 0px!important; font-size:18px!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#2ECC71!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;} .stSelectbox div[data-baseweb='select'] {font-size:18px!important; font-weight:bold!important; color:#ffffff!important;}</style>", unsafe_allow_html=True)

# Inicijalizacija session_state liste za čuvanje unetih obroka
if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

# Izbor jezika na samom vrhu stranice
st.markdown("🌐 **Jezik / Language / Idioma / Sprache**<br>🇷🇸 | 🇬🇧 | 🇪🇸 | 🇩🇪", unsafe_allow_html=True)
jezik = st.selectbox("Izbor jezika", ["Srpski", "English", "Español", "Deutsch"], label_visibility="collapsed")

# --- REČNIK FIKSNIH TEKSTOVA ZA SVE JEZIKE ---
if jezik == "English":
    t_naslov, t_podnaslov = "♠️♥️Diet Diary♦️♣️", "mineral levels tracking with daily intake sum"
    t_napomena1 = "⚠️ *Mineral values are expressed in milligrams (mg) per 100 grams of cleaned, raw food.*"
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg | Sodium max 1500-2000mg*"
    t_korak1 = "🔍 Step 1: Click and type a letter to find food (A-Z sorted):"
    t_okvir_baza = "Values per 100g -> "
    t_korak2 = "⚖️ Step 2: Enter the amount of food consumed (in grams):"
    t_dugme_dodaj = "➕ Add meal to my diary"
    t_naslov_tabele = "📋 Your daily diet log and entered meals"
    t_zbir_okvir = "📊 TOTAL DAILY SUM OF ALL ENTERED MEALS:"
    t_dugme_obrisi = "🗑️ Clear complete diary"
    t_dugme_pdf = "📄 Download PDF report"
    t_placeholder_ime = "e.g. John Doe"
    t_labela_ime = "Name and surname:"
    t_uputstvo_brisanje = "💡 <b>How to delete:</b> Check the box next to the food item, then click the trash can icon (top right above the table) or press <b>DELETE</b> on your keyboard."
    t_labela_godina = "Year of birth:"
    t_placeholder_godina = "e.g. 1965"


    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Food Item', 'Amount (g)', 'Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)'
    ime_kolone_baza = 'Namirnica_EN'
    t_labela_unos = "Amount in grams"
elif jezik == "Español":
    t_naslov, t_podnaslov = "♠️♥️Diario de Alimentación♦️♣️", "seguimiento de minerales con suma de ingesta diaria"
    t_napomena1 = "⚠️ *Los valores de minerales se expresan in miligramos (mg) por cada 100 gramos de alimento limpio y crudo.*"
    t_napomena2 = "ⓘ *Ingesta diaria recomendada: Potasio 1200-1500mg | Fósforo 800-1000mg | Sodio máx 1500-2000mg*"
    t_korak1 = "🔍 Paso 1: Busque un alimento en la lista (Ordenado A-Z):"
    t_okvir_baza = "Valores por 100g -> "
    t_korak2 = "⚖️ Paso 2: Ingrese la cantidad de alimento (en gramos):"
    t_dugme_dodaj = "➕ Añadir comida a mi diario"
    t_naslov_tabele = "📋 Su registro diario de dieta y comidas ingresadas"
    t_zbir_okvir = "📊 SUMA TOTAL DIARIA DE TODAS LAS COMIDAS INGRESADAS:"
    t_dugme_obrisi = "🗑️ Vaciar diario completo"
    t_dugme_pdf = "📄 Descargar informe PDF"
    t_placeholder_ime = "por ejemplo, Juan Pérez"
    t_labela_ime = "Nombre y apellido del paciente:"
    t_uputstvo_brisanje = "💡 <b>Cómo eliminar:</b> Marque la casilla al lado del alimento, luego haga clic en el icono del cubo de basura (arriba a la derecha de la tabla) o presione <b>DELETE</b> en el teclado."
    t_labela_ime = "Nombre y apellido:"
    t_labela_godina = "Año de nacimiento:"
    t_placeholder_godina = "por ejemplo, 1965"


    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Alimento', 'Cantidad (g)', 'Potasio (mg)', 'Fósforo (mg)', 'Sodio (mg)'
    ime_kolone_baza = 'Namirnica_ES'
    t_labela_unos = "Cantidad en gramos"
elif jezik == "Deutsch":
    t_naslov, t_podnaslov = "♠️♥️Ernährungstagebuch♦️♣️", "Überwachung des Mineralstoffgehalts mit täglicher Gesamtaufnahme"
    t_napomena1 = "⚠️ *Die Mineralstoffwerte sind in Milligramm (mg) pro 100 Gramm gereinigter, roher Lebensmittel angegeben.*"
    t_napomena2 = "ⓘ *Empfohlene tägliche Aufnahme: Kalium 1200-1500mg | Phosphor 800-1000mg | Natrium max 1500-2000mg*"
    t_korak1 = "🔍 Schritt 1: Lebensmittel aus der Liste auswählen (A-Z sortiert):"
    t_okvir_baza = "Werte pro 100g -> "
    t_korak2 = "⚖️ Schritt 2: Verzehrte Menge in Gramm eingeben:"
    t_dugme_dodaj = "➕ Mahlzeit hinzufügen"
    t_naslov_tabele = "📋 Ihr tägliches Ernährungsprotokoll und eingegebene Mahlzeiten"
    t_zbir_okvir = "📊 TÄGLICHE GESAMTSUMME ALLER EINGEGEBENEN MAHLZEITEN:"
    t_dugme_obrisi = "🗑️ Tagebuch leeren"
    t_dugme_pdf = "📄 PDF-Bericht herunterladen"
    t_placeholder_ime = "z.B. Max Mustermann"
    t_labela_ime = "Name und Vorname:"
    t_uputstvo_brisanje = "💡 <b>Anleitung zum Löschen:</b> Markieren Sie das Kästchen neben dem Lebensmittel, klicken Sie dann auf das Mülleimer-Symbol (oben rechts über der Tabelle) oder drücken Sie <b>DELETE</b> auf der Tastatur."
    t_labela_godina = "Geburtsjahr:"
    t_placeholder_godina = "z.B. 1965"


    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
    t_labela_unos = "Menge in Gramm"
else:
    t_naslov, t_podnaslov = "♠️♥️Dnevnik Ishrane♦️♣️", "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg | Natrijum max 1500-2000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu (Lista je sortirana po abecedi A-Z)"
    t_okvir_baza = "Vrednosti na 100g -> "
    t_korak2 = "⚖️ Korak 2: Upišite količinu namirnice u gramima"
    t_dugme_dodaj = "➕ Dodaj obrok u moj dnevnik"
    t_naslov_tabele = "📋 Vaš današnji dnevnik ishrane i uneti obroci"
    t_zbir_okvir = "📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:"
    t_dugme_obrisi = "🗑️ Isprazni kompletan dnevnik"
    t_dugme_pdf = "📄 Preuzmi PDF izveštaj"
    t_placeholder_ime = "npr. Petar Petrović"
    t_labela_ime = "Ime i prezime:"
    t_uputstvo_brisanje = "💡 <b>Uputstvo za brisanje:</b> Čekirajte kvadrat ispred naziva namirnice, pa kliknite na kantu za smeće (gore desno iznad tabele) ili pritisnite <b>DELETE</b> na tastaturi."
    t_labela_godina = "Godina rođenja:"
    t_placeholder_godina = "npr. 1965"


    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Namirnica', 'Količina (g)', 'Kalijum (mg)', 'Fosfor (mg)', 'Natrijum (mg)'
    ime_kolone_baza = 'Namirnica'
    t_labela_unos = "Količina u gramima"

# Prikaz naslova aplikacije
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}<br><span style='font-size: 22px; font-weight: normal;'>{t_podnaslov}</span></h1>", unsafe_allow_html=True)
st.write(t_napomena1)
st.write(t_napomena2)

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    try:
        df_baza = pd.read_excel("KPH-AI-GLOBAL.xlsx")
        df_baza.columns = ['Namirnica', 'Namirnica_EN', 'Namirnica_ES', 'Namirnica_DE', 'Kalijum', 'Fosfor', 'Natrijum']
        return df_baza
    except:
        return None

df = ucitaj_bazu()

# --- FUNKCIJA ZA KREIRANJE PDF-a ---
def generisi_pdf_file(ime_pacijenta, godina_rodjenja, df_podaci, uk_k, uk_f, uk_n):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=False, margin=5)

    # 1. Užo zeleno polje na vrhu
    pdf.set_fill_color(46, 204, 113)
    pdf.rect(0, 0, 210, 17, "F")

    # LOGO
    pdf.image('QRF.png', x=175, y=3, w=20)

    
    # Naslov unutar zelene trake
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(180, 11, text="DNEVNIK ISHRANE & UNOSA MINERALA", border=0, ln=1, align="C")
    
    # Vraćamo tekst na tamno sivu
    pdf.set_text_color(44, 62, 80)
    pdf.ln(5) 
    
       # 2. Blok sa podacima - Siva pozadina (povećana visina na 22 sa 16 zbog novog reda)
    pdf.set_fill_color(205, 212, 218) 
        
            # 1. Eksplicitno postavljamo kursor na visinu 27 (ispod zelenog zaglavlja)
    pdf.set_y(27)
    
    # Ispis tekstova IZNAD sive trake (Normal font, crna boja)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(120, 5, text="Ime i prezime / godina rodjenja:", border=0, ln=0)
    pdf.cell(60, 5, text="Datum:", border=0, ln=1, align="R")
    
    # 2. Spuštamo kursor na visinu 32 gde počinje siva traka
    pdf.set_y(32)
    
    # Crtanje sive trake (od visine 32 do visine 44 -> ukupna visina je 12mm)
    pdf.set_fill_color(205, 212, 218) 
    pdf.rect(15, 32, 180, 12, "F")
    
    # Ispis podataka UNUTAR sive trake (Bold font, visina ćelije pronalazi centar trake)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(120, 12, text=f" {ime_pacijenta.upper()} ({godina_rodjenja})", border=0, ln=0)
    pdf.cell(60, 12, text=f"{datetime.now().strftime('%d.%m.%Y.')} ", border=0, ln=1, align="R")
    
    # 3. Postavljamo kursor na visinu 48 kako bi tabela počela tačno ispod sive trake
    pdf.set_y(48)




    # 3. Tabela obroka (Zeleno-sivo zaglavlje)
    pdf.set_font("Courier", "", 10)
    pdf.set_fill_color(52, 73, 94) 
    pdf.set_text_color(255, 255, 255) 
    
    
        # FORMAT TABELE 1 (Smanjena visina na 5 da odgovara podacima)
    pdf.cell(65, 5, text=" Namirnica", border=0, fill=True)
    pdf.cell(25, 5, text="Kolicina (g)", border=0, fill=True, align="C")
    pdf.cell(30, 5, text="Kalijum (mg)", border=0, fill=True, align="C")
    pdf.cell(30, 5, text="Fosfor (mg)", border=0, fill=True, align="C")
    pdf.cell(30, 5, text="Natrijum (mg)", border=0, fill=True, align="C")

    pdf.ln()
    
    pdf.set_text_color(44, 62, 80)
    pdf.set_font("Helvetica", size=10)


    
    
    brojac_reda = 0
    for _, red in df_podaci.iterrows():
        if brojac_reda % 2 == 0:
            pdf.set_fill_color(248, 250, 252) 
            is_fill = True
        else:
            is_fill = False
            
        pdf.cell(65, 5, text=f" {str(red['food'])[:28]}", border="B", fill=is_fill)
        pdf.cell(25, 5, text=f"{red['amount']:.1f} g", border="B", fill=is_fill, align="C")
        pdf.cell(30, 5, text=f"{red['potassium']:.1f}", border="B", fill=is_fill, align="C")
        pdf.cell(30, 5, text=f"{red['phosphorus']:.1f}", border="B", fill=is_fill, align="C")
        pdf.cell(30, 5, text=f"{red['sodium']:.1f}", border="B", fill=is_fill, align="C")


        pdf.ln()
        brojac_reda += 1
        
    pdf.ln(10)


    #TABELA REZIME
    pdf.cell(180, 8, "REZIME UKUPNOG DNEVNOG UNOSA:", 0, 1)
    pdf.ln(2)
    
    pdf.set_font("Courier", "", 10)
    pdf.set_fill_color(230, 235, 240)
    # Smanjena visina zaglavlja sa 8 na 5.5
    pdf.cell(40, 5.5, " Mineral", 1, 0, "C", True)
    pdf.cell(45, 5.5, "Ukupno uneto", 1, 0, "C", True)
    pdf.cell(45, 5.5, "Preporuceni limit", 1, 0, "C", True)
    pdf.cell(50, 5.5, "Status", 1, 1, "C", True)
    
    pdf.set_font("Courier", "", 10)
    
    # Kalijum (Smanjena visina sa 8 na 5.5)
    pdf.cell(40, 5.5, " Kalijum", 1)
    pdf.cell(45, 5.5, f"{uk_k:.2f} mg", 1, 0, "C")
    pdf.cell(45, 5.5, "1500.00 mg", 1, 0, "C")
    if uk_k > 1500.0:
        pdf.set_text_color(231, 76, 60)
        pdf.set_font("Courier", "", 10)
        pdf.cell(50, 5.5, " Prekoraceno", 1, 1, "C")
    else:
        pdf.set_text_color(39, 174, 96)
        pdf.cell(50, 5.5, " [OK] U granicama", 1, 1, "C")
    pdf.set_text_color(44, 62, 80)
    pdf.set_font("Courier", "", 10)
    
    # Fosfor (Smanjena visina sa 8 na 5.5)
    pdf.cell(40, 5.5, " Fosfor", 1)
    pdf.cell(45, 5.5, f"{uk_f:.2f} mg", 1, 0, "C")
    pdf.cell(45, 5.5, "1000.00 mg", 1, 0, "C")
    if uk_f > 1000.0:
        pdf.set_text_color(231, 76, 60)
        pdf.set_font("Courier", "", 10)
        pdf.cell(50, 5.5, " Prekoraceno", 1, 1, "C")
    else:
        pdf.set_text_color(39, 174, 96)
        pdf.cell(50, 5.5, " [OK] U granicama", 1, 1, "C")
    pdf.set_text_color(44, 62, 80)
    pdf.set_font("Courier", "", 10)
    
    # Natrijum (Smanjena visina sa 8 na 5.5)
    pdf.cell(40, 5.5, " Natrijum", 1)
    pdf.cell(45, 5.5, f"{uk_n:.2f} mg", 1, 0, "C")
    pdf.cell(45, 5.5, "2000.00 mg", 1, 0, "C")
    if uk_n > 2000.0:
        pdf.set_text_color(231, 76, 60)
        pdf.set_font("Courier", "", 10)
        pdf.cell(50, 5.5, " Prekoraceno", 1, 1, "C")
    else:
        pdf.set_text_color(39, 174, 96)
        pdf.cell(50, 5.5, " [OK] U granicama", 1, 1, "C")

    pdf.set_text_color(44, 62, 80)
    pdf.set_font("Courier", "", 10)
    pdf.ln(12)

    # Pozicioniramo kursor za legendu visoko (na prvu stranu)
    pdf.set_y(-60)
    
    # Legenda
    pdf.set_font("Courier", "U", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(180, 5, "LEGENDA - GRANICNE VREDNOSTI (24h):", 0, 1)
    
    pdf.set_font("Courier", "", 8)
    pdf.cell(180, 4, "* KALIJUM:  Zelena boja = do 1500.00 mg  |  Crvena boja ! = preko 1500.00 mg", 0, 1)
    pdf.cell(180, 4, "* FOSFOR:   Zelena boja = do 1000.00 mg  |  Crvena boja ! = preko 1000.00 mg", 0, 1)
    pdf.cell(180, 4, "* NATRIJUM: Zelena boja = do 2000.00 mg  |  Crvena boja ! = preko 2000.00 mg (oko 5g soli)", 0, 1)

    
            # === REŠENJE ZA FUTER ===
    # Pravimo fiksni razmak na dole od 15mm nakon legende, tako da ostane na istoj strani
    pdf.ln(15) 
    
    # 1. Postavljanje fonta za futer
    pdf.set_font("Courier", "", 8)

    # 2. Ispis teksta BEZ osenčene pozadine (fill=False)
    # Prvi red sa informativnim medicinskim odricanjem
    pdf.cell(0, 8, "Izvestaj generisan putem AI je informativnog karaktera i ne predstavlja medicinski savet.", 0, 1, "C", fill=False)

    # 3. Podešavanje sive boje pozadine SAMO za drugi red
    pdf.set_fill_color(205, 212, 218)

    # 4. Ispis SA sivom pozadinom (fill=True)
    # Drugi red sa vašim potpisom i kontaktom
    pdf.cell(0, 8, "Written by MAGICOMP magicom@bluewin.ch +38163310850 | Powered by Python", 0, 1, "C", fill=True)

    # 5. Poništavanje (vraćanje na standardni font za sve što ide posle)
    pdf.set_font("Helvetica", "", 9)

    # OVE 4 LINIJE GENERIŠU PDF BUFFER:
    pdf.set_text_color(44, 62, 80)
    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

    # KRAJ FUTERA



# --- GLAVNI RENDER STRANICE ---
if df is not None:
    df_sortirano = df.dropna(subset=[ime_kolone_baza]).sort_values(by=ime_kolone_baza)
    kompletna_lista = df_sortirano[ime_kolone_baza].tolist()
    
    st.write("---")
    st.subheader(t_korak1)
    
    izbor = st.selectbox("👇", kompletna_lista, key="trenutni_izbor", label_visibility="collapsed")
    
    trenutni_red = df[df[ime_kolone_baza] == izbor]
    if not trenutni_red.empty:
        k_100 = float(trenutni_red['Kalijum'].values[0])
        f_100 = float(trenutni_red['Fosfor'].values[0])
        n_100 = float(trenutni_red['Natrijum'].values[0])
        
        k_boja = "#FF4B4B" if k_100 > 200.0 else "#2ECC71"
        f_boja = "#FF4B4B" if f_100 > 150.0 else "#2ECC71"
        n_boja = "#FF4B4B" if n_100 > 400.0 else "#2ECC71"
        
        st.markdown(f"""
        <div style='background-color: #1e2430; padding: 12px; border-left: 4px solid #2ECC71; border-radius: 4px; color: #ffffff; font-weight: bold; font-size: 15px;'>
            {t_okvir_baza} 
            <span style='color: {k_boja};'>{l_kalijum}: {k_100:.0f} mg</span> | 
            <span style='color: {f_boja};'>{l_fosfor}: {f_100:.0f} mg</span> | 
            <span style='color: {n_boja};'>{l_natrijum}: {n_100:.0f} mg</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader(t_korak2)
    
    kolicina_g = st.number_input(t_labela_unos, min_value=1.0, max_value=5000.0, value=100.0, step=10.0, label_visibility="collapsed", key="trenutna_kolicina")
    
    st.write("")
    
    if st.button(t_dugme_dodaj):
        red_dodaj = df[df[ime_kolone_baza] == izbor]
        if not red_dodaj.empty:
            k_d = float(red_dodaj['Kalijum'].values[0])
            f_d = float(red_dodaj['Fosfor'].values[0])
            n_d = float(red_dodaj['Natrijum'].values[0])
            
            st.session_state['dnevnik_obroka'].append({
                'food': izbor,
                'amount': kolicina_g,
                'potassium': round((k_d * kolicina_g) / 100.0, 2),
                'phosphorus': round((f_d * kolicina_g) / 100.0, 2),
                'sodium': round((n_d * kolicina_g) / 100.0, 2)
            })
            st.rerun()

    #=========================POCETAK TABELE DNEVNOG UNOSA NAMIRNICA==================================
    if st.session_state['dnevnik_obroka']:
        st.write("---")
        st.subheader(t_naslov_tabele)
        
        df_prikaz = pd.DataFrame(st.session_state['dnevnik_obroka'])
        
        # Privremeno dodajemo indeks kao kolonu da bismo znali šta brišemo
        df_prikaz['ID'] = df_prikaz.index
        
        df_prikaz_prevedeno = df_prikaz.rename(columns={
            'food': l_namirnica,
            'amount': l_kolicina,
            'potassium': l_kalijum,
            'phosphorus': l_fosfor,
            'sodium': l_natrijum
        })
        
        # Rekonstruišemo raspored kolona (ID ide prvi ali ga krijemo)
        kolone_redosled = ['ID', l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum]
        df_prikaz_prevedeno = df_prikaz_prevedeno[kolone_redosled]
        
        # PRIKAZ TABELE KROZ DATA_EDITOR SA OPCIJOM BRISANJA REDOVA
        izmenjeni_df = st.data_editor(
            df_prikaz_prevedeno,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",  # Ovo omogućava brisanje redova
            disabled=[l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum], # Sprečava menjanje teksta, dozvoljava samo brisanje
            column_config={"ID": None}  # Potpuno sakriva ID kolonu od korisnika
        )

        # Uputstvo za brisanja 
        
        st.markdown(f"""
<p style='color: #ffffff; font-size: 16px; line-height: 1.4; margin-top: 10px;'>
{t_uputstvo_brisanje}
</p>
""", unsafe_allow_html=True)
        # KRAJ Uputstva za brisanje

        # Ako je korisnik obrisao neki red, ažuriramo session_state
        if len(izmenjeni_df) != len(df_prikaz_prevedeno):
            preostali_id_lista = izmenjeni_df['ID'].tolist()
            st.session_state['dnevnik_obroka'] = [
                st.session_state['dnevnik_obroka'][i] for i in preostali_id_lista
            ]
            st.rerun()

# KRAJ Uputstvo za brisanje
            
        # Računanje ukupnih vrednosti iz trenutnog stanja
        uk_k = df_prikaz['potassium'].sum()
        uk_f = df_prikaz['phosphorus'].sum()
        uk_n = df_prikaz['sodium'].sum()
        
        st.write("")
        st.markdown(f"### {t_zbir_okvir}")
        
        dnevna_k_boja = "#FF4B4B" if uk_k > 1500.0 else "#2ECC71"
        dnevna_f_boja = "#FF4B4B" if uk_f > 1000.0 else "#2ECC71"
        dnevna_n_boja = "#FF4B4B" if uk_n > 2000.0 else "#2ECC71"
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div style='background-color: #1e2430; padding: 12px; border-radius: 6px; text-align: center; border-top: 3px solid {dnevna_k_boja};'>
                <p style='margin: 0px; color: #a0aec0; font-size: 15px; font-weight: bold;'>{l_kalijum}</p>
                <p style='margin: 5px 0px 0px 0px; color: {dnevna_k_boja}; font-size: 22px; font-weight: 900;'>{uk_k:.2f} mg</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div style='background-color: #1e2430; padding: 12px; border-radius: 6px; text-align: center; border-top: 3px solid {dnevna_f_boja};'>
                <p style='margin: 0px; color: #a0aec0; font-size: 15px; font-weight: bold;'>{l_fosfor}</p>
                <p style='margin: 5px 0px 0px 0px; color: {dnevna_f_boja}; font-size: 22px; font-weight: 900;'>{uk_f:.2f} mg</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div style='background-color: #1e2430; padding: 12px; border-radius: 6px; text-align: center; border-top: 3px solid {dnevna_n_boja};'>
                <p style='margin: 0px; color: #a0aec0; font-size: 15px; font-weight: bold;'>{l_natrijum}</p>
                <p style='margin: 5px 0px 0px 0px; color: {dnevna_n_boja}; font-size: 22px; font-weight: 900;'>{uk_n:.2f} mg</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("---")
   # POLJA ZA UNOS PODATAKA DIREKTNO NA EKRANU
        col_inp1, col_inp2 = st.columns(2)
        with col_inp1:
            st.markdown(f"**{t_labela_ime}**")
            ime_pacijenta = st.text_input("Ime", placeholder=t_placeholder_ime, label_visibility="collapsed")
        with col_inp2:
            st.markdown(f"**{t_labela_godina}**")
            godina_rodjenja = st.text_input("Godina", placeholder=t_placeholder_godina, label_visibility="collapsed")

# KRAJ CMD ZA UNOS PODATAKA

        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if ime_pacijenta and godina_rodjenja:
                try:
                    pdf_bytes = generisi_pdf_file(ime_pacijenta, godina_rodjenja, df_prikaz, uk_k, uk_f, uk_n)
                    st.download_button(
                        label=t_dugme_pdf,
                        data=pdf_bytes,
                        file_name=f"Izvestaj_{ime_pacijenta.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Greska: {e}")
            else:
                st.button(t_dugme_pdf, disabled=True, use_container_width=True)
        with col_btn2:
            if st.button(t_dugme_obrisi, use_container_width=True):
                st.session_state['dnevnik_obroka'] = []
                st.rerun()
else:
    st.error("Baza podataka 'KPH-AI-GLOBAL.xlsx' nije pronađena ili je oštećena.")
    
#=========================KRAJ TABELE DNEVNOG UNOSA NAMIRNICA==================================

# --- UVOZ BIBLIOTEKA (MORA BITI NA POČETKU BLOKA) ---
import os
import streamlit as st

# --- LOGIKA ZA INTERNI BROJAČ POSETA ---
ime_fajla = "brojac.txt"
pocetni_broj = 3002

if 'poseta_uracunata' not in st.session_state:
    if not os.path.exists(ime_fajla):
        with open(ime_fajla, "w") as f:
            f.write(str(pocetni_broj))
        trenutni_broj = pocetni_broj
    else:
        with open(ime_fajla, "r") as f:
            try:
                trenutni_broj = int(f.read().strip()) + 1
            except:
                trenutni_broj = pocetni_broj
        with open(ime_fajla, "w") as f:
            f.write(str(trenutni_broj))
    st.session_state['poseta_uracunata'] = trenutni_broj
else:
    if os.path.exists(ime_fajla):
        with open(ime_fajla, "r") as f:
            try:
                trenutni_broj = int(f.read().strip())
            except:
                trenutni_broj = pocetni_broj
    else:
        trenutni_broj = pocetni_broj

# --- FUTER SA DINAMIČKIM BROJAČEM POSETA ---
st.write("---")

st.markdown(f"""
<div style='text-align: center; line-height: 1.2;'>
    <p style='margin: 0px; color: #ffffff; font-size: 14px;'>Ukupno poseta aplikaciji: <span style='color: #2ECC71; font-weight: bold;'>{trenutni_broj}</span></p>
    <p style='margin: 5px 0px 0px 0px; font-weight: bold; color: #ffffff;'>♣️♦️♥️♠️ MAGICOMP & AI Gemini</p>
    <p style='margin: 0px; color: #279FF5;'>magy@usa.com &nbsp;&nbsp;|&nbsp;&nbsp; Tel.+38163310850</p>
    <p style='margin: 0px;  color: #888888; font-size: 12px;'>Powered by PYTHON</p>
</div>
""", unsafe_allow_html=True)
