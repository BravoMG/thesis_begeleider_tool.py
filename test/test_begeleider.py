"""
test_begeleider.py
Unittest voor ThesisBegeleider - Erasmus Universiteit

Draai deze test met:
    python -m unittest tests/test_begeleider.py
Of:
    python tests/test_begeleider.py
"""

import unittest
import sys
import os
import re

# Voeg de hoofdmap toe aan het pad zodat we de tool kunnen importeren
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thesis_begeleider_tool import ThesisBegeleider


class TestThesisBegeleider(unittest.TestCase):
    """Testklasse voor alle functionaliteiten van de thesisbegeleider"""

    def setUp(self):
        """Wordt voor elke test uitgevoerd - maak een verse begeleider aan"""
        self.begeleider = ThesisBegeleider(
            student_name="Test Student",
            thesis_title="Test Thesis Titel"
        )
        
        # Voorbeeld van een GOED titelblad
        self.goed_titelblad = """
        Titel: De invloed van AI op studiemotivatie
        Naam: Jan Jansen
        Studentnummer: 12345678
        Opleiding: Master Data Science
        Datum: 15-04-2026
        Begeleider: Dr. E. Erasmus
        """
        
        # Voorbeeld van een GOEDE methodologie
        self.goede_methodologie = """
        Dit onderzoek gebruikt een cross-sectioneel design. 
        De steekproef bestaat uit 200 studenten van de Erasmus Universiteit.
        Het meetinstrument is een gevalideerde vragenlijst met 20 items.
        Dataverzameling vond plaats in april 2026 via Qualtrics.
        De analyse bestaat uit een multipele regressieanalyse met SPSS.
        """
        
        # Voorbeeld van GOEDE referenties (APA 7e editie)
        self.goede_referenties = """
        Gooty, J., Connelly, S., Griffith, J., & Gupta, A. (2010). Leadership, affect and emotions: A state of the science review. The Leadership Quarterly, 21(6), 979-1004. https://doi.org/10.1016/j.leaqua.2010.10.005
        Poelmans, P., & Severijnen, O. (2022). De APA-richtlijnen: Over literatuurverwijzing en onderzoeksrapportage (2e, herziene druk). Coutinho.
        """

    # ========== TEST 1: TITELBLAD ==========
    
    def test_titelblad_goed(self):
        """Test of een correct titelblad wordt goedgekeurd"""
        feedback = self.begeleider.beoordeel_titelblad(self.goed_titelblad)
        # Minstens één feedbackitem moet een vinkje ✅ bevatten
        self.assertTrue(any("✅" in f for f in feedback))
        
    def test_titelblad_mist_naam(self):
        """Test of ontbrekende naam wordt gedetecteerd"""
        titelblad_zonder_naam = """
        Titel: Mijn thesis
        Studentnummer: 12345678
        Opleiding: Master
        Datum: 15-04-2026
        """
        feedback = self.begeleider.beoordeel_titelblad(titelblad_zonder_naam)
        self.assertTrue(any("mist" in f and "naam" in f.lower() for f in feedback))
        
    def test_titelblad_mist_studentnummer(self):
        """Test of ontbrekend studentnummer wordt gedetecteerd"""
        titelblad_zonder_nummer = """
        Titel: Mijn thesis
        Naam: Jan Jansen
        Opleiding: Master
        Datum: 15-04-2026
        Begeleider: Dr. Y
        """
        feedback = self.begeleider.beoordeel_titelblad(titelblad_zonder_nummer)
        self.assertTrue(any("studentnummer" in f.lower() for f in feedback))
        
    def test_titelblad_mist_datum(self):
        """Test of ontbrekende datum wordt gedetecteerd"""
        titelblad_zonder_datum = """
        Titel: Mijn thesis
        Naam: Jan Jansen
        Studentnummer: 12345678
        Opleiding: Master
        Begeleider: Dr. Y
        """
        feedback = self.begeleider.beoordeel_titelblad(titelblad_zonder_datum)
        self.assertTrue(any("datum" in f.lower() for f in feedback))
    
    def test_titelblad_mist_begeleider(self):
        """Test of ontbrekende begeleider wordt gedetecteerd"""
        titelblad_zonder_begeleider = """
        Titel: Mijn thesis
        Naam: Jan Jansen
        Studentnummer: 12345678
        Opleiding: Master
        Datum: 15-04-2026
        """
        feedback = self.begeleider.beoordeel_titelblad(titelblad_zonder_begeleider)
        self.assertTrue(any("begeleider" in f.lower() for f in feedback))

    # ========== TEST 2: METHODOLOGIE ==========
    
    def test_methodologie_compleet(self):
        """Test of complete methodologie wordt goedgekeurd"""
        feedback = self.begeleider.beoordeel_methodologie(self.goede_methodologie)
        self.assertTrue(any("✅" in f for f in feedback))
        
    def test_methodologie_mist_design(self):
        """Test of ontbrekend design wordt gedetecteerd"""
        methode_zonder_design = """
        De steekproef bestaat uit 200 studenten.
        De vragenlijst is afgenomen in april.
        Data is geanalyseerd met regressie.
        """
        feedback = self.begeleider.beoordeel_methodologie(methode_zonder_design)
        self.assertTrue(any("design" in f.lower() for f in feedback))
        
    def test_methodologie_mist_steekproef(self):
        """Test of ontbrekende steekproef wordt gedetecteerd"""
        methode_zonder_steekproef = """
        Design is cross-sectioneel.
        Vragenlijst is gebruikt voor meting.
        Regressieanalyse is toegepast.
        """
        feedback = self.begeleider.beoordeel_methodologie(methode_zonder_steekproef)
        self.assertTrue(any("steekproef" in f.lower() or "sample" in f.lower() for f in feedback))
        
    def test_methodologie_mist_meetinstrument(self):
        """Test of ontbrekend meetinstrument wordt gedetecteerd"""
        methode_zonder_instrument = """
        Design is experimenteel.
        Steekproef: 100 proefpersonen.
        Data geanalyseerd met t-toets.
        """
        feedback = self.begeleider.beoordeel_methodologie(methode_zonder_instrument)
        self.assertTrue(any("meetinstrument" in f.lower() for f in feedback))
    
    def test_methodologie_mist_procedure(self):
        """Test of ontbrekende procedure wordt gedetecteerd"""
        methode_zonder_procedure = """
        Design is cross-sectioneel.
        Steekproef: 200 studenten.
        Meetinstrument: vragenlijst.
        Analyse: regressie.
        """
        feedback = self.begeleider.beoordeel_methodologie(methode_zonder_procedure)
        self.assertTrue(any("procedure" in f.lower() for f in feedback))
    
    def test_methodologie_mist_analyse(self):
        """Test of ontbrekende analysemethode wordt gedetecteerd"""
        methode_zonder_analyse = """
        Design is cross-sectioneel.
        Steekproef: 200 studenten.
        Meetinstrument: vragenlijst.
        Procedure: afname in april.
        """
        feedback = self.begeleider.beoordeel_methodologie(methode_zonder_analyse)
        self.assertTrue(any("analyse" in f.lower() for f in feedback))

    # ========== TEST 3: BRONVERMELDING (APA 7e editie) ==========
    
    def test_bronvermelding_goed(self):
        """Test of correcte APA-bronnen worden goedgekeurd"""
        feedback = self.begeleider.check_bronvermelding(self.goede_referenties)
        self.assertTrue(any("✅" in f for f in feedback))
        
    def test_bronvermelding_leeg(self):
        """Test of lege referentielijst wordt gedetecteerd"""
        feedback = self.begeleider.check_bronvermelding("")
        self.assertTrue(any("Geen referentielijst" in f or "Geen bronnen" in f for f in feedback))
        
    def test_bronvermelding_zonder_ampersand(self):
        """Test of 'en' in plaats van '&' wordt gedetecteerd (APA p.40)"""
        referenties_zonder_ampersand = """
        Poelmans, P. en Severijnen, O. (2022). De APA-richtlijnen. Coutinho.
        """
        feedback = self.begeleider.check_bronvermelding(referenties_zonder_ampersand)
        # Moet een waarschuwing geven over 'en' vs '&'
        self.assertTrue(any("&" in f or "en" in f for f in feedback))
        
    def test_bronvermelding_zonder_jaartal(self):
        """Test of ontbrekend jaartal wordt gedetecteerd (APA p.96)"""
        referenties_zonder_jaartal = """
        Jansen, P. Titel van het boek. Uitgever.
        """
        feedback = self.begeleider.check_bronvermelding(referenties_zonder_jaartal)
        self.assertTrue(any("jaartal" in f.lower() for f in feedback))
    
    def test_bronvermelding_alfabetisch(self):
        """Test of niet-alfabetische volgorde wordt gedetecteerd (APA p.91)"""
        referenties_niet_alfabetisch = """
        Zwaan, A. (2020). Titel Z. Uitgever.
        Aalbers, B. (2019). Titel A. Uitgever.
        Jansen, C. (2021). Titel J. Uitgever.
        """
        feedback = self.begeleider.check_bronvermelding(referenties_niet_alfabetisch)
        # Moet een waarschuwing geven over alfabetische volgorde
        self.assertTrue(any("alfabetisch" in f.lower() for f in feedback))

    # ========== TEST 4: APA 7e EDITIE SPECIFIEKE CHECKS ==========
    
    def test_apa_boek_correct(self):
        """Test of een correct APA-boek wordt herkend"""
        referentie = "Poelmans, P., & Severijnen, O. (2022). De APA-richtlijnen (2e druk). Coutinho."
        # Dit is een correcte APA-referentie, zou geen fouten moeten geven
        feedback = self.begeleider.check_apa_conformiteit(referentie)
        # Alleen als er geen fouten zijn, is er een ✅
        self.assertTrue(any("✅" in f for f in feedback) or len(feedback) == 1)
    
    def test_apa_tijdschrift_met_doi(self):
        """Test of een tijdschriftartikel met DOI correct is (APA p.99-100)"""
        referentie = "Gooty, J., Connelly, S., Griffith, J., & Gupta, A. (2010). Leadership. The Leadership Quarterly, 21(6), 979-1004. https://doi.org/10.1016/j.leaqua.2010.10.005"
        feedback = self.begeleider.check_apa_conformiteit(referentie)
        self.assertTrue(any("✅" in f for f in feedback) or len(feedback) == 1)
    
    def test_apa_tijdschrift_zonder_doi(self):
        """Test of een tijdschriftartikel zonder DOI wordt gedetecteerd (APA p.100)"""
        referentie = "Jansen, P. (2023). Titel artikel. Tijdschrift, 12(3), 45-67."
        feedback = self.begeleider.check_apa_conformiteit(referentie)
        self.assertTrue(any("DOI" in f for f in feedback))

    # ========== TEST 5: CITAAT CHECKS ==========
    
    def test_citaat_met_paginanummer(self):
        """Test of een citaat met paginanummer correct is (APA p.34)"""
        tekst = 'Volgens Goleman (1995) is "emotionele intelligentie cruciaal" (p. 45).'
        feedback = self.begeleider.check_citaten(tekst)
        # Geen fouten verwacht
        self.assertTrue(any("✅" in f for f in feedback))
    
    def test_citaat_zonder_paginanummer(self):
        """Test of een kort citaat zonder paginanummer wordt gedetecteerd (APA p.34)"""
        tekst = 'Volgens Goleman (1995) is "emotionele intelligentie cruciaal voor leiderschap".'
        feedback = self.begeleider.check_citaten(tekst)
        self.assertTrue(any("paginanummer" in f.lower() for f in feedback))

    # ========== TEST 6: AI-DETECTIE ==========
    
    def test_ai_detectie_geen_indicatoren(self):
        """Test of normale tekst geen AI-waarschuwing geeft"""
        normale_tekst = """
        Ik heb zelf dit onderzoek uitgevoerd. Mijn conclusie is dat 
        de resultaten laten zien dat er een verband is.
        """
        feedback, score = self.begeleider.ai_detectie(normale_tekst)
        self.assertTrue(any("✅" in f for f in feedback))
        self.assertLess(score, 0.2)
        
    def test_ai_detectie_met_indicatoren(self):
        """Test of AI-markers worden gedetecteerd"""
        ai_tekst = """
        Het is belangrijk om te benadrukken dat de resultaten significant zijn.
        Daarnaast zien we een sterk effect. Bovendien is de correlatie hoog.
        Samenvattend kan worden gesteld dat de hypothese wordt bevestigd.
        """
        feedback, score = self.begeleider.ai_detectie(ai_tekst)
        self.assertTrue(any("AI-signaal" in f for f in feedback))
        self.assertGreater(score, 0.15)

    # ========== TEST 7: STAPPENPLAN ==========
    
    def test_stappenplan_genereert_bij_fouten(self):
        """Test of stappenplan wordt gegenereerd bij fouten"""
        feedback_met_fouten = [
            "❌ Titelblad mist: naam",
            "⚠️ Methodologie mist: steekproef",
            "⚠️ Gebruik '&' in plaats van 'en'"
        ]
        stappen = self.begeleider.genereer_stappenplan(feedback_met_fouten)
        # Er moeten stappen zijn (niet leeg)
        self.assertTrue(len(stappen) > 0)
        # Geen ✅ mag erin staan (want er zijn fouten)
        self.assertFalse(any("✅" in stap for stap in stappen))
        
    def test_stappenplan_geen_fouten(self):
        """Test of stappenplan aangeeft dat alles goed is"""
        feedback_zonder_fouten = [
            "✅ Titelblad volledig",
            "✅ Methodologie compleet",
            "✅ Bronvermelding correct"
        ]
        stappen = self.begeleider.genereer_stappenplan(feedback_zonder_fouten)
        self.assertTrue(any("✅" in stap for stap in stappen))
        self.assertTrue(any("Geen correcties" in stap or "slagen" in stap for stap in stappen))

    # ========== TEST 8: VOLLEDIGE BEOORDELING ==========
    
    def test_volledige_beoordeling_retourneert_dict(self):
        """Test of volledige_beoordeling een dictionary retourneert"""
        resultaat = self.begeleider.volledige_beoordeling(
            titelblad=self.goed_titelblad,
            methodologie=self.goede_methodologie,
            referenties=self.goede_referenties,
            volledige_tekst=self.goede_methodologie
        )
        self.assertIsInstance(resultaat, dict)
        self.assertIn("feedback", resultaat)
        self.assertIn("stappenplan", resultaat)
        self.assertIn("ai_score", resultaat)
        self.assertIn("log", resultaat)
        self.assertIn("hoofdstuk_4_rapport", resultaat)
        
    def test_volledige_beoordeling_logt_feedback(self):
        """Test of feedback wordt gelogd in de begeleider"""
        start_log_count = len(self.begeleider.feedback_log)
        self.begeleider.volledige_beoordeling(
            titelblad=self.goed_titelblad,
            methodologie=self.goede_methodologie,
            referenties=self.goede_referenties
        )
        einde_log_count = len(self.begeleider.feedback_log)
        self.assertEqual(einde_log_count, start_log_count + 1)
        
    def test_volledige_beoordeling_met_slechte_input(self):
        """Test of volledige beoordeling werkt met slechte/lege input"""
        resultaat = self.begeleider.volledige_beoordeling(
            titelblad="",
            methodologie="",
            referenties=""
        )
        # Moet feedback geven (geen crash)
        self.assertIsNotNone(resultaat["feedback"])
        self.assertTrue(len(resultaat["feedback"]) > 0)

    # ========== TEST 9: TABELLEN GENERATOR ==========
    
    def test_tabel_4_1_wordt_genereerd(self):
        """Test of Tabel 4.1 wordt gegenereerd"""
        tabel = self.begeleider.genereer_tabel_4_1()
        self.assertIsInstance(tabel, str)
        self.assertIn("Tabel 4.1", tabel)
        self.assertIn("Rutte", tabel)
        self.assertIn("De Jonge", tabel)
        self.assertIn("Totaal", tabel)
    
    def test_tabel_4_2_wordt_genereerd(self):
        """Test of Tabel 4.2 wordt gegenereerd"""
        tabel = self.begeleider.genereer_tabel_4_2()
        self.assertIsInstance(tabel, str)
        self.assertIn("Tabel 4.2", tabel)
        self.assertIn("Competentie", tabel)
        self.assertIn("Zelfregulatie", tabel)
    
    def test_tabel_4_3_wordt_genereerd(self):
        """Test of Tabel 4.3 wordt gegenereerd"""
        tabel = self.begeleider.genereer_tabel_4_3()
        self.assertIsInstance(tabel, str)
        self.assertIn("Tabel 4.3", tabel)
        self.assertIn("Zelfbewustzijn", tabel)
        self.assertIn("Empathie", tabel)
    
    def test_hoofdstuk_4_rapport_wordt_genereerd(self):
        """Test of volledig Hoofdstuk 4 rapport wordt gegenereerd"""
        rapport = self.begeleider.genereer_rapport_hoofdstuk_4()
        self.assertIsInstance(rapport, str)
        self.assertIn("HOOFDSTUK 4", rapport.upper())
        self.assertIn("Tabel 4.1", rapport)
        self.assertIn("Tabel 4.2", rapport)
        self.assertIn("Tabel 4.3", rapport)

    # ========== TEST 10: RANDGEWALLEN ==========
    
    def test_empty_begeleider_initialisatie(self):
        """Test of begeleider zonder parameters werkt"""
        lege_begeleider = ThesisBegeleider()
        self.assertIsNotNone(lege_begeleider)
        self.assertEqual(lege_begeleider.student_name, "")
        
    def test_unicode_en_speciale_tekens(self):
        """Test of Unicode en speciale tekens goed worden verwerkt"""
        titelblad_unicode = """
        Titel: Onderzoek naar ééntonige klanken
        Naam: Jéronimo van der Müller
        Studentnummer: 12345678
        Opleiding: Master Taalwetenschap
        Datum: 15-04-2026
        Begeleider: Dr. E. van den Berg
        """
        try:
            feedback = self.begeleider.beoordeel_titelblad(titelblad_unicode)
            self.assertIsInstance(feedback, list)
        except Exception as e:
            self.fail(f"Unicode veroorzaakt fout: {e}")
            
    def test_lange_teksten(self):
        """Test of lange teksten (1000+ karakters) goed worden verwerkt"""
        lange_methodologie = "Design: experimenteel. " * 500  # Herhaald voor lange tekst
        try:
            feedback = self.begeleider.beoordeel_methodologie(lange_methodologie)
            self.assertIsInstance(feedback, list)
        except Exception as e:
            self.fail(f"Lange tekst veroorzaakt fout: {e}")


# ========== EXTRA: PERFORMANCE TEST (optioneel) ==========
class PerformanceTestThesisBegeleider(unittest.TestCase):
    """Test de snelheid van de begeleider bij grote hoeveelheden data"""
    
    def setUp(self):
        self.begeleider = ThesisBegeleider()
        
    def test_snelle_verwerking(self):
        """Test of de begeleider snel reageert (minder dan 0.5 seconden)"""
        import time
        lange_tekst = "Dit is een test. " * 10000
        
        start = time.time()
        self.begeleider.ai_detectie(lange_tekst)
        eind = time.time()
        
        self.assertLess(eind - start, 0.5, "AI-detectie is te traag (>0.5s)")


# ========== HOOFDPROGRAMMA ==========
if __name__ == "__main__":
    # Zet verbositeit aan voor gedetailleerde output
    unittest.main(verbosity=2)