# Wanderlust AI – Kelionių Agentūros Pokalbių Robotas (Chatbot)

## 1. Įvadas
Šis projektas yra **taisyklėmis paremtas (rule-based) pokalbių robotas (chatbot)**, sukurtas imituoti kelionių agentūros konsultantą. Sistema sukurta nuo nulio, nenaudojant jokių iš anksto paruoštų pokalbių platformų (tokių kaip DialogFlow ar Rasa).
Vartotojo sąsajai įgyvendinti naudojama **Streamlit** biblioteka, o tekstų atpažinimui ir logikai – **Python** ir **reguliariosios išraiškos (Regular Expressions - Regex)**.

---

## 2. Techninis Įgyvendinimas

### 2.1. Metodas
Pasirinktas metodas: **Taisyklių rinkinys (Rule-based system)** su reguliariosiomis išraiškomis.
Sistema nenaudoja mašininio mokymosi modelių, o remiasi **griežta logine struktūra**. Tai užtikrina tikslius ir nuspėjamus atsakymus į specifines užklausas (pvz., vizų reikalavimai ar valiuta), pašalinant "haliucinacijų" riziką, būdingą generatyviniams modeliams.

### 2.2. Architektūra (*travel\_bot.py*)
* **Klasė `RuleBasedChatbot`:** Pagrindinis variklis, kuriame saugoma visa logika ir duomenų bazės.
* **Būsenos valdymas (State Machine):** Naudojamas `self.context`, kad robotas "prisimintų" pokalbio kontekstą. Tai leidžia vykdyti **kelių žingsnių dialogus** (pvz., kuriant kelionės paketą: Šalis -> Žmonių skaičius -> Biudžetas -> Trukmė).
* **Žinių bazė:** Vidiniuose žodynuose (**Python dictionaries**) saugoma informacija apie:
    * Lankytinas vietas (`country_attractions`)
    * Vizų taisykles (pvz., Šengeno zona, JAV ESTA)
    * Šalių informaciją (valiuta, arbatpinigiai, geriausias laikas)
    * Vidutines kainas ir pakavimo sąrašus.
* **Vartotojo sąsaja:** Moderni, tamsaus stiliaus sąsaja, sukurta su **Streamlit**, pritaikyta mobiliems įrenginiams.

---

## 3. Funkcionalumas (Palaikomi klausimų tipai)
Chatbotas geba atsakyti į daugiau nei **5 skirtingų kategorijų** klausimus:

* **Kelionės paketų sudarymas (Travel Packages):**
    * Užklausa: *"Create a travel package for Poland"*
    * Logika: Robotas surenka informaciją apie biudžetą ir žmonių skaičių, tada apskaičiuoja optimalią kelionės trukmę pagal vidutinius tos šalies kaštus.
* **Vizų reikalavimai (Visa Requirements):**
    * Užklausa: *"Do I need a visa from USA to Japan?"*
    * Logika: Tikrina kilmės ir tikslo šalis. Atpažįsta Šengeno zoną, bevizius režimus ir specifinius reikalavimus (pvz., ESTA, E-Visa).
* **Lankytinos vietos (Tourist Attractions):**
    * Užklausa: *"What to visit in France?"*
    * Logika: Pateikia populiariausių objektų sąrašą pasirinktoje šalyje.
* **Šalies specifika (Local Info):**
    * Užklausos: 
        * "What is the currency in Turkey?" (Valiuta)
        * "Do I need to tip in USA?" (Arbatpinigiai)
        * "Best time to visit Thailand?" (Sezoniškumas)
        * "What language is spoken in Lithuania?" (Kalba)
* **Pakavimo patarimai (Packing Advice):**
    * Užklausa: *"What to pack for Iceland?"*
    * Logika: Analizuoja šalies klimatą (šaltas/karštas) ir pateikia atitinkamą daiktų sąrašą (pvz., termo drabužiai Islandijai, kremas nuo saulės Tailandui).
* **Rekomendacijos (Suggestions):**
    * Užklausa: *"Suggest a beach trip"*
    * Logika: Pasiūlo kryptį pagal kategoriją (paplūdimys, kalnai, miestas, pigios kelionės).

---

## 4. Diegimas ir Paleidimas
Norint paleisti programą, reikalinga Python aplinka.

Įdiekite priklausomybes:
pip install streamlit

Paleiskite aplikaciją:
streamlit run travel_bot.py

## 5. Testavimas
Sukurta **unittest** pagrindu veikianti testavimo sistema (*test\_bot.py*), kuri patikrina visas pagrindines funkcijas, užtikrindama, kad robotas teisingai interpretuoja užklausas ir grąžina laukiamus atsakymus.
Darbas atliktas **savarankiškai**, naudojant Python ir Streamlit technologijas.
