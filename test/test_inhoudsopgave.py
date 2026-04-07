"""
test_inhoudsopgave.py
Test of de thesis een correcte inhoudsopgave heeft volgens Word-richtlijnen.
Gebaseerd op: SeniorWeb.nl (2020). Inhoudsopgave maken met Word.

Draai met: python -m unittest tests/test_inhoudsopgave.py
"""

import unittest
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class InhoudsopgaveValidator:
    """Valideert of een thesis een correcte inhoudsopgave heeft"""
    
    def __init__(self):
        self.kop_niveaus = {
            "Kop 1": r'^(\d+\.\s+[A-Z])|(Hoofdstuk\s+\d+)',
            "Kop 2": r'^\d+\.\d+\s+[A-Z]',
            "Kop 3": r'^\d+\.\d+\.\d+\s+[A-Z]'
        }
    
    def valideer_kop_structuur(self, tekst: str) -> dict:
        """Valideer of koppen correct zijn genummerd en gestructureerd"""
        feedback = {
            "aantal_kop1": 0,
            "aantal_kop2": 0,
            "aantal_kop3": 0,
            "fouten": [],
            "waarschuwingen": []
        }
        
        regels = tekst.split('\n')
        huidig_kop1 = 0
        
        for regel in regels:
            # Check voor Kop 1 (hoofdstukken)
            if re.match(self.kop_niveaus["Kop 1"], regel.strip()):
                feedback["aantal_kop1"] += 1
                huidig_kop1 += 1
            
            # Check voor Kop 2 (paragrafen)
            elif re.match(self.kop_niveaus["Kop 2"], regel.strip()):
                feedback["aantal_kop2"] += 1
                # Check of er een Kop 1 aan voorafgaat
                if huidig_kop1 == 0:
                    feedback["fouten"].append(f"Kop 2 '{regel.strip()[:50]}...' zonder voorgaande Kop 1")
            
            # Check voor Kop 3 (subparagrafen)
            elif re.match(self.kop_niveaus["Kop 3"], regel.strip()):
                feedback["aantal_kop3"] += 1
        
        # Check of er voldoende structuur is
        if feedback["aantal_kop1"] < 3:
            feedback["waarschuwingen"].append(f"Weinig hoofdstukken ({feedback['aantal_kop1']}) - minimaal 3 aanbevolen voor een thesis")
        
        if feedback["aantal_kop2"] == 0 and feedback["aantal_kop3"] == 0:
            feedback["waarschuwingen"].append("Geen tussenkoppen (Kop 2/Kop 3) gevonden - thesis mist structuur")
        
        return feedback
    
    def valideer_inhoudsopgave(self, inhoudsopgave: str) -> dict:
        """Valideer of de inhoudsopgave correct is opgebouwd"""
        feedback = {
            "bevat_paginanummers": False,
            "bevat_hoofdstukken": False,
            "bevat_inspringing": False,
            "fouten": []
        }
        
        # Check of er paginanummers zijn (meestal aan het einde van de regel)
        paginanummer_pattern = r'\s+\.{2,}\s+\d+$'
        if re.search(paginummer_pattern, inhoudsopgave, re.MULTILINE):
            feedback["bevat_paginanummers"] = True
        else:
            feedback["fouten"].append("Inhoudsopgave bevat geen paginanummers")
        
        # Check of er hoofdstukken zijn (Kop 1 niveau)
        hoofdstuk_pattern = r'^(\d+\.\s+[A-Z]|Hoofdstuk\s+\d+)'
        if re.search(hoofdstuk_pattern, inhoudsopgave, re.MULTILINE):
            feedback["bevat_hoofdstukken"] = True
        else:
            feedback["fouten"].append("Inhoudsopgave bevat geen hoofdstukken")
        
        # Check of er inspringing is (tab of spaties aan begin van regel)
        if re.search(r'^\s{2,}', inhoudsopgave, re.MULTILINE):
            feedback["bevat_inspringing"] = True
        
        return feedback


class TestInhoudsopgave(unittest.TestCase):
    """Test of de inhoudsopgave voldoet aan de richtlijnen"""
    
    def setUp(self):
        self.validator = InhoudsopgaveValidator()
    
    def test_kop_structuur_correct(self):
        """Test of koppen correct zijn gestructureerd"""
        goede_structuur = """
        1. Inleiding
        1.1 Aanleiding
        1.2 Probleemstelling
        2. Theorie
        2.1 Emotionele intelligentie
        2.1.1 Het ability-model
        2.1.2 Het gemengde model
        3. Methode
        """
        
        resultaat = self.validator.valideer_kop_structuur(goede_structuur)
        self.assertEqual(resultaat["aantal_kop1"], 3)
        self.assertEqual(resultaat["aantal_kop2"], 3)
        self.assertEqual(resultaat["aantal_kop3"], 2)
        self.assertEqual(len(resultaat["fouten"]), 0)
    
    def test_kop_structuur_mist_kop1(self):
        """Test of ontbrekende Kop 1 wordt gedetecteerd"""
        structuur_zonder_kop1 = """
        1.1 Aanleiding (geen voorgaande Kop 1!)
        1.2 Probleemstelling
        """
        
        resultaat = self.validator.valideer_kop_structuur(structuur_zonder_kop1)
        self.assertGreater(len(resultaat["fouten"]), 0)
    
    def test_inhoudsopgave_heeft_paginanummers(self):
        """Test of inhoudsopgave paginanummers bevat"""
        goede_inhoudsopgave = """
        1. Inleiding ............................................. 1
        1.1 Aanleiding .......................................... 2
        1.2 Probleemstelling .................................... 3
        2. Theorie .............................................. 5
        2.1 Emotionele intelligentie ............................ 5
        """
        
        resultaat = self.validator.valideer_inhoudsopgave(goede_inhoudsopgave)
        self.assertTrue(resultaat["bevat_paginanummers"])
        self.assertTrue(resultaat["bevat_hoofdstukken"])
    
    def test_inhoudsopgave_zonder_paginanummers(self):
        """Test of inhoudsopgave zonder paginanummers wordt gedetecteerd"""
        slechte_inhoudsopgave = """
        1. Inleiding
        1.1 Aanleiding
        1.2 Probleemstelling
        """
        
        resultaat = self.validator.valideer_inhoudsopgave(slechte_inhoudsopgave)
        self.assertIn("geen paginanummers", " ".join(resultaat["fouten"]).lower())
    
    def test_geen_hoofdstukken_in_inhoudsopgave(self):
        """Test of inhoudsopgave zonder hoofdstukken wordt gedetecteerd"""
        inhoudsopgave_zonder_hoofdstukken = """
        Inleiding ................................................ 1
        Theorie .................................................. 5
        Methode .................................................. 10
        """
        
        resultaat = self.validator.valideer_inhoudsopgave(inhoudsopgave_zonder_hoofdstukken)
        self.assertFalse(resultaat["bevat_hoofdstukken"])
        self.assertIn("geen hoofdstukken", " ".join(resultaat["fouten"]).lower())


# ========== HANDMATIGE CHECKLIST VOOR STUDENTEN ==========
def genereer_inhoudsopgave_checklist() -> str:
    """Genereer een checklist voor studenten om hun inhoudsopgave te controleren"""
    checklist = """
================================================================================
📑 INHOUDSOPGAVE CHECKLIST - Voor het inleveren van je thesis
================================================================================

VOORDAT JE DE INHOUDSOPGAVE MAAKT:
--------------------------------------------------------------------------------
☐ Alle hoofdstuktitels hebben de stijl 'Kop 1'
☐ Alle paragrafen hebben de stijl 'Kop 2'
☐ Alle subparagrafen hebben de stijl 'Kop 3' (indien aanwezig)
☐ De titel van het document heeft de stijl 'Titel' (niet in inhoudsopgave)

INHOUDSPOGAVE INVOEGEN:
--------------------------------------------------------------------------------
☐ Ga naar het tabblad 'Verwijzingen'
☐ Klik op 'Inhoudsopgave'
☐ Kies 'Automatische inhoudsopgave 2'

VOOR HET INLEVEREN (ALTijd DOEN!):
--------------------------------------------------------------------------------
☐ Klik op de inhoudsopgave
☐ Klik op 'Bijwerken'
☐ Kies 'In zijn geheel bijwerken'
☐ Controleer of alle paginanummers kloppen

CHECKLIST VOOR DE DEFINITIEVE VERSIE:
--------------------------------------------------------------------------------
☐ De inhoudsopgave staat op de juiste plek (na titelpagina, voor inleiding)
☐ Alle hoofdstukken staan in de inhoudsopgave
☐ Alle paginanummers zijn correct
☐ De inspringniveaus kloppen (Kop 2 springt in t.o.v. Kop 1)
☐ Er staan geen handmatige paginanummers in de inhoudsopgave
☐ De inhoudsopgave is niet handmatig getypt maar automatisch gegenereerd

VEELGEMAAKTE FOUTEN (check hierop!):
--------------------------------------------------------------------------------
❌ Kop verschijnt niet in inhoudsopgave → oplossing: controleer of de kop de juiste stijl heeft
❌ Paginanummers kloppen niet → oplossing: klik op 'Bijwerken' → 'In zijn geheel bijwerken'
❌ Titel staat in inhoudsopgave → oplossing: verander de stijl van de titel naar 'Titel'
❌ Verkeerd inspringniveau → oplossing: controleer of je Kop 1, Kop 2 of Kop 3 hebt gebruikt
❌ Inhoudsopgave is handmatig getypt → oplossing: verwijder en voeg automatische inhoudsopgave toe

================================================================================
Bron: SeniorWeb.nl (2020). Inhoudsopgave maken met Word.
================================================================================
"""
    return checklist


if __name__ == "__main__":
    print(genereer_inhoudsopgave_checklist())
    print("\n" + "="*70)
    print("Draai de tests met: python -m unittest tests/test_inhoudsopgave.py -v")
    unittest.main(verbosity=2)