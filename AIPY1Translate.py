import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

st.title("🤖 Automatski prevodilac cele Excel baze")

@st.cache_data
def ucitaj_bazu():
    try:
        return pd.read_excel("KPH-AI.xlsx", header=1)
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    # Automatski dodeljujemo imena kolonama ako nisu ispravna
    if len(df.columns) >= 4:
        df.columns = ['Namirnica', 'Kalijum', 'Fosfor', 'Natrijum'] + list(df.columns[4:])
    else:
        df.columns = ['Namirnica', 'Kalijum', 'Fosfor', 'Natrijum']

    st.write(f"📊 Tabela je uspešno učitana. Ukupno ima **{len(df)}** namirnica za prevod.")
    
    if st.button("🚀 POKRENI AUTOMATSKI PREVOD CELE BAZE"):
        progres_bar = st.progress(0)
        status_tekst = st.empty()
        
        lista_prevoda = []
        ukupno = len(df)
        
        for i, n in enumerate(df['Namirnica'].tolist()):
            status_tekst.text(f"Prevođenje: {n}")
            try:
                # Sređujemo bazične kulinarske pojmove pre slanja Google-u
                t = str(n).lower()
                if "curetina" in t: t = t.replace("curetina", "ćuretina")
                if "skembici" in t: t = t.replace("skembici", "škembići")
                if "juneci" in t: t = t.replace("juneci", "juneći")
                if "karabatak" in t: t = t.replace("karabatak", "thigh")
                if "batak" in t: t = t.replace("batak", "drumstick")
                
                prevod = GoogleTranslator(source='sr', target='en').translate(t.capitalize())
                prevod = prevod.replace("Drumstick, drumstick", "Drumstick").replace("Thigh, thigh", "Thigh")
                lista_prevoda.append(prevod)
            except:
                lista_prevoda.append(n) # Ako pukne net, ostavlja original
                
            progres_bar.progress((i + 1) / ukupno)
            
        df.insert(1, 'Namirnica_EN', lista_prevoda)
        st.success("✅ Prevod je uspešno završen!")
        
        # Pretvaranje u Excel format za preuzimanje
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        
        st.download_button(
            label="📥 PREUZMI PREVEDENI EXCEL FAJL",
            data=processed_data,
            file_name="KPH-AI-Prevedeno.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.error("❌ Program ne može da pronađe fajl 'KPH-AI.xlsx' u vašem folderu na GitHub-u.")
