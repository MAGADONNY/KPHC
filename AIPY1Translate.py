import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import io

st.title("🤖 Super-Preprevodilac baze (SR ➡️ EN ➡️ ES ➡️ DE)")

@st.cache_data
def ucitaj_bazu():
    try:
        # Čitamo fajl direktno sa prve linije jer je baza idealno očišćena
        df = pd.read_excel("KPH-AI.xlsx")
        df.columns = ['Namirnica', 'Kalijum', 'Fosfor', 'Natrijum']
        df = df.dropna(subset=['Namirnica'])
        return df
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    st.write(f"📊 Originalna čista baza uspešno učitana. Ukupno ima **{len(df)}** namirnica za obradu.")
    
    if st.button("🚀 POKRENI KOMPLETAN PREVOD NA SVA 3 JEZIKA"):
        progres_bar = st.progress(0)
        status_tekst = st.empty()
        
        prevodi_en = []
        prevodi_es = []
        prevodi_de = []
        ukupno = len(df)
        
        for i, n in enumerate(df['Namirnica'].tolist()):
            pojam = str(n).strip()
            status_tekst.text(f"Obrađujem ({i+1}/{ukupno}): {pojam}")
            
            if pojam and pojam != "nan":
                # Pametno peglanje kulinarskih reči pre slanja na Google mrežu
                t = pojam.lower()
                if "curetina" in t: t = t.replace("curetina", "ćuretina")
                if "skembici" in t: t = t.replace("skembici", "škembići")
                if "juneci" in t: t = t.replace("juneci", "juneći")
                if "karabatak" in t: t = t.replace("karabatak", "thigh")
                if "batak" in t: t = t.replace("batak", "drumstick")
                tekst_za_prevod = t.capitalize()
                
                # 1. Prevod na Engleski (en)
                try:
                    p_en = GoogleTranslator(source='sr', target='en').translate(tekst_za_prevod)
                    p_en = p_en.replace("Drumstick, drumstick", "Drumstick").replace("Thigh, thigh", "Thigh")
                    prevodi_en.append(p_en)
                except:
                    prevodi_en.append(pojam)
                    
                # 2. Prevod na Španski (es)
                try:
                    p_es = GoogleTranslator(source='sr', target='es').translate(tekst_za_prevod)
                    prevodi_es.append(p_es)
                except:
                    prevodi_es.append(pojam)
                    
                # 3. Prevod na Nemački (de)
                try:
                    p_de = GoogleTranslator(source='sr', target='de').translate(tekst_za_prevod)
                    prevodi_de.append(p_de)
                except:
                    prevodi_de.append(pojam)
            else:
                prevodi_en.append("")
                prevodi_es.append("")
                prevodi_de.append("")
                
            progres_bar.progress((i + 1) / ukupno)
            
        # Kreiramo novi, čisti DataFrame sa savršenim globalnim rasporedom kolona
        novi_df = pd.DataFrame({
            'Namirnica': df['Namirnica'].tolist(),
            'Namirnica_EN': prevodi_en,
            'Namirnica_ES': prevodi_es,
            'Namirnica_DE': prevodi_de,
            'Kalijum': df['Kalijum'].tolist(),
            'Fosfor': df['Fosfor'].tolist(),
            'Natrijum': df['Natrijum'].tolist()
        })
        
        st.success("✅ Generisanje savršene globalne baze je završeno!")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            novi_df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        
        st.download_button(
            label="📥 PREUZMI SVETSKU EXCEL BAZU",
            data=processed_data,
            file_name="KPH-AI-Svetska.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.error("❌ Greška: Proverite da li se čist fajl 'KPH-AI.xlsx' nalazi na vašem GitHub-u.")
