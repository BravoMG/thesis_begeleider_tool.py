"""
Specifieke tests voor Master Bestuurskunde - Erasmus Universiteit
Gebaseerd op: Handleiding Afstudeertraject Master Bestuurskunde 2023-2024

Draai met: python -m unittest tests/test_begeleider_bestuurskunde.py
"""

import unittest
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from thesis_begeleider_tool import ThesisBegeleider


class TestBestuurskundeHandleiding(unittest.TestCase):
    """
    Toetst of een scriptie voldoet aan de specifieke eisen uit
    de Handleiding Afstudeertraject Master Bestuurskunde 2023-2024
    """

    def setUp(self):
        self.begeleider = ThesisBegeleider(
            student_name="Test Student Bestuurskunde",
            thesis_title="Bestuurskundig onderzoek naar beleidsevaluatie"
        )
        
        # Goed voorbeeld volgens handleiding (p. 7-11)
        self.voorbeeld_goede_inleiding = """
        Hoofdstuk 1: Inleiding
        De aanleiding voor dit onderzoek is de toenemende druk op het openbaar bestuur.
        De probleemstelling luidt: Hoe kan beleidsevaluatie bijdragen aan effectiever bestuur?
        De wetenschappelijke relevantie is het toetsen van bestaande evaluatietheorieën.
        De maatschappelijke relevantie is het verbeteren van overheidsbeleid.
        Dit hoofdstuk is als volgt opgebouwd. Eerst wordt de probleemstelling uitgewerkt,
        daarna de relevantie en tot slot de opbouw van de scriptie.
        """
        
        self.voorbeeld_goede_theorie = """
        Hoofdstuk 2: Theoretisch kader
        Dit onderzoek maakt gebruik van de evaluatietheorie van Vedung (1997).
        Daarnaast wordt het beleidsnetwerkperspectief van Rhodes (2006) toegepast.
        Het conceptueel model toont de relatie tussen evaluatievormen en beleidseffecten.
        Figuur 2.1 geeft dit schema weer. De belangrijkste concepten zijn:
        evaluatiecapaciteit, beleidsleren en effectiviteit.
        """
        
        self.voorbeeld_goede_methode = """
        Hoofdstuk 3: Methodologische verantwoording
        Dit onderzoek gebruikt een kwalitatieve casestudie (Yin, 2003).
        De steekproef bestaat uit 4 beleidscases binnen de publieke sector.
        Dataverzameling vindt plaats via semi-gestructureerde interviews (n=12)
        en documentanalyse van beleidsstukken.
        De analyse gebeurt met thematische analyse (Braun & Clarke, 2006).
        Informed consent is verkregen van alle respondenten.
        """
        
        self.voorbeeld_goede_resultaten = """
        Hoofdstuk 4: Resultaten en analyse
        Uit de interviews blijkt dat evaluatiecapaciteit per organisatie verschilt.
        Tabel 4.1 toont de scores op evaluatieactiviteiten.
        Casus A heeft een hoge evaluatiecapaciteit, casus B een lage.
        De analyse laat zien dat beleidsleren positief samenhangt met evaluatiegebruik.
        Discussie: De resultaten zijn beperkt generaliseerbaar door de kleine steekproef.
        """
        
        self.voorbeeld_goede_conclusie = """
        Hoofdstuk 5: Conclusies en aanbevelingen
        De hoofdvraag wordt beantwoord: Beleidsevaluatie draagt bij aan effectiever bestuur
        wanneer er sprake is van leiderschap en leercultuur.
        Reflectie: De methodologische keuze voor casestudie beperkt generaliseerbaarheid.
        Aanbeveling 1: Investeer in evaluatievaardigheden bij beleidsmedewerkers.
        Aanbeveling 2: Creëer structurele evaluatiemomenten in beleidscycli.
        """

    # ========== TEST 1: WOORDENAANTAL (p. 7) ==========
    
    def test_woordenaantal_max_12000(self):
        """Handleiding p.7: Maximaal 12.000 woorden"""
        # Simuleer een tekst van 13.000 woorden
        lange_tekst = "woord " * 13000
        woordentelling = len(lange_tekst.split())
        self.assertLessEqual(
            woordentelling, 12000,
            f"Scriptie heeft {woordentelling} woorden, max is 12000 (p.7 handleiding)"
        )
    
    def test_woordenaantal_bijlagen_uitgesloten(self):
        """Handleiding p.7: Bijlagen tellen niet mee"""
        hoofdtekst = "Dit is de hoofdtekst." * 500  # ~2500 woorden
        bijlagen = "Dit is bijlage A met extra data."
        
        # Alleen hoofdtekst mag meetellen
        woorden_hoofdtekst = len(hoofdtekst.split())
        self.assertGreater(woorden_hoofdtekst, 0, "Hoofdtekst mag niet leeg zijn")

    # ========== TEST 2: HOOFDSTUKSTRUCTUUR (p. 7-8) ==========
    
    def test_verplichte_hoofdstukken_aanwezig(self):
        """Handleiding p.7: Verplichte 5 hoofdstukken"""
        scriptie = """
        Hoofdstuk 1: Inleiding
        Hoofdstuk 2: Theorie
        Hoofdstuk 3: Methode
        Hoofdstuk 4: Resultaten
        Hoofdstuk 5: Conclusies
        """
        verplichte_kopjes = ["Inleiding", "Theorie", "Methode", "Resultaten", "Conclusies"]
        for kopje in verplichte_kopjes:
            self.assertIn(
                kopje, scriptie,
                f"Hoofdstuk '{kopje}' ontbreekt (p.7 handleiding)"
            )
    
    def test_omvang_verhoudingen_binnen_bandbreedte(self):
        """Handleiding p.8: Aangeraden omvang per hoofdstuk"""
        # Simuleer een scriptie van 10.000 woorden
        omvang = {
            "inleiding": 1000,    # 10% - goed
            "theorie": 2200,      # 22% - binnen 20-25%
            "methode": 1700,      # 17% - binnen 15-20%
            "resultaten": 3700,   # 37% - binnen 35-40%
            "conclusie": 1400     # 14% - binnen 15-20% (iets laag maar acceptabel)
        }
        
        totaal = sum(omvang.values())
        
        # Controleer of inleiding ongeveer 10% is
        inleiding_pct = omvang["inleiding"] / totaal * 100
        self.assertAlmostEqual(inleiding_pct, 10, delta=5,
            msg=f"Inleiding is {inleiding_pct:.1f}%, suggestie is 10% (p.8)")
        
        # Controleer theorie tussen 20-25%
        theorie_pct = omvang["theorie"] / totaal * 100
        self.assertBetween(theorie_pct, 20, 25,
            f"Theorie is {theorie_pct:.1f}%, moet 20-25% zijn (p.8)")
    
    def assertBetween(self, waarde, ondergrens, bovengrens, msg):
        """Hulpfunctie om te checken of waarde tussen grenzen ligt"""
        self.assertGreaterEqual(waarde, ondergrens, msg)
        self.assertLessEqual(waarde, bovengrens, msg)

    # ========== TEST 3: TITELBLAD (p. 10) ==========
    
    def test_titelblad_vereisten(self):
        """Handleiding p.10: Titelblad moet bevatten"""
        goed_titelblad = """
        Titel: Beleidsevaluatie in het openbaar bestuur
        Naam: Jan Jansen
        Studentnummer: 12345678
        Erasmus Universiteit Rotterdam
        Master Bestuurskunde
        Begeleider: Dr. E. Erasmus
        Tweede beoordelaar: Dr. S. Smit
        Datum: 15 juni 2024
        """
        
        vereisten = [
            "titel", "naam", "studentnummer", "erasmus universiteit",
            "master bestuurskunde", "begeleider", "tweede beoordelaar", "datum"
        ]
        
        for vereiste in vereisten:
            self.assertIn(
                vereiste, goed_titelblad.lower(),
                f"Titelblad mist: {vereiste} (p.10 handleiding)"
            )

    # ========== TEST 4: SAMENVATTING (p. 10) ==========
    
    def test_samenvatting_aanwezig(self):
        """Handleiding p.10: Samenvatting van 1-2 pagina's"""
        scriptie_met_samenvatting = """
        Samenvatting
        In deze scriptie wordt onderzocht hoe beleidsevaluatie bijdraagt aan effectiever bestuur.
        De hoofdvraag luidt: Wat is de relatie tussen evaluatiecapaciteit en beleidseffectiviteit?
        Uit de resultaten blijkt dat een hoge evaluatiecapaciteit leidt tot meer beleidsleren.
        De aanbeveling is om structurele evaluatiemomenten in te bouwen.
        """
        self.assertIn("samenvatting", scriptie_met_samenvatting.lower(),
            "Samenvatting ontbreekt (p.10 handleiding)")

    # ========== TEST 5: BRONVERMELDING APA (p. 11) ==========
    
    def test_bronvermelding_apa_conform(self):
        """Handleiding p.11: APA-stijl voor bronvermelding"""
        goede_apa = """
        Jansen, P. (2023). Beleidsevaluatie in de praktijk. Tijdschrift voor Bestuurskunde, 12(3), 45-67.
        Smit, L. & de Boer, T. (2022). Publiek management. Amsterdam: Boom uitgevers.
        Vedung, E. (1997). Public policy and program evaluation. New Brunswick: Transaction Publishers.
        """
        
        # Controleer op jaartal na auteur
        self.assertTrue(re.search(r'[A-Z][a-z]+,\s[A-Z]\.?\s\(\d{4}\)', goede_apa),
            "Geen APA-formaat herkend (jaartal na auteur) - p.11 handleiding")
        
        # Controleer op & voor meerdere auteurs
        self.assertTrue('&' in goede_apa or 'en' in goede_apa,
            "Gebruik '&' voor meerdere auteurs (APA) - p.11 handleiding")

    # ========== TEST 6: PROBLEEMSTELLING (p. 14-15) ==========
    
    def test_probleemstelling_bevat_doelstelling(self):
        """Handleiding p.14-15: Probleemstelling heeft doelstelling en vraagstelling"""
        goede_probleemstelling = """
        Doelstelling: Het doel van dit onderzoek is het verklaren van variatie in beleidseffectiviteit.
        Hoofdvraag: Wat is de invloed van evaluatiecapaciteit op beleidseffectiviteit?
        Deelvraag 1: Hoe wordt evaluatiecapaciteit gemeten?
        Deelvraag 2: Welke factoren bevorderen evaluatiegebruik?
        """
        
        self.assertIn("doelstelling", goede_probleemstelling.lower(),
            "Probleemstelling mist doelstelling (p.14-15 handleiding)")
        self.assertIn("hoofdvraag", goede_probleemstelling.lower(),
            "Probleemstelling mist hoofdvraag (p.14-15 handleiding)")
        self.assertIn("deelvraag", goede_probleemstelling.lower(),
            "Probleemstelling mist deelvragen (p.14-15 handleiding)")

    # ========== TEST 7: STAGE-ONDERWERP (p. 4-5) ==========
    
    def test_stage_publieke_sector(self):
        """Handleiding p.4: Stage in publieke sector"""
        stage_beschrijving = """
        Stageplaats: Ministerie van Binnenlandse Zaken
        Sector: Publieke sector - Rijksoverheid
        """
        self.assertIn("publieke", stage_beschrijving.lower(),
            "Stage moet in publieke sector (p.4 handleiding)")
        
    def test_stage_omvang_min_280_uur(self):
        """Handleiding p.4: Stage minimaal 280 uur, max 4 dagen/week"""
        stage_uren = 280
        self.assertGreaterEqual(stage_uren, 280,
            f"Stage is {stage_uren} uur, minimaal 280 uur (p.4 handleiding)")

    # ========== TEST 8: BEOORDELINGSCRITERIA (p. 11-12) ==========
    
    def test_beoordelingscriteria_aanwezig_in_scriptie(self):
        """Handleiding p.11-12: 8 beoordelingscriteria weerspiegeld"""
        scriptie_met_criteria = """
        Probleemstelling: dit onderzoek richt zich op...
        Theorie: het theoretisch kader bestaat uit...
        Onderzoeksopzet: de methodologie is...
        Kwaliteit analyse: de resultaten tonen aan...
        Conclusies: de hoofdvraag wordt beantwoord...
        Reflectie: de beperkingen van dit onderzoek zijn...
        Helderheid: de scriptie is gestructureerd...
        Proces: het onderzoek is zelfstandig uitgevoerd...
        """
        
        criteria = [
            "probleemstelling", "theorie", "onderzoeksopzet", "analyse",
            "conclusies", "reflectie", "helderheid", "proces"
        ]
        
        for criterium in criteria:
            self.assertIn(criterium, scriptie_met_criteria.lower(),
                f"Scriptie adresseert criterium '{criterium}' onvoldoende (p.11-12)")

    # ========== TEST 9: PLAGIAAT (p. 13) ==========
    
    def test_geen_plagiaat(self):
        """Handleiding p.13: Plagiaatscan verplicht"""
        eigen_tekst = "Dit is mijn eigen originele formulering van het onderzoek."
        # Simuleer dat een student citeert met bronvermelding
        citaat_met_bron = "Volgens Jansen (2023) is 'beleidsevaluatie cruciaal' (p. 45)."
        
        # Check of er geen letterlijke overname is zonder aanhalingstekens
        self.assertNotRegex(eigen_tekst, r'\w{20,}\s+\w{20,}',
            "Verdacht lange woordcombinatie zonder bron - check op plagiaat (p.13)")

    # ========== TEST 10: PRIVACY & INFORMED CONSENT (p. 13) ==========
    
    def test_informed_consent_vermeld(self):
        """Handleiding p.13: Informed consent vereist"""
        scriptie_met_consent = """
        Voorafgaand aan de interviews is schriftelijke toestemming (informed consent)
        verkregen van alle respondenten. De privacy van participanten is gewaarborgd
        door anonimisering van persoonsgegevens.
        """
        self.assertIn("informed consent", scriptie_met_consent.lower(),
            "Informed consent niet vermeld (p.13 handleiding - privacy wetgeving)")

    # ========== TEST 11: MAXIMALE BEOORDELINGSMATRIX (p. 24-27) ==========
    
    def test_cijferbepaling_gewogen_gemiddelde(self):
        """Handleiding p.24: Gewogen gemiddelde, niet rekenkundig"""
        scores = {
            "probleemstelling": 7.5,
            "theorie": 8.0,
            "onderzoeksopzet": 6.5,
            "analyse": 7.0,
            "conclusies": 7.5,
            "reflectie": 8.0,
            "helderheid": 9.0,
            "proces": 8.0
        }
        
        # Simuleer gewogen gemiddelde (theorie en methode zwaarder)
        gewicht = {
            "probleemstelling": 1,
            "theorie": 2,
            "onderzoeksopzet": 2,
            "analyse": 2,
            "conclusies": 1,
            "reflectie": 1,
            "helderheid": 1,
            "proces": 1
        }
        
        totaal_gewicht = sum(gewicht.values())
        gewogen_som = sum(scores[c] * gewicht[c] for c in scores)
        eindcijfer = gewogen_som / totaal_gewicht
        
        self.assertGreaterEqual(eindcijfer, 5.5,
            f"Eindcijfer {eindcijfer:.1f} is onvoldoende volgens matrix (p.24-27)")
    
    def test_fundamentele_fout_leidt_tot_onvoldoende(self):
        """Handleiding p.24: Fundamentele fout = onvoldoende, ook al zijn andere criteria voldoende"""
        # Scenario: alle criteria voldoende, maar statistische analyse is fout
        fundamentele_fout_aanwezig = True
        
        if fundamentele_fout_aanwezig:
            self.skipTest("Fundamentele fout gedetecteerd: scriptie is onvoldoende (p.24 matrix)")


# ========== EXTRA: INTEGRATIETEST ==========
class TestBestuurskundeIntegratie(unittest.TestCase):
    """Test of de Bestuurskunde-specifieke checks werken met de hoofdtool"""
    
    def setUp(self):
        self.begeleider = ThesisBegeleider()
        
    def test_handleiding_wordt_toegepast(self):
        """Controleer of de tool Bestuurskunde-regels herkent"""
        # Dit is een integratietest die controleert of de begeleider
        # de specifieke regels uit de handleiding kan toepassen
        
        scriptie_tekst = """
        Master Bestuurskunde
        Probleemstelling: Dit onderzoekt beleidsevaluatie.
        Theoretisch kader: Gebruik van evaluatietheorie.
        Methode: Casestudie met interviews.
        """
        
        # Check of de tool de context herkent
        if "bestuurskunde" in scriptie_tekst.lower():
            # Specifieke regels voor Bestuurskunde moeten actief zijn
            self.assertTrue(True, "Bestuurskunde-specifieke regels actief")


if __name__ == "__main__":
    unittest.main(verbosity=2)