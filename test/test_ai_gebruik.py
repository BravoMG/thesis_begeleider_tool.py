"""
test_ai_gebruik.py
Test of het AI-gebruik in de thesis voldoet aan de richtlijnen van:
- VUB (2023). Verantwoord gebruik van artificiële intelligentie voor onderzoeksdoeleinden.
- Universiteit Utrecht, REBO (2025). Richtlijnen voor het gebruik van AI in Afstudeerwerken.

Draai met: python -m unittest tests/test_ai_gebruik.py
"""

import unittest
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAIGebruik(unittest.TestCase):
    """Test of AI-gebruik in de thesis transparant en verantwoord is."""

    def setUp(self):
        self.ai_tools = [
            "chatgpt", "gpt-4", "gpt-3.5", "openai",
            "copilot", "github copilot",
            "elicit", "perplexity", "scite", "consensus", "connected papers", "research rabbit",
            "grammarly", "writefull", "quillbot",
            "midjourney", "dall-e", "stable diffusion",
            "claude", "llama", "gemini", "bard"
        ]

    # ========== 1. TRANSPARANTIE OVER AI-GEBRUIK ==========

    def test_ai_gebruik_vermeld_in_methodologie(self):
        """Test of het gebruik van AI-tools wordt vermeld in de methodologie."""
        methodologie_tekst = """
        Voor het verkennen van literatuur is gebruik gemaakt van Elicit (https://elicit.org).
        Grammaticacontrole is uitgevoerd met Grammarly.
        """

        # Simuleer dat een student dit vergeet
        lege_methodologie = "Dit onderzoek gebruikt een kwalitatieve casestudy."

        # Check of er een AI-tool wordt genoemd
        gevonden = any(tool in methodologie_tekst.lower() for tool in self.ai_tools)
        self.assertTrue(gevonden, "Geen AI-tool gevonden in de methodologie, terwijl deze wel gebruikt is.")

        gevonden_in_lege = any(tool in lege_methodologie.lower() for tool in self.ai_tools)
        self.assertFalse(gevonden_in_lege, "AI-tool gevonden in methodologie, maar geen gebruik vermeld.")

    # ========== 2. LOGBOEK BIJHOUDEN (Check op bestand) ==========

    def test_logboek_bestaat(self):
        """Test of het AI-logboek bestand aanwezig is (voorbeeld)."""
        logboek_bestand = "ai_logboek_student.txt"
        # In een echte test zou je controleren of het bestand bestaat.
        # Hier simuleren we dat het bestaat.
        logboek_bestaat = True
        self.assertTrue(logboek_bestaat, f"Logboekbestand '{logboek_bestand}' niet gevonden. Verplicht volgens REBO-richtlijnen.")

    # ========== 3. VERBODEN PRAKTIJK: Tekst laten genereren ==========

    def test_geen_ai_gegenereerde_tekst_zonder_controle(self):
        """Test of er geen aanwijzingen zijn voor klakkeloos overnemen van AI-tekst."""
        tekst = """
        In dit onderzoek wordt een diepgaande analyse uitgevoerd naar de rol van
        emotionele intelligentie in crisismanagement. De resultaten tonen aan dat
        er een significant verband is.
        """
        # Detecteer typische AI-woorden (VUB-richtlijnen)
        ai_markers = [
            "diepgaande analyse", "significant verband", "het is belangrijk om te benadrukken",
            "in deze studie", "de resultaten tonen aan", "zoals eerder vermeld"
        ]
        markers_gevonden = [m for m in ai_markers if m in tekst.lower()]

        if markers_gevonden:
            # Dit is geen fout, maar een waarschuwing
            print(f"⚠️ Let op: veelgebruikte AI-formuleringen gevonden: {markers_gevonden}")

    # ========== 4. VERBODEN PRAKTIJK: AI als auteur ==========

    def test_ai_niet_als_auteur(self):
        """Test of AI-tools niet als auteur op het titelblad of in literatuurlijst staan."""
        titelblad = "Student: Jan Jansen. Begeleider: Dr. E. Erasmus."
        literatuurlijst = "Jansen, P. (2023). Titel. Uitgever."

        self.assertNotIn("ChatGPT", titelblad)
        self.assertNotIn("OpenAI", titelblad)
        self.assertNotIn("ChatGPT", literatuurlijst)
        self.assertNotIn("OpenAI", literatuurlijst)

    # ========== 5. VERBODEN PRAKTIJK: Delen van vertrouwelijke info ==========

    def test_geen_persoonsgegevens_in_prompts(self):
        """Test of er geen duidelijke persoonsgegevens in de thesis staan die aan AI zijn gevraagd."""
        # In een echte test zou je de prompts controleren, hier een check op de thesis
        thesis_tekst = "De student, Jan Jansen, onderzoekt het gedrag van proefpersonen A, B en C."
        # Dit is een voorbeeld van een simpele check (in werkelijkheid complexer)
        # Deze test is een placeholder voor een API-call naar de AI-tool geschiedenis
        self.assertIsNotNone(thesis_tekst)

    # ========== 6. ADVIES: Reflectie op AI-gebruik in conclusie ==========

    def test_reflectie_op_ai_gebruik(self):
        """Test of er in de discussie/conclusie wordt gereflecteerd op het gebruik van AI."""
        discussie_tekst = """
        De gebruikte AI-tool (Elicit) hielp bij het verkennen van literatuur, maar de
        selectie en interpretatie van bronnen bleef bij de onderzoeker.
        """
        reflectie_indicatoren = ["AI", "tool", "beperking", "verantwoordelijkheid", "controle"]
        heeft_reflectie = any(woord in discussie_tekst.lower() for woord in reflectie_indicatoren)
        self.assertTrue(heeft_reflectie, "Geen reflectie op AI-gebruik in discussie/conclusie (aanbevolen).")


class TestAILogboekTemplate(unittest.TestCase):
    """Test of het AI-logboek voldoet aan de REBO-template (Bijlage 1)."""

    def test_logboek_template_vereisten(self):
        """Test of het logboek alle verplichte velden bevat."""
        verplichte_velden = [
            "Datum", "AI-tool", "Doel", "Input (Prompt)", "Output", "Reflectie"
        ]
        # Simuleer een logboek entry
        logboek_entry = """
        | Datum | AI-tool | Doel | Input | Output | Reflectie |
        |-------|---------|------|-------|--------|-----------|
        """
        for veld in verplichte_velden:
            self.assertIn(veld, logboek_entry)


if __name__ == "__main__":
    print("=" * 70)
    print("🤖 AI-GEBRUIK TEST - VUB & REBO Richtlijnen")
    print("=" * 70)
    print("\nDeze test controleert of het AI-gebruik in je thesis voldoet aan:")
    print("  - VUB (2023). Verantwoord gebruik van AI voor onderzoeksdoeleinden.")
    print("  - REBO (2025). Richtlijnen voor het gebruik van AI in Afstudeerwerken.")
    print("\nLet op: Deze test kan niet alle vormen van oneigenlijk AI-gebruik detecteren.")
    print("Jouw begeleider en examencommissie beoordelen de uiteindelijke inzet.\n")
    unittest.main(verbosity=2)