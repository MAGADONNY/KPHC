import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import io

st.title("🤖 Globalni prevodilac baze (SR ➡️ EN ➡️ ES ➡️ DE)")

@st.cache_data
def ucitaj_bazu():
    try:
        # Čitamo fajl bez preskakanja zaglavlja jer je struktura već definisana
        df = pd.read_excel("KPH-AI.xlsx")
        return df
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    # Osiguravamo da prva kolona uvek bude preimenovana u 'Namirnica' radi stabilnosti skripte
    df.rename(columns={df.columns[0]: 'Namirnica'}, inplace=True)
    
    st.write(f"📊 Učitano je **{len(df)}** namirnica.")
    
    if st.button("🚀 POKRENI AUTOMATSKI PREVOD NA ŠPANSKI I NEMAČKI"):
        progres_bar = st.progress(0)
        status_tekst = st.empty()
        
        prevodi_es = []
        prevodi_de = []
        ukupno = len(df)
        
        for i, n in enumerate(df['Namirnica'].tolist()):
            pojam_za_slanje = str(n).strip()
            status_tekst.text(f"Prevođenje ({i+1}/{ukupno}): {pojam_za_slanje}")
            
            if pojam_za_slanje and pojam_za_slanje != "nan":
                # Sređivanje pre slanja Google-u
                t = pojam_za_slanje.lower()
                if "curetina" in t: t = t.replace("curetina", "ćuretina")
                if "skembici" in t: t = t.replace("skembici", "škembići")
                if "juneci" in t: t = t.replace("juneci", "juneći")
                if "karabatak" in t: t = t.replace("karabatak", "thigh")
                if "batak" in t: t = t.replace("batak", "drumstick")
                pojam = t.capitalize()
                
                # Prevod na Španski (es)
                try:
                    p_es = GoogleTranslator(source='sr', target='es').translate(pojam)
                    prevodi_es.append(p_es)
                except:
                    prevodi_es.append(pojam_za_slanje)
                    
                # Prevod na Nemački (de)
                try:
                    p_de = GoogleTranslator(source='sr', target='de').translate(pojam)
                    prevodi_de.append(p_de)
                except:
                    prevodi_de.append(pojam_za_slanje)
            else:
                prevodi_es.append("")
                prevodi_de.append("")
                
            progres_bar.progress((i + 1) / ukupno)
            
        # Bezbedno ubacivanje novih kolona na tačna mesta u tabeli
        if 'Namirnica_ES' in df.columns:
            df['Namirnica_ES'] = prevodi_es
        else:
            df.insert(2, 'Namirnica_ES', prevodi_es)
            
        if 'Namirnica_DE' in df.columns:
            df['Namirnica_DE'] = prevodi_de
        else:
            df.insert(3, 'Namirnica_DE', prevodi_de)
            
        st.success("✅ Prevod na španski i nemački uspešno završen!")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        
        st.download_button(
            label="📥 PREUZMI GLOBALNU EXCEL BAZU",
            data=processed_data,
            file_name="KPH-AI-Global.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.error("❌ Program ne može da pronađe ili pročita fajl 'KPH-AI.xlsx' na GitHub-u.")
