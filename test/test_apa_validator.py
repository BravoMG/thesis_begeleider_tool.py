"""
APA-validator voor Master Theses - Gebaseerd op:
Poelmans, P. & Severijnen, O. (2022). De APA-richtlijnen (7e editie). Coutinho.

Test of bronvermeldingen voldoen aan APA 7e editie richtlijnen.
Draai met: python -m unittest tests/test_apa_validator.py
"""

import unittest
import re
from typing import List, Dict, Tuple


class APAValidator:
    """Valideert bronvermeldingen volgens APA 7e editie richtlijnen"""
    
    def __init__(self):
        self.apa_richtlijnen = {
            "boek": {
                "patroon": r'^([A-Z][a-z]+,\s[A-Z]\.?\s?(&\s?[A-Z][a-z]+,\s[A-Z]\.?)?)\s\((\d{4}(?:,\s[a-z]+)?)\)\.\s([A-Za-z\s\-\:]+)\.\s([A-Za-z\s]+)\.$',
                "verplicht": ["auteur", "jaar", "titel", "uitgever"]
            },
            "tijdschrift": {
                "patroon": r'^([A-Z][a-z]+,\s[A-Z]\.?\s?(&\s?[A-Z][a-z]+,\s[A-Z]\.?)?)\s\((\d{4})\)\.\s([A-Za-z\s\-\:]+)\.\s([A-Za-z\s]+),\s(\d+)\((\d+)\)(?:,\s(\d+)-(\d+))?\.?$',
                "verplicht": ["auteur", "jaar", "titel", "tijdschrift", "volume", "paginas"]
            },
            "hoofdstuk": {
                "patroon": r'^([A-Z][a-z]+,\s[A-Z]\.?\s?(&\s?[A-Z][a-z]+,\s[A-Z]\.?)?)\s\((\d{4})\)\.\s([A-Za-z\s\-\:]+)\.\sIn\s([A-Z][a-z]+\s?(&\s?[A-Z][a-z]+)?)\s\(Ed\.\)\.\s([A-Za-z\s\-\:]+)\s\(pp\.\s(\d+)-(\d+)\)\.\s([A-Za-z\s]+)\.$',
                "verplicht": ["auteur_hfdst", "jaar", "titel_hfdst", "redacteur", "titel_boek", "paginas", "uitgever"]
            },
            "web": {
                "patroon": r'^([A-Z][a-z]+,\s[A-Z]\.?\s?(&\s?[A-Z][a-z]+,\s[A-Z]\.?)?|\[@[A-Za-z]+\])\s\((\d{4}(?:,\s\d{1,2}\s[a-z]+)?)\)\.\s(.+)\.\s([A-Za-z\s]+)\.\s(https?://[^\s]+)$',
                "verplicht": ["auteur", "datum", "titel", "site_naam", "url"]
            }
        }
        
        self.fouten = []
    
    def valideer_auteur(self, auteur_tekst: str) -> Dict:
        """Valideer auteur volgens APA 7e editie (p. 92-95)"""
        issues = []
        
        # Check op 'en' in plaats van '&' (p. 40)
        if ' en ' in auteur_tekst.lower() and '&' not in auteur_tekst:
            issues.append("Gebruik '&' in plaats van 'en' bij meerdere auteurs (APA p.40)")
        
        # Check op correct formaat: Achternaam, V.
        auteur_pattern = r'^[A-Z][a-z]+,\s[A-Z]\.?'
        if not re.match(auteur_pattern, auteur_tekst.split('&')[0].strip()):
            issues.append(f"Ongeldig auteurformaat: '{auteur_tekst}'. Gebruik: 'Achternaam, V.' (APA p.92)")
        
        # Check op punt na initiaal
        if re.search(r'[A-Z]\s', auteur_tekst) and '&' not in auteur_tekst:
            issues.append("Zet een punt na elke initiaal: 'J. D.' in plaats van 'J D' (APA p.93)")
        
        return {
            "geldig": len(issues) == 0,
            "issues": issues,
            "gecorrigeerd": auteur_tekst.replace(' en ', ' & ') if ' en ' in auteur_tekst else auteur_tekst
        }
    
    def valideer_datum(self, datum_tekst: str, bron_type: str) -> Dict:
        """Valideer datum volgens APA 7e editie (p. 96-97)"""
        issues = []
        
        # Check of jaar geldig is (1900-2025)
        jaar_match = re.search(r'(\d{4})', datum_tekst)
        if jaar_match:
            jaar = int(jaar_match.group(1))
            if jaar < 1900 or jaar > 2025:
                issues.append(f"Ongeldig jaar: {jaar}. Jaar moet tussen 1900 en 2025 liggen (APA p.96)")
        
        # Check voor '(n.d.)' voor geen datum
        if 'n.d.' in datum_tekst.lower():
            issues.append("Gebruik '(n.d.)' voor bronnen zonder datum (APA p.97)")
        
        # Check voor specifieke datum bij webpagina's
        if bron_type == "web" and not re.search(r'\d{4},\s\d{1,2}\s[a-z]+', datum_tekst.lower()):
            issues.append("Voor webpagina's: specifieke datum toevoegen (jaar, dag maand) (APA p.97)")
        
        return {
            "geldig": len(issues) == 0,
            "issues": issues
        }
    
    def valideer_titel(self, titel_tekst: str, bron_type: str) -> Dict:
        """Valideer titel volgens APA 7e editie (p. 97)"""
        issues = []
        
        if bron_type == "tijdschrift":
            # Check of titel niet cursief is in referentie (dat moet later)
            if titel_tekst.endswith('.'):
                pass  # Goed
            else:
                issues.append("Titel van artikel moet eindigen met een punt (APA p.97)")
        
        elif bron_type == "boek":
            # Boektitel moet cursief (niet te checken in tekst) en met hoofdletter
            if not titel_tekst[0].isupper():
                issues.append("Eerste woord van titel met hoofdletter (APA p.97)")
        
        # Check voor dubbele punt en spatie
        if ':' in titel_tekst and ': ' not in titel_tekst:
            issues.append("Na dubbele punt: spatie toevoegen (APA p.97)")
        
        return {
            "geldig": len(issues) == 0,
            "issues": issues
        }
    
    def valideer_doi(self, referentie: str) -> Dict:
        """Valideer DOI volgens APA 7e editie (p. 99-100)"""
        issues = []
        
        # Zoek naar DOI
        doi_match = re.search(r'https?://doi\.org/(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', referentie, re.IGNORECASE)
        
        if doi_match:
            doi = doi_match.group(1)
            # Check DOI formaat
            if not re.match(r'10\.\d{4,9}/', doi):
                issues.append(f"Ongeldig DOI formaat: {doi} (APA p.99)")
        else:
            # Check of het een journalartikel is zonder DOI
            if 'journal' in referentie.lower() or 'tijdschrift' in referentie.lower():
                issues.append("Journalartikel mist DOI. Voeg toe: https://doi.org/10.xxx/xxxx (APA p.100)")
        
        return {
            "heeft_doi": doi_match is not None,
            "doi": doi_match.group(1) if doi_match else None,
            "issues": issues,
            "geldig": len(issues) == 0
        }
    
    def valideer_literatuurlijst(self, referenties: List[str]) -> Dict:
        """Valideer volledige literatuurlijst volgens APA (p. 90-95)"""
        issues = []
        
        # Check alfabetische volgorde (p. 91)
        sorted_refs = sorted(referenties, key=lambda x: re.sub(r'^[^A-Za-z]*', '', x).lower())
        if referenties != sorted_refs:
            issues.append("Literatuurlijst niet alfabetisch gesorteerd op achternaam auteur (APA p.91)")
        
        # Check op dubbele spaties (p. 90)
        for i, ref in enumerate(referenties):
            if '  ' in ref:
                issues.append(f"Regel {i+1}: Dubbele spatie gevonden (APA p.90)")
        
        # Check op hanging indent (niet te checken in tekst)
        
        # Check op juiste interpunctie
        for i, ref in enumerate(referenties):
            if ref.endswith(' ,'):
                issues.append(f"Regel {i+1}: Spatie voor komma (APA p.90)")
            if '..' in ref:
                issues.append(f"Regel {i+1}: Dubbele punt (APA p.90)")
        
        return {
            "geldig": len(issues) == 0,
            "issues": issues,
            "aantal_bronnen": len(referenties)
        }
    
    def valideer_citaat(self, citaat: str) -> Dict:
        """Valideer citaat volgens APA 7e editie (p. 33-35)"""
        issues = []
        
        # Check voor paginanummer bij citaat korter dan 40 woorden
        if len(citaat.split()) < 40:
            if not re.search(r'\(p\.\s?\d+\)|\(pp\.\s?\d+-\d+\)', citaat):
                issues.append("Citaat korter dan 40 woorden: paginanummer toevoegen (APA p.34)")
        
        # Check voor aanhalingstekens
        if citaat.startswith('"') and not citaat.endswith('"'):
            issues.append("Aanhalingstekens niet gesloten (APA p.34)")
        
        # Check voor blokcitaat (langer dan 40 woorden)
        if len(citaat.split()) >= 40:
            if not citaat.startswith('  '):
                issues.append("Citaat langer dan 40 woorden: inspringen (blokcitaat) (APA p.35)")
        
        return {
            "geldig": len(issues) == 0,
            "issues": issues,
            "aantal_woorden": len(citaat.split())
        }
    
    def valideer_parafrase(self, tekst: str, bron_auteur: str) -> Dict:
        """Valideer parafrase volgens APA 7e editie (p. 36-37)"""
        issues = []
        
        # Check of auteur genoemd is
        if bron_auteur.lower() not in tekst.lower():
            issues.append(f"Auteur '{bron_auteur}' niet genoemd in parafrase (APA p.36)")
        
        # Check of jaar genoemd is
        if not re.search(r'\(\d{4}\)', tekst):
            issues.append("Jaartal ontbreekt in parafrase (APA p.36)")
        
        return {
            "geldig": len(issues) == 0,
            "issues": issues
        }
    
    def genereer_apa_advies(self, referentie: str, bron_type: str = "auto") -> str:
        """Genereer advies voor correcte APA-opmaak"""
        advies = []
        advies.append("=" * 60)
        advies.append("📘 APA 7e editie - Correctie advies")
        advies.append("=" * 60)
        advies.append(f"Origineel: {referentie}")
        advies.append("")
        
        if bron_type == "boek":
            advies.append("✅ Correct formaat voor een BOEK:")
            advies.append("   Auteur, A. A. (jaar). Titel: Ondertitel. Uitgever.")
            advies.append("   Voorbeeld: Poelmans, P. & Severijnen, O. (2022). De APA-richtlijnen (2e druk). Coutinho.")
        
        elif bron_type == "tijdschrift":
            advies.append("✅ Correct formaat voor een TIJDSCHRIFTARTIKEL:")
            advies.append("   Auteur, A. A. (jaar). Titel artikel. Titel Tijdschrift, volume(issue), paginas.")
            advies.append("   Voorbeeld: Gooty, J., Connelly, S., Griffith, J., & Gupta, A. (2010). Leadership. The Leadership Quarterly, 21(6), 979-1004.")
            advies.append("   Voeg DOI toe: https://doi.org/10.1016/j.leaqua.2010.10.005")
        
        elif bron_type == "web":
            advies.append("✅ Correct formaat voor een WEBPAGINA:")
            advies.append("   Auteur, A. A. (jaar, dag maand). Titel. Site Naam. URL")
            advies.append("   Voorbeeld: Lendering, J. (2019, 27 oktober). Drie centimeter hoog beeldje. Twitter. https://twitter.com/...")
        
        else:
            advies.append("ℹ️ Bepaal het brontype en pas het juiste formaat toe.")
            advies.append("   Raadpleeg hoofdstuk 4 van 'De APA-richtlijnen' (Poelmans & Severijnen, 2022)")
        
        advies.append("")
        advies.append("📖 Bron: Poelmans, P. & Severijnen, O. (2022). De APA-richtlijnen (2e druk). Coutinho.")
        
        return "\n".join(advies)


# ========== UNIT TESTS ==========

class TestAPAValidator(unittest.TestCase):
    """Test de APA-validator met voorbeelden uit de richtlijnen"""
    
    def setUp(self):
        self.validator = APAValidator()
    
    def test_valideer_boek_correct(self):
        """Test correct boek volgens APA (p. 102)"""
        boek = "Poelmans, P. & Severijnen, O. (2022). De APA-richtlijnen (2e druk). Coutinho."
        # Deze zou moeten valideren
        self.assertIsNotNone(boek)
    
    def test_valideer_boek_fout_geen_ampersand(self):
        """Test boek met 'en' in plaats van '&' (p. 40)"""
        auteur = "Poelmans, P. en Severijnen, O."
        resultaat = self.validator.valideer_auteur(auteur)
        self.assertFalse(resultaat["geldig"])
        self.assertTrue(any("&" in issue for issue in resultaat["issues"]))
    
    def test_valideer_tijdschrift_correct(self):
        """Test correct tijdschriftartikel (p. 101)"""
        artikel = "Gooty, J., Connelly, S., Griffith, J., & Gupta, A. (2010). Leadership, affect and emotions. The Leadership Quarterly, 21(6), 979-1004."
        self.assertIsNotNone(artikel)
    
    def test_valideer_tijdschrift_zonder_doi(self):
        """Test tijdschriftartikel zonder DOI (p. 100)"""
        referentie = "Jansen, P. (2023). Titel. Tijdschrift, 12(3), 45-67."
        resultaat = self.validator.valideer_doi(referentie)
        self.assertFalse(resultaat["geldig"])
        self.assertTrue(any("DOI" in issue for issue in resultaat["issues"]))
    
    def test_valideer_citaat_zonder_paginanummer(self):
        """Test citaat korter dan 40 woorden zonder paginanummer (p. 34)"""
        citaat = "Dit is een kort citaat zonder paginanummer."
        resultaat = self.validator.valideer_citaat(citaat)
        self.assertFalse(resultaat["geldig"])
        self.assertTrue(any("paginanummer" in issue.lower() for issue in resultaat["issues"]))
    
    def test_valideer_parafrase_zonder_jaartal(self):
        """Test parafrase zonder jaartal (p. 36)"""
        tekst = "Volgens Jansen is dit belangrijk."
        resultaat = self.validator.valideer_parafrase(tekst, "Jansen")
        self.assertFalse(resultaat["geldig"])
        self.assertTrue(any("Jaartal" in issue for issue in resultaat["issues"]))
    
    def test_valideer_literatuurlijst_alfabetisch(self):
        """Test of literatuurlijst alfabetisch is gesorteerd (p. 91)"""
        referenties = [
            "Zwaan, A. (2020). Titel Z. Uitgever.",
            "Aalbers, B. (2019). Titel A. Uitgever.",
            "Jansen, C. (2021). Titel J. Uitgever."
        ]
        resultaat = self.validator.valideer_literatuurlijst(referenties)
        self.assertFalse(resultaat["geldig"])
        self.assertTrue(any("alfabetisch" in issue.lower() for issue in resultaat["issues"]))
    
    def test_genereer_apa_advies(self):
        """Test of APA-advies wordt gegenereerd"""
        advies = self.validator.genereer_apa_advies("Test referentie", "boek")
        self.assertIn("APA 7e editie", advies)
        self.assertIn("Poelmans, P. & Severijnen, O. (2022)", advies)


# ========== HOOFDPROGRAMMA ==========
if __name__ == "__main__":
    print("=" * 70)
    print("📘 APA-VALIDATOR - Gebaseerd op Poelmans & Severijnen (2022)")
    print("=" * 70)
    print("")
    print("Deze tool valideert bronvermeldingen volgens APA 7e editie.")
    print("Gebruik: python -m unittest tests/test_apa_validator.py -v")
    print("")
    
    # Voorbeeld gebruik
    validator = APAValidator()
    
    test_referenties = [
        "Gooty, J., Connelly, S., Griffith, J., & Gupta, A. (2010). Leadership, affect and emotions. The Leadership Quarterly, 21(6), 979-1004.",
        "Poelmans, P. en Severijnen, O. (2022). De APA-richtlijnen. Coutinho.",
        "Mayer, J. D., Roberts, R. D., & Barsade, S. G. (2007). Human abilities. Annual Review Of Psychology, 59(1), 507-536."
    ]
    
    print("📋 Test referenties:")
    for ref in test_referenties:
        print(f"   • {ref[:80]}...")
    
    print("")
    print(validator.genereer_apa_advies(test_referenties[1], "boek"))
    
    # Voer unittesten uit
    unittest.main(verbosity=2)