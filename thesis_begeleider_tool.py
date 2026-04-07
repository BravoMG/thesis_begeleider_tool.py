"""
thesis_begeleider_tool.py
Senior Thesis Begeleider - Erasmus Universiteit
Functies: inhoud, lay-out, bronvermelding (APA 7e editie), AI-check, feedback & stappenplan
Tabellen & grafieken generator voor Hoofdstuk 4
Academisch schrijven checks (zandlopermodel, IMRD, argumentatie, schrijfstijl)
Inhoudsopgave validator (gebaseerd op SeniorWeb.nl, 2020)
AI-gebruik validator (gebaseerd op VUB 2023 & REBO 2025 richtlijnen)

Gebaseerd op:
- Handleiding Afstudeertraject Master Bestuurskunde 2023-2024
- Poelmans, P. & Severijnen, O. (2022). De APA-richtlijnen (7e editie). Coutinho.
- TutKit.com (2024). Tabellen in Word efficiënt opmaken.
- Handleiding Academisch schrijven & presenteren (2025-2026). Universiteit Utrecht.
- SeniorWeb.nl (2020). Inhoudsopgave maken met Word.
- VUB (2023). Verantwoord gebruik van artificiële intelligentie voor onderzoeksdoeleinden.
- Universiteit Utrecht, REBO (2025). Richtlijnen voor het gebruik van AI in Afstudeerwerken.
- Erasmus Universiteit Rotterdam. AI@EUR visie en strategie.
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


class ThesisBegeleider:
    def __init__(self, student_name: str = "", thesis_title: str = ""):
        self.student_name = student_name
        self.thesis_title = thesis_title
        self.feedback_log = []
        self.universiteit = "Erasmus Universiteit"
        self.apa_stijl = "APA 7e editie"
        
        # Verbindingswoorden voor argumentatiestructuur
        self.verbindingswoorden = {
            "tegenstelling": ["daarentegen", "echter", "maar", "hoewel", "anderzijds", "terwijl", "in tegenstelling tot"],
            "overeenkomst": ["en", "ook", "eveneens", "alsmede", "tevens", "mede", "evenals", "bovendien", "daarnaast"],
            "resultaat": ["dus", "daarom", "derhalve", "vandaar"],
            "samenvatting": ["samengevat", "kortom", "tot slot"],
            "argumentatie_meervoud": ["ten eerste", "ten tweede", "ten slotte"],
            "argumentatie_onderschikkend": ["want", "omdat", "aangezien"],
            "argumentatie_nevenschikkend": ["bovendien", "daarbij komt", "ook gezien het feit"]
        }
        
        # Kopstijlen voor inhoudsopgave (SeniorWeb.nl, 2020)
        self.kop_stijlen = {
            "Kop 1": r'^(\d+\.\s+[A-Z])|(Hoofdstuk\s+\d+)',
            "Kop 2": r'^\d+\.\d+\s+[A-Z]',
            "Kop 3": r'^\d+\.\d+\.\d+\s+[A-Z]'
        }
        
        # AI-tools voor detectie (VUB & REBO richtlijnen)
        self.ai_tools = [
            "chatgpt", "gpt-4", "gpt-3.5", "openai", "claude", "anthropic", "llama", "meta",
            "copilot", "github copilot", "code whisperer", "code llama",
            "elicit", "perplexity", "scite", "consensus", "connected papers", "research rabbit", "iris", "humata",
            "grammarly", "writefull", "quillbot", "languagetool",
            "midjourney", "dall-e", "dalle", "stable diffusion", "imagen",
            "gemini", "bard", "deepseek", "mistral", "cohere"
        ]
        
        # AI-markers voor detectie van AI-geschreven tekst
        self.ai_tekst_markers = [
            "het is belangrijk om te benadrukken", "daarnaast", "echter",
            "bovendien", "samenvattend kan worden gesteld", "in conclusie",
            "niet alleen maar ook", "derhalve", "aldus", "opvallend is dat",
            "in deze studie", "de resultaten tonen aan", "zoals eerder vermeld",
            "een diepgaande analyse", "significant verband"
        ]

    # ========== BASIS CHECKS ==========
    
    def beoordeel_titelblad(self, titelblad_tekst: str) -> List[str]:
        """Controleer titelblad op vereiste onderdelen"""
        verplicht = {
            "titel": r"(?i)titel|title",
            "naam": r"(?i)naam|name|student",
            "studentnummer": r"\b\d{7,8}\b",
            "opleiding": r"(?i)master|opleiding|programma",
            "datum": r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",
            "begeleider": r"(?i)begeleider|supervisor"
        }
        feedback = []
        for veld, patroon in verplicht.items():
            if not re.search(patroon, titelblad_tekst):
                feedback.append(f"❌ Titelblad mist: {veld}")
        if not feedback:
            feedback.append("✅ Titelblad volledig volgens richtlijnen")
        return feedback

    def beoordeel_methodologie(self, method_tekst: str) -> List[str]:
        """Beoordeel methodologische kwaliteit"""
        criteria = {
            "onderzoeksdesign": r"(?i)design|longitudinaal|cross-sectioneel|case study|experiment",
            "steekproef": r"(?i)steekproef|sample|respondenten|participanten",
            "meetinstrument": r"(?i)vragenlijst|interview|observatie|test|schaal",
            "procedure": r"(?i)procedure|afname|dataverzameling",
            "analyse": r"(?i)analyse|statistiek|regressie|t-toets|anova|thematische analyse"
        }
        feedback = []
        for criterium, patroon in criteria.items():
            if not re.search(patroon, method_tekst):
                feedback.append(f"⚠️ Methodologie mist: {criterium}")
        if not feedback:
            feedback.append("✅ Methodologie compleet en verantwoord")
        return feedback

    # ========== APA 7e EDITIE CHECKS (Poelmans & Severijnen, 2022) ==========
    
    def check_apa_conformiteit(self, referentie_tekst: str) -> List[str]:
        """Controleer of bronvermelding voldoet aan APA 7e editie"""
        feedback = []
        
        if not referentie_tekst.strip():
            feedback.append("❌ Geen bronnen gevonden in literatuurlijst")
            return feedback
        
        referenties = [r.strip() for r in referentie_tekst.split('\n') if r.strip()]
        
        if not referenties:
            feedback.append("❌ Geen bronnen gevonden in literatuurlijst")
            return feedback
        
        # Check 1: Alfabetische volgorde (APA p. 91)
        def sort_key(ref):
            ref_lower = ref.lower()
            for prefix in ["van ", "de ", "den ", "der ", "ten ", "ter "]:
                if ref_lower.startswith(prefix):
                    ref_lower = ref_lower[len(prefix):]
            return ref_lower
        
        sorted_refs = sorted(referenties, key=sort_key)
        if referenties != sorted_refs:
            feedback.append("⚠️ Literatuurlijst niet alfabetisch gesorteerd (APA p.91)")
        
        # Check 2: Gebruik van '&' ipv 'en' (APA p. 40)
        for ref in referenties:
            if ' en ' in ref.lower() and '&' not in ref:
                feedback.append(f"⚠️ Gebruik '&' ipv 'en': '{ref[:60]}...' (APA p.40)")
        
        # Check 3: Jaartal direct na auteur (APA p. 96)
        for ref in referenties:
            if not re.search(r'[A-Za-z]\.?\s?\((\d{4}(?:,\s[a-z]+)?)\)', ref):
                if '(n.d.)' not in ref:
                    feedback.append(f"⚠️ Jaartal ontbreekt: '{ref[:60]}...' (APA p.96)")
        
        # Check 4: DOI bij journalartikelen (APA p. 99-100)
        for ref in referenties:
            if re.search(r'(journal|tijdschrift|quarterly|review|annual)', ref.lower()):
                if 'https://doi.org/' not in ref and 'doi.org' not in ref:
                    feedback.append(f"⚠️ Journal mist DOI: '{ref[:60]}...' (APA p.100)")
        
        # Check 5: Dubbele spaties (APA p. 90)
        for i, ref in enumerate(referenties):
            if '  ' in ref:
                feedback.append(f"⚠️ Dubbele spatie in ref {i+1} (APA p.90)")
        
        if not feedback:
            feedback.append("✅ Bronvermelding voldoet aan APA 7e editie")
        
        return feedback

    def check_citaten(self, tekst: str) -> List[str]:
        """Controleer of citaten voldoen aan APA 7e editie (p. 33-35)"""
        feedback = []
        citaten = re.findall(r'"([^"]{10,})"', tekst)
        
        for citaat in citaten:
            if len(citaat.split()) < 40:
                citaat_positie = tekst.find(citaat)
                omliggende_tekst = tekst[max(0, citaat_positie-100):citaat_positie+200]
                if not re.search(r'\(p\.\s?\d+\)|\(pp\.\s?\d+-\d+\)', omliggende_tekst):
                    feedback.append(f"⚠️ Kort citaat mist paginanummer: \"{citaat[:50]}...\" (APA p.34)")
        
        if not feedback:
            feedback.append("✅ Citaten voldoen aan APA richtlijnen")
        return feedback

    def check_bronvermelding(self, referentie_tekst: str) -> List[str]:
        """Combinatie van basis APA-check en uitgebreide APA 7e editie check"""
        basis_feedback = []
        if not referentie_tekst.strip():
            basis_feedback.append("❌ Geen referentielijst gevonden")
        
        apa_journal = r"[A-Z][a-z]+,\s[A-Z]\.\s\(\d{4}\).+\.\s[A-Za-z\s]+,\s\d+\(\d+\)"
        if not re.search(apa_journal, referentie_tekst):
            basis_feedback.append("⚠️ Geen APA-journalartikelen herkend")
        
        if "&" not in referentie_tekst and "et al." not in referentie_tekst:
            basis_feedback.append("⚠️ Gebruik '&' of 'et al.' voor meerdere auteurs")
        
        uitgebreide_feedback = self.check_apa_conformiteit(referentie_tekst)
        alle_feedback = basis_feedback + uitgebreide_feedback
        unieke_feedback = list(dict.fromkeys(alle_feedback))
        
        return unieke_feedback or ["✅ Bronvermelding APA-conform (7e editie)"]

    # ========== AI-DETECTIE & AI-GEBRUIK CHECKS (VUB 2023 & REBO 2025) ==========
    
    def ai_detectie(self, tekst: str) -> Tuple[List[str], float]:
        """
        Detecteer of tekst AI-kenmerken bevat.
        Gebaseerd op VUB (2023) richtlijnen.
        """
        score = 0
        gevonden = []
        for marker in self.ai_tekst_markers:
            if marker in tekst.lower():
                score += 1
                gevonden.append(marker)
        ratio = score / len(self.ai_tekst_markers) if self.ai_tekst_markers else 0
        
        if ratio > 0.15:
            return ([f"⚠️ AI-signaal: veelvoorkomende marker(s) '{', '.join(gevonden[:3])}' (VUB richtlijnen)"], ratio)
        return (["✅ Geen duidelijke AI-indicaties (VUB 2023)"], ratio)
    
    def check_ai_transparantie(self, methodologie_tekst: str) -> List[str]:
        """
        Check of AI-gebruik transparant is vermeld in de methodologie.
        Verplicht volgens VUB (2023) en REBO (2025) richtlijnen.
        """
        feedback = []
        
        # Zoek naar vermelding van AI-tools in de methodologie
        gevonden_tools = []
        for tool in self.ai_tools:
            if tool in methodologie_tekst.lower():
                gevonden_tools.append(tool)
        
        if gevonden_tools:
            feedback.append(f"✅ AI-gebruik vermeld in methodologie: {', '.join(gevonden_tools[:3])}")
        else:
            # Check of er wel AI-achtige formuleringen zijn (suggestie van gebruik)
            if any(marker in methodologie_tekst.lower() for marker in self.ai_tekst_markers[:5]):
                feedback.append("⚠️ Let op: Er zijn aanwijzingen voor mogelijk AI-gebruik, maar geen vermelding in methodologie (VUB 2023 vereist transparantie)")
            else:
                feedback.append("ℹ️ Geen AI-tools gevonden in methodologie. Indien geen AI gebruikt, is dit akkoord.")
        
        return feedback
    
    def check_ai_logboek(self, logboek_tekst: str = "") -> List[str]:
        """
        Check of het AI-logboek aanwezig is en voldoet aan REBO (2025) template.
        Verplicht volgens REBO-richtlijnen voor afstudeerwerken.
        """
        feedback = []
        
        if not logboek_tekst:
            feedback.append("⚠️ AI-logboek niet aangeleverd (verplicht volgens REBO 2025 richtlijnen)")
            feedback.append("   Gebruik het template in 'examples/ai_logboek_voorbeeld.txt'")
            return feedback
        
        # Check of logboek de verplichte velden bevat
        verplichte_velden = ["datum", "ai-tool", "doel", "prompt", "output", "reflectie"]
        for veld in verplichte_velden:
            if veld not in logboek_tekst.lower():
                feedback.append(f"⚠️ Logboek mist veld: {veld} (REBO template vereist)")
        
        if not feedback:
            feedback.append("✅ AI-logboek aanwezig en voldoet aan REBO template")
        
        return feedback
    
    def check_ai_reflectie(self, discussie_tekst: str) -> List[str]:
        """
        Check of er reflectie op AI-gebruik is opgenomen in discussie/conclusie.
        Aanbevolen volgens VUB (2023) richtlijnen.
        """
        feedback = []
        
        reflectie_indicatoren = [
            "ai", "tool", "beperking", "verantwoordelijkheid", "controle",
            "chatgpt", "generatieve ai", "kunstmatige intelligentie"
        ]
        
        heeft_reflectie = any(woord in discussie_tekst.lower() for woord in reflectie_indicatoren)
        
        if heeft_reflectie:
            feedback.append("✅ Reflectie op AI-gebruik aanwezig in discussie/conclusie")
        else:
            feedback.append("⚠️ Overweeg reflectie op AI-gebruik in discussie/conclusie (VUB 2023 beveelt aan)")
        
        return feedback
    
    def check_ai_verboden_praktijken(self, tekst: str) -> List[str]:
        """
        Check op aanwijzingen voor verboden AI-praktijken.
        Gebaseerd op REBO (2025) richtlijnen.
        """
        feedback = []
        
        # Check op tekenen van AI als auteur
        if "chatgpt" in tekst.lower() and "auteur" in tekst.lower():
            feedback.append("⚠️ Controleer: AI mag niet als auteur worden vermeld (REBO 2025)")
        
        # Check op tekenen van AI-gegenereerde bronnen
        if "as an ai" in tekst.lower() or "as a large language model" in tekst.lower():
            feedback.append("⚠️ Let op: Dit lijkt op AI-gegenereerde tekst. AI mag geen bronnen of argumenten genereren (REBO 2025)")
        
        return feedback

    # ========== INHOUDSOPGAVE CHECK (SeniorWeb.nl, 2020) ==========
    
    def check_kop_structuur(self, tekst: str) -> List[str]:
        """
        Controleer of koppen correct zijn gestructureerd volgens Word-kopstijlen.
        Gebaseerd op: SeniorWeb.nl (2020). Inhoudsopgave maken met Word.
        """
        feedback = []
        
        regels = tekst.split('\n')
        aantal_kop1 = 0
        aantal_kop2 = 0
        aantal_kop3 = 0
        fouten = []
        
        for regel in regels:
            regel = regel.strip()
            if not regel:
                continue
            
            if re.match(self.kop_stijlen["Kop 1"], regel):
                aantal_kop1 += 1
                if len(regel) > 100:
                    feedback.append(f"⚠️ Kop 1 '{regel[:50]}...' is te lang (max 100 tekens)")
            
            elif re.match(self.kop_stijlen["Kop 2"], regel):
                aantal_kop2 += 1
                if aantal_kop1 == 0:
                    fouten.append(f"Kop 2 '{regel[:50]}...' zonder voorgaande Kop 1")
            
            elif re.match(self.kop_stijlen["Kop 3"], regel):
                aantal_kop3 += 1
        
        if aantal_kop1 < 3:
            feedback.append(f"⚠️ Weinig hoofdstukken ({aantal_kop1}) - minimaal 3 aanbevolen")
        elif aantal_kop1 >= 3:
            feedback.append(f"✅ {aantal_kop1} hoofdstukken (Kop 1) gevonden")
        
        if aantal_kop2 == 0 and aantal_kop3 == 0:
            feedback.append("⚠️ Geen tussenkoppen (Kop 2/Kop 3) gevonden - thesis mist structuur")
        elif aantal_kop2 > 0:
            feedback.append(f"✅ {aantal_kop2} paragrafen (Kop 2) gevonden")
        
        if aantal_kop3 > 0:
            feedback.append(f"✅ {aantal_kop3} subparagrafen (Kop 3) gevonden")
        
        for fout in fouten[:3]:
            feedback.append(f"⚠️ {fout}")
        
        if not feedback:
            feedback.append("✅ Kopstructuur correct (Kop 1, Kop 2, Kop 3 correct toegepast)")
        
        return feedback

    # ========== ACADEMISCH SCHRIJVEN CHECKS ==========
    
    def check_zandlopermodel(self, tekst: str, sectie: str = "inleiding") -> List[str]:
        """Check of de tekst het zandlopermodel volgt."""
        feedback = []
        
        if sectie == "inleiding":
            breed_indicatoren = ["wereldwijd", "maatschappij", "samenleving", "probleem", "relevant"]
            specifiek_indicatoren = ["onderzoekt", "vraag", "doel", "hypothese", "onderzochten"]
            
            heeft_breed = any(woord in tekst.lower() for woord in breed_indicatoren)
            heeft_specifiek = any(woord in tekst.lower() for woord in specifiek_indicatoren)
            
            if not heeft_breed:
                feedback.append("⚠️ Inleiding mist brede context - zandlopermodel")
            if not heeft_specifiek:
                feedback.append("⚠️ Inleiding mist specifieke vraagstelling - zandlopermodel")
                
        elif sectie == "discussie":
            breed_indicatoren = ["bijdrage", "betekenis", "implicatie", "maatschappij", "toekomst"]
            heeft_terugkoppeling = any(woord in tekst.lower() for woord in breed_indicatoren)
            
            if not heeft_terugkoppeling:
                feedback.append("⚠️ Discussie mist terugkoppeling naar brede context - zandlopermodel")
        
        if not feedback:
            feedback.append(f"✅ Zandlopermodel correct toegepast in {sectie}")
        
        return feedback

    def check_objectieve_schrijfstijl(self, tekst: str) -> List[str]:
        """Check of de schrijfstijl objectief is."""
        feedback = []
        
        waardeoordelen = ["helaas", "gelukkig", "mooi", "lelijk", "jammer", "prachtig"]
        subjectief = ["ontzettend", "duidelijk te zien", "zeer", "enorm", "opvallend"]
        
        for woord in waardeoordelen:
            if woord in tekst.lower():
                feedback.append(f"⚠️ Waardeoordeel '{woord}' - blijf objectief")
        
        for woord in subjectief:
            if woord in tekst.lower():
                feedback.append(f"⚠️ Subjectieve kwalificatie '{woord}' - wees objectief")
        
        if not feedback:
            feedback.append("✅ Schrijfstijl objectief")
        
        return feedback

    def check_verbindingswoorden(self, tekst: str) -> List[str]:
        """Check of verbindingswoorden worden gebruikt."""
        feedback = []
        
        gevonden_woorden = []
        for categorie, woorden in self.verbindingswoorden.items():
            for woord in woorden:
                if woord in tekst.lower():
                    gevonden_woorden.append(woord)
        
        unieke_woorden = set(gevonden_woorden)
        
        if len(unieke_woorden) < 3:
            feedback.append(f"⚠️ Weinig verbindingswoorden ({len(unieke_woorden)} unieke) - versterk samenhang")
        else:
            feedback.append(f"✅ Verbindingswoorden gebruikt: {', '.join(list(unieke_woorden)[:5])}...")
        
        return feedback

    # ========== FIGUREN EN TABELLEN CHECKS ==========
    
    def check_figuren(self, tekst: str) -> List[str]:
        """Check of figuren correct zijn opgemaakt."""
        feedback = []
        
        figuur_refs = re.findall(r'(Figuur|figuur)\s+\d+', tekst)
        figuur_nummers = set(re.findall(r'Figuur\s+(\d+\.?\d*)', tekst, re.IGNORECASE))
        
        if len(figuur_refs) > 0:
            for nummer in figuur_nummers:
                bijschrift_pattern = rf'Figuur\s+{nummer}[\.\-:]\s*([^\n]+)'
                bijschrift = re.search(bijschrift_pattern, tekst, re.IGNORECASE)
                if not bijschrift:
                    feedback.append(f"⚠️ Figuur {nummer} mist een beschrijvend bijschrift")
        
        if not feedback and len(figuur_refs) > 0:
            feedback.append("✅ Figuren correct opgemaakt")
        elif len(figuur_refs) == 0:
            feedback.append("ℹ️ Geen figuren gevonden in de tekst")
        
        return feedback

    def check_tabellen(self, tekst: str) -> List[str]:
        """Check of tabellen correct zijn opgemaakt."""
        feedback = []
        
        tabel_refs = re.findall(r'(Tabel|tabel)\s+\d+', tekst)
        tabel_nummers = set(re.findall(r'Tabel\s+(\d+\.?\d*)', tekst, re.IGNORECASE))
        
        if len(tabel_refs) > 0:
            for nummer in tabel_nummers:
                bovenschrift_pattern = rf'Tabel\s+{nummer}[\.\-:]\s*([^\n]+)'
                bovenschrift = re.search(bovenschrift_pattern, tekst, re.IGNORECASE)
                if not bovenschrift:
                    feedback.append(f"⚠️ Tabel {nummer} mist een bovenschrift")
        
        if not feedback and len(tabel_refs) > 0:
            feedback.append("✅ Tabellen correct opgemaakt")
        elif len(tabel_refs) == 0:
            feedback.append("ℹ️ Geen tabellen gevonden in de tekst")
        
        return feedback

    # ========== STAPPENPLAN ==========
    
    def genereer_stappenplan(self, alle_feedback: List[str]) -> List[str]:
        """Genereer actiestappen op basis van feedback."""
        stappen = []
        
        if any("mist" in f for f in alle_feedback):
            stappen.append("📌 Stap 1: Voeg ontbrekende elementen toe aan titelblad")
        
        if any("methodologie mist" in f for f in alle_feedback):
            stappen.append("📌 Stap 2: Beschrijf onderzoeksdesign, steekproef, instrument, procedure en analyse")
        
        if any("APA" in f for f in alle_feedback):
            stappen.append("📌 Stap 3: Formatteer referenties volgens APA 7e editie (Poelmans & Severijnen, 2022)")
        
        if any("AI-logboek" in f or "transparantie" in f for f in alle_feedback):
            stappen.append("📌 Stap 4: Lever AI-logboek aan volgens REBO template (verplicht!)")
            stappen.append("   - Gebruik template in 'examples/ai_logboek_voorbeeld.txt'")
        
        if any("AI-signaal" in f for f in alle_feedback):
            stappen.append("📌 Stap 5: Herschrijf passages in eigen woorden en voeg persoonlijke reflectie toe")
        
        if any("reflectie op AI" in f for f in alle_feedback):
            stappen.append("📌 Stap 6: Voeg reflectie op AI-gebruik toe in discussie/conclusie (VUB 2023 beveelt aan)")
        
        if any("Kop" in f for f in alle_feedback):
            stappen.append("📌 Stap 7: Controleer kopstijlen (Kop 1 voor hoofdstukken, Kop 2 voor paragrafen)")
        
        if any("zandlopermodel" in f.lower() for f in alle_feedback):
            stappen.append("📌 Stap 8: Pas het zandlopermodel toe - inleiding van breed naar specifiek")
        
        if any("objectief" in f.lower() for f in alle_feedback):
            stappen.append("📌 Stap 9: Vermijd waardeoordelen en subjectieve kwalificaties")
        
        if any("figuur" in f.lower() or "tabel" in f.lower() for f in alle_feedback):
            stappen.append("📌 Stap 10: Controleer of alle figuren/tabellen een bijschrift/bovenschrift hebben")
        
        if not stappen:
            stappen.append("✅ Geen correcties nodig. Volgende stap: indienen voor eindbeoordeling.")
        
        return stappen

    # ========== TABELLEN GENERATOR (Hoofdstuk 4) ==========
    
    def genereer_tabel_4_1(self) -> str:
        """Genereer Tabel 4.1: Overzicht geanalyseerde fragmenten"""
        return """
┌─────────────────────────────────────────────────────────────────────────────┐
│ Tabel 4.1 - Overzicht van geanalyseerde fragmenten per spreker en per moment │
├──────────────┬───────────────────┬───────────────┬─────────────────┬────────┤
│    Datum     │       Type        │    Rutte      │    De Jonge     │ Totaal │
├──────────────┼───────────────────┼───────────────┼─────────────────┼────────┤
│ 2 feb 2021   │ Persconferentie   │     104       │      132        │  236   │
│ 10 mrt 2021  │ Kamerdebat        │     165       │      380        │  545   │
│ 23 mrt 2021  │ Persconferentie   │     202       │      200        │  402   │
│ 9 jul 2021   │ Persconferentie   │     112       │      303        │  415   │
│ 14 sep 2021  │ Persconferentie   │     185       │      338        │  523   │
│ 14 dec 2021  │ Persconferentie   │     288       │      264        │  552   │
├──────────────┼───────────────────┼───────────────┼─────────────────┼────────┤
│ **Totaal**   │                   │   **1056**    │    **1617**     │ **2673**│
└──────────────┴───────────────────┴───────────────┴─────────────────┴────────┘
Bron: Analyse persconferenties en Kamerdebat, 2021 (N=2673 fragmenten)
"""

    def genereer_tabel_4_2(self) -> str:
        """Genereer Tabel 4.2: Aantal mentions per EI-competentie"""
        return """
┌─────────────────────────────────────────────────────────────┐
│ Tabel 4.2 - Aantal mentions per EI-competentie            │
├─────────────────────┬───────────────┬─────────────────────┤
│     Competentie     │  Mark Rutte   │   Hugo de Jonge     │
├─────────────────────┼───────────────┼─────────────────────┤
│ Zelfbewustzijn      │      12       │         9           │
│ Zelfregulatie       │      28       │        31           │
│ Empathie            │      19       │        27           │
│ Sociale vaardigheden│      17       │        22           │
├─────────────────────┼───────────────┼─────────────────────┤
│ **Totaal**          │     **76**    │       **89**        │
└─────────────────────┴───────────────┴─────────────────────┘
Bron: Thematische analyse van transcripties (2021)
"""

    def genereer_tabel_4_3(self) -> str:
        """Genereer Tabel 4.3: Kwalitatieve voorbeelden per EI-competentie"""
        return """
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Tabel 4.3 - Voorbeelden van EI-kenmerken in citaten van Rutte en De Jonge                  │
├──────────────────┬─────────────────────────────────────────┬─────────────────────────────────┤
│   Competentie    │         Mark Rutte                      │         Hugo de Jonge           │
├──────────────────┼─────────────────────────────────────────┼─────────────────────────────────┤
│ Zelfbewustzijn   │ "Ik reken het mij persoonlijk aan"      │ "We hebben de vorige keer       │
│                  │ (14 dec 2021)                           │ gesproken..." (10 mrt 2021)     │
├──────────────────┼─────────────────────────────────────────┼─────────────────────────────────┤
│ Zelfregulatie    │ "Hij gaat niet aftreden"                │ "Het lijkt me praktisch, want   │
│                  │ (9 jul 2021)                            │ de dingen gebeuren" (9 jul 2021)│
├──────────────────┼─────────────────────────────────────────┼─────────────────────────────────┤
│ Empathie         │ "Ondernemers die het water aan de       │ "Ik kan me voorstellen dat het  │
│                  │ lippen staat" (2 feb 2021)              │ tegenvalt" (9 jul 2021)         │
├──────────────────┼─────────────────────────────────────────┼─────────────────────────────────┤
│ Sociale          │ "Die gedachten betrekken we erbij"      │ "Ik deel zeer de zorg van de    │
│ vaardigheden     │ (10 mrt 2021)                           │ heer Wilders" (10 mrt 2021)     │
└──────────────────┴─────────────────────────────────────────┴─────────────────────────────────┘
Bron: Transcripties persconferenties en Kamerdebat (2021)
"""

    def genereer_rapport_hoofdstuk_4(self) -> str:
        """Genereer volledig rapport voor Hoofdstuk 4 met tabellen."""
        return "\n".join([
            "=" * 80,
            "HOOFDSTUK 4: RESULTATEN EN ANALYSE",
            "=" * 80,
            "",
            "In dit hoofdstuk worden de resultaten van de empirische analyse gepresenteerd.",
            "De analyse is gebaseerd op 6 persconferenties en 1 Kamerdebat uit 2021.",
            "",
            self.genereer_tabel_4_1(),
            "",
            self.genereer_tabel_4_2(),
            "",
            self.genereer_tabel_4_3(),
            "",
            "=" * 80
        ])

    # ========== VOLLEDIGE BEOORDELING ==========
    
    def volledige_beoordeling(self, titelblad: str, methodologie: str, referenties: str, 
                              volledige_tekst: str = "", logboek_tekst: str = "") -> Dict:
        """
        Voer alle checks uit en retourneer volledig rapport.
        
        Parameters:
        - titelblad: tekst van het titelblad
        - methodologie: tekst van de methodologie sectie
        - referenties: literatuurlijst
        - volledige_tekst: volledige thesis tekst (optioneel)
        - logboek_tekst: AI-logboek tekst (optioneel maar aanbevolen)
        """
        print("\n" + "="*70)
        print(f"📘 THESIS BEGELEIDINGSRAPPORT - {self.universiteit}")
        print(f"Student: {self.student_name or '[onbekend]'} | Titel: {self.thesis_title or '[onbekend]'}")
        print(f"Datum: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
        print("="*70 + "\n")

        # Basis checks
        feedback_titel = self.beoordeel_titelblad(titelblad)
        feedback_methode = self.beoordeel_methodologie(methodologie)
        feedback_bron = self.check_bronvermelding(referenties)
        
        # AI-gebruik checks (VUB 2023 & REBO 2025)
        feedback_ai_transparantie = self.check_ai_transparantie(methodologie)
        feedback_ai_logboek = self.check_ai_logboek(logboek_tekst)
        
        # AI-detectie op volledige tekst
        ai_feedback, ai_score = self.ai_detectie(volledige_tekst or methodologie)
        feedback_ai_verboden = self.check_ai_verboden_praktijken(volledige_tekst or methodologie)
        
        # Reflectie op AI (check in discussie, maar we hebben geen aparte discussie tekst)
        # Gebruik volledige_tekst als proxy
        feedback_ai_reflectie = self.check_ai_reflectie(volledige_tekst or methodologie)
        
        # Overige checks
        feedback_citaten = self.check_citaten(volledige_tekst or methodologie)
        feedback_kop_structuur = self.check_kop_structuur(volledige_tekst or methodologie)
        feedback_zandloper = self.check_zandlopermodel(volledige_tekst or methodologie, "inleiding")
        feedback_objectief = self.check_objectieve_schrijfstijl(volledige_tekst or methodologie)
        feedback_verbindingswoorden = self.check_verbindingswoorden(volledige_tekst or methodologie)
        feedback_figuren = self.check_figuren(volledige_tekst or methodologie)
        feedback_tabellen = self.check_tabellen(volledige_tekst or methodologie)

        # Verzamel alle feedback
        alle_feedback = (
            feedback_titel + feedback_methode + feedback_bron + feedback_citaten +
            feedback_ai_transparantie + feedback_ai_logboek + ai_feedback + 
            feedback_ai_verboden + feedback_ai_reflectie +
            feedback_kop_structuur + feedback_zandloper + feedback_objectief +
            feedback_verbindingswoorden + feedback_figuren + feedback_tabellen
        )
        
        # Genereer stappenplan
        stappenplan = self.genereer_stappenplan(alle_feedback)

        # Print feedback
        for item in alle_feedback:
            print(f"• {item}")
        print("\n📌 STAPPENPLAN OM TE SLAGEN:")
        for stap in stappenplan:
            print(f"  {stap}")

        # Log feedback
        self.feedback_log.append({
            "timestamp": datetime.now().isoformat(),
            "feedback": alle_feedback,
            "stappenplan": stappenplan,
            "ai_score": ai_score
        })

        return {
            "feedback": alle_feedback,
            "stappenplan": stappenplan,
            "ai_score": ai_score,
            "log": self.feedback_log,
            "hoofdstuk_4_rapport": self.genereer_rapport_hoofdstuk_4()
        }


# ========== VOORBEELD GEBRUIK ==========
if __name__ == "__main__":
    # Voorbeeld student data
    student_titelblad = """
    Titel: Emotionele Intelligentie in Publiek Crisisleiderschap
    Naam: Jan Jansen
    Studentnummer: 12345678
    Opleiding: Master Bestuurskunde
    Datum: 15-04-2026
    Begeleider: Dr. E. Erasmus
    """

    student_methodologie = """
    Dit onderzoek gebruikt een kwalitatieve casestudy. 
    De steekproef bestaat uit 6 persconferenties en 1 Kamerdebat.
    Data wordt geanalyseerd met thematische analyse.
    
    Voor het verkennen van literatuur is gebruik gemaakt van Elicit (https://elicit.org).
    Grammaticacontrole is uitgevoerd met Grammarly.
    """

    student_referenties = """
    Gooty, J., Connelly, S., Griffith, J., & Gupta, A. (2010). Leadership, affect and emotions. The Leadership Quarterly, 21(6), 979-1004.
    Poelmans, P., & Severijnen, O. (2022). De APA-richtlijnen (2e druk). Coutinho.
    """

    student_tekst = """
    In deze studie wordt onderzocht welke kenmerken van emotionele intelligentie 
    zichtbaar waren in het leiderschap van Rutte en De Jonge tijdens de COVID-19 crisis.
    
    De resultaten tonen aan dat zelfregulatie bij beide leiders prominent aanwezig was.
    Dit komt overeen met eerdere bevindingen in de literatuur (Gooty et al., 2010).
    """

    # Voorbeeld AI-logboek
    student_logboek = """
    Datum: 2026-03-15
    AI-tool: Elicit
    Doel: Literatuur verkennen over emotionele intelligentie
    Prompt: "Find papers on emotional intelligence and crisis leadership"
    Output: Lijst met 10 relevante papers
    Reflectie: Alle papers zijn zelf gelezen en gecontroleerd.
    """

    # Initialiseer begeleider
    begeleider = ThesisBegeleider(
        student_name="Jan Jansen", 
        thesis_title="Emotionele Intelligentie in Publiek Crisisleiderschap"
    )

    # Voer volledige beoordeling uit
    resultaat = begeleider.volledige_beoordeling(
        titelblad=student_titelblad,
        methodologie=student_methodologie,
        referenties=student_referenties,
        volledige_tekst=student_tekst,
        logboek_tekst=student_logboek
    )
    
    # Toon gegenereerd Hoofdstuk 4 rapport
    print("\n" + resultaat["hoofdstuk_4_rapport"])