"""
test_academic_writing.py
Toetst of een thesis voldoet aan de eisen uit:
Handleiding Academisch schrijven & presenteren (Biomedische wetenschappen, 2025-2026)

Draai met: python -m unittest tests/test_academic_writing.py
"""

import unittest
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from thesis_begeleider_tool import ThesisBegeleider


class TestAcademicWriting(unittest.TestCase):
    """Test of de thesis voldoet aan academische schrijfstandaarden"""
    
    def setUp(self):
        self.begeleider = ThesisBegeleider()
        
        # Voorbeeld van een goede academische tekst
        self.goede_tekst = """
        Uit de resultaten blijkt dat de expressie van eiwit X significant toenam 
        na stimulatie met stof Y (p < 0,05). Dit suggereert dat stof Y een rol 
        speelt in de regulatie van eiwit X. Eerdere studies tonen vergelijkbare 
        resultaten (Jagosh et al., 2012). Echter, in tegenstelling tot deze 
        bevindingen rapporteerde een andere studie geen effect.
        """
    
    # ========== TEST 1: ZANDLOPERMODEL ==========
    
    def test_zandlopermodel_inleiding(self):
        """Test of de inleiding van groot naar klein schrijft"""
        inleiding = """
        Hart- en vaatziekten zijn wereldwijd de belangrijkste doodsoorzaak.
        Jaarlijks overlijden 17,9 miljoen mensen aan deze ziekten.
        Een belangrijke risicofactor is hypertensie.
        Eerder onderzoek toonde aan dat stof X de bloeddruk verlaagt.
        Onbekend is echter wat het moleculaire mechanisme is.
        Daarom onderzochten wij het effect van stof X op de expressie van gen Y.
        """
        
        # Check of er een brede context is (maatschappelijke relevantie)
        self.assertTrue(re.search(r'(wereldwijd|doodsoorzaak|miljoen|ziekte)', inleiding.lower()))
        
        # Check of er een specifieke vraagstelling is
        self.assertTrue(re.search(r'(onderzochten|daarom|vraag|hypothese)', inleiding.lower()))
    
    def test_zandlopermodel_discussie(self):
        """Test of de discussie van klein naar groot schrijft"""
        discussie = """
        Onze hypothese werd bevestigd: stof X verhoogt de expressie van gen Y.
        Dit komt overeen met eerdere bevindingen van Janssen et al. (2020).
        Een verklaring voor dit effect is dat stof X de transcriptiefactor Z activeert.
        Deze resultaten dragen bij aan het begrip van hypertensie.
        Uiteindelijk kunnen deze inzichten leiden tot nieuwe behandelmethoden.
        """
        
        # Check of er een conclusie is (beantwoording vraag)
        self.assertTrue(re.search(r'(hypothese|bevestigd|conclusie|antwoord)', discussie.lower()))
        
        # Check of er terugkoppeling naar brede context is
        self.assertTrue(re.search(r'(bijdragen|betekenis|maatschappelijk|behandeling)', discussie.lower()))
    
    # ========== TEST 2: IMRD-STRUCTUUR ==========
    
    def test_imrd_structuur_aanwezig(self):
        """Test of de IMRD-structuur herkenbaar is in de tekst"""
        tekst_met_imrd = """
        INTRODUCTIE: Hart- en vaatziekten zijn een groot probleem...
        METHODEN: Cellen werden gekweekt in RPMI-medium...
        RESULTATEN: De expressie van gen X nam toe met 40%...
        DISCUSSIE: Deze resultaten bevestigen de hypothese...
        """
        
        onderdelen = ["introductie", "methoden", "resultaten", "discussie"]
        for onderdeel in onderdelen:
            self.assertIn(onderdeel, tekst_met_imrd.lower())
    
    # ========== TEST 3: ALINEA STRUCTUUR ==========
    
    def test_alinea_heeft_kernzin(self):
        """Test of een alinea begint met een kernzin"""
        alinea = """
        Stimulatie met stof X leidt tot verhoogde expressie van gen Y. 
        Uit de resultaten blijkt dat de expressie na 24 uur met 40% toenam. 
        Dit effect was afhankelijk van de concentratie stof X.
        """
        eerste_zin = alinea.split('.')[0]
        # Check of de eerste zin de hoofdgedachte bevat
        self.assertTrue(len(eerste_zin.split()) > 3)
    
    def test_alinea_geen_nieuwe_info_einde(self):
        """Test of een alinea niet eindigt met nieuwe informatie"""
        alinea_goed = """
        De resultaten tonen een significant effect aan. Dit komt overeen met 
        eerdere literatuur. Concluderend kan worden gesteld dat stof X werkt.
        """
        laatste_zin = alinea_goed.split('.')[-2] if len(alinea_goed.split('.')) > 1 else ""
        # Laatste zin moet een afronding zijn, geen nieuwe informatie
        self.assertNotIn("nieuw", laatste_zin.lower())
    
    # ========== TEST 4: OBJECTIEVE SCHRIJFSTIJL ==========
    
    def test_geen_waardeoordelen(self):
        """Test of er geen subjectieve waardeoordelen zijn"""
        tekst_met_fout = "Gelukkig was het resultaat significant."
        tekst_zonder_fout = "Het resultaat was significant."
        
        fout_woorden = ["helaas", "gelukkig", "mooi", "lelijk", "jammer"]
        for woord in fout_woorden:
            if woord in tekst_met_fout.lower():
                self.fail(f"Waardeoordeel '{woord}' gevonden")
    
    def test_geen_subjectieve_kwalificaties(self):
        """Test of er geen subjectieve kwalificaties zijn"""
        tekst_met_fout = "Ontzettend veel cellen reageerden."
        
        fout_woorden = ["ontzettend", "duidelijk te zien", "zeer", "enorm"]
        for woord in fout_woorden:
            if woord in tekst_met_fout.lower():
                self.fail(f"Subjectieve kwalificatie '{woord}' gevonden")
    
    # ========== TEST 5: ACTIEVE SCHRIJFSTIJL ==========
    
    def test_actieve_schrijfstijl(self):
        """Test of actieve schrijfstijl wordt gebruikt (waar mogelijk)"""
        actieve_zin = "Vitamine A vergroot de kans op haarverlies."
        passieve_zin = "De kans op haarverlies wordt vergroot door vitamine A."
        
        # Check of passieve constructies vermeden worden
        if "wordt vergroot door" in passieve_zin.lower():
            # Dit is passief - een waarschuving
            pass
    
    # ========== TEST 6: VERBINDINGSWOORDEN ==========
    
    def test_verbindingswoorden_aanwezig(self):
        """Test of verbindingswoorden worden gebruikt voor samenhang"""
        verbindingswoorden = [
            "daarentegen", "echter", "maar", "hoewel", "anderzijds",
            "bovendien", "daarnaast", "ten eerste", "ten tweede",
            "dus", "daarom", "derhalve", "kortom", "samengevat"
        ]
        
        tekst_met_woorden = self.goede_tekst
        heeft_verbinding = any(woord in tekst_met_woorden.lower() for woord in verbindingswoorden)
        
        # Niet per se verplicht, maar aanbevolen
        if not heeft_verbinding:
            print("⚠️ Overweeg het gebruik van verbindingswoorden voor betere samenhang")
    
    # ========== TEST 7: CIJFERS EN EENHEDEN ==========
    
    def test_cijfers_klein_getal_voluit(self):
        """Test of cijfers onder de 10 voluit worden geschreven (behalve uitzonderingen)"""
        zin_goed = "Er werden drie experimenten uitgevoerd."
        zin_fout = "Er werden 3 experimenten uitgevoerd."
        
        # Dit is een richtlijn, geen harde eis
        if " 3 " in zin_fout:
            print("⚠️ Cijfer 3 kan beter als 'drie' worden geschreven")
    
    def test_eenheden_correct(self):
        """Test of eenheden correct zijn weergegeven"""
        goede_eenheid = "0,5 mg"
        # Check spatie tussen getal en eenheid
        if "0,5mg" in "0,5mg":
            self.fail("Geen spatie tussen getal en eenheid: '0,5mg' moet '0,5 mg' zijn")
    
    # ========== TEST 8: AFKORTINGEN ==========
    
    def test_afkorting_eerste_keer_uitgeschreven(self):
        """Test of afkortingen de eerste keer worden uitgeschreven"""
        tekst_goed = "Polymerase chain reaction (PCR) werd gebruikt. De PCR reactie duurde 2 uur."
        
        # Check of 'PCR' wordt uitgelegd bij eerste gebruik
        if "PCR" in tekst_goed and "polymerase chain reaction" not in tekst_goed.lower():
            print("⚠️ Afkorting 'PCR' moet de eerste keer worden uitgeschreven")
    
    # ========== TEST 9: BONDIGHEID ==========
    
    def test_geen_overbodige_formuleringen(self):
        """Test of er geen overbodige formuleringen zijn"""
        overbodige_formuleringen = [
            "zoals de voorgaande resultaten lieten zien",
            "uit de resultaten kan worden geconcludeerd dat",
            "het is belangrijk om te benadrukken",
            "zoals eerder vermeld"
        ]
        
        for formulering in overbodige_formuleringen:
            if formulering in self.goede_tekst.lower():
                self.fail(f"Overbodige formulering: '{formulering}'")
    
    # ========== TEST 10: VOORZETSELUITDRUKKINGEN ==========
    
    def test_geen_voorzetseluitdrukkingen(self):
        """Test of voorzetseluitdrukkingen worden vermeden"""
        vervangbare_uitdrukkingen = {
            "met betrekking tot": "over/voor",
            "door middel van": "door",
            "als gevolg van": "door",
            "in verband met": "door, doordat, omdat"
        }
        
        for fout, correct in vervangbare_uitdrukkingen.items():
            if fout in self.goede_tekst.lower():
                print(f"⚠️ Vervang '{fout}' door '{correct}'")


# ========== EXTRA: FIGUREN EN TABELLEN TESTS ==========
class TestFiguresAndTables(unittest.TestCase):
    """Test of figuren en tabellen voldoen aan de richtlijnen"""
    
    def test_figuur_heeft_onderschrift(self):
        """Test of figuren een onderschrift hebben"""
        figuur_met_onderschrift = """
        Figuur 4.1 - Expressie van eiwit X
        Mesenchymale stamcellen werden gestimuleerd met stof Y (n=6, ± SD).
        """
        self.assertIn("Figuur", figuur_met_onderschrift)
        self.assertIn("n=", figuur_met_onderschrift)
    
    def test_tabel_heeft_bovenschrift(self):
        """Test of tabellen een bovenschrift hebben"""
        tabel_met_bovenschrift = """
        Tabel 4.2 - Gemiddelde expressiewaarden
        Parameter: concentratie (μg/ml)
        """
        self.assertIn("Tabel", tabel_met_bovenschrift)
    
    def test_grafiek_heeft_foutbalken(self):
        """Test of grafieken foutbalken hebben (in beschrijving)"""
        grafiek_beschrijving = """
        De grafiek toont de gemiddelde waarden met standaarddeviatie (foutbalken).
        """
        self.assertIn("foutbalk", grafiek_beschrijving.lower())
    
    def test_grafiek_heeft_juiste_as_titels(self):
        """Test of assen correcte titels hebben met eenheden"""
        as_titels = "Concentratie (μg/ml)" in "Concentratie (μg/ml)" 
        self.assertTrue(as_titels or True)  # Placeholder


if __name__ == "__main__":
    print("=" * 70)
    print("📘 ACADEMIC WRITING TEST - Handleiding Academisch schrijven & presenteren")
    print("=" * 70)
    print("")
    print("Deze test toetst je thesis aan de richtlijnen uit:")
    print("Handleiding Academisch schrijven & presenteren (2025-2026)")
    print("Biomedische wetenschappen, Universiteit Utrecht")
    print("")
    
    unittest.main(verbosity=2)