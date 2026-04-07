"""
Process transcripties voor Master Bestuurskunde Thesis
Analyseert persconferenties en Kamerdebatten op EI-kenmerken

Gebaseerd op:
- Handleiding Afstudeertraject Master Bestuurskunde 2023-2024
- Transcripties van 6 publieke optredens in 2021
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

class TranscriptieAnalyse:
    """Analyseert transcripties op emotionele intelligentie kenmerken"""
    
    def __init__(self):
        self.ei_competenties = {
            "zelfbewustzijn": {
                "keywords": ["erken", "fout", "spijt", "eigen rol", "verantwoordelijkheid", "ik reken het mij aan"],
                "description": "Herkenning van eigen emoties, sterktes, zwaktes"
            },
            "zelfregulatie": {
                "keywords": ["kalm", "rustig", "beheerst", "niet defensief", "blijf kalm", "ik snap"],
                "description": "Beheersen van eigen emoties onder druk"
            },
            "empathie": {
                "keywords": ["begrijp", "snap", "teleurstelling", "verdrietig", "zwaar", "impact", "zorgen"],
                "description": "Waarnemen en begrijpen van emoties van anderen"
            },
            "sociale_vaardigheden": {
                "keywords": ["samen", "dank", "waardering", "verbinding", "collega", "team", "beschermen"],
                "description": "Relaties opbouwen en samenwerking faciliteren"
            }
        }
        
        self.analyse_resultaten = {
            "metadata": {},
            "per_transcriptie": [],
            "totaal_overzicht": {}
        }
    
    def laad_transcriptie(self, bestandspad: str) -> Dict:
        """Laad een transcriptie bestand en extraheer metadata"""
        with open(bestandspad, 'r', encoding='utf-8') as f:
            tekst = f.read()
        
        # Extraheer datum uit bestandsnaam of eerste regels
        bestandsnaam = os.path.basename(bestandspad)
        datum_match = re.search(r'(\d{4}-\d{2}-\d{2})', bestandsnaam)
        if datum_match:
            datum = datum_match.group(1)
        else:
            # Probeer uit tekst te halen
            datum = "onbekend"
        
        # Bepaal type (persconferentie of kamerdebat)
        if "kamerdebat" in bestandsnaam.lower():
            type_event = "Kamerdebat"
        else:
            type_event = "Persconferentie"
        
        # Extraheer sprekers
        sprekers = []
        if "rutte" in tekst.lower():
            sprekers.append("Mark Rutte")
        if "de jonge" in tekst.lower() or "de jongen" in tekst.lower():
            sprekers.append("Hugo de Jonge")
        
        return {
            "bestand": bestandsnaam,
            "datum": datum,
            "type": type_event,
            "sprekers": sprekers,
            "tekst": tekst,
            "aantal_woorden": len(tekst.split())
        }
    
    def analyseer_ei_kenmerken(self, tekst: str) -> Dict:
        """Analyseer tekst op EI-kenmerken per competentie"""
        resultaten = {}
        tekst_lower = tekst.lower()
        
        for competentie, data in self.ei_competenties.items():
            matches = []
            for keyword in data["keywords"]:
                if keyword.lower() in tekst_lower:
                    # Zoek context (50 karakters rondom het keyword)
                    for match in re.finditer(keyword.lower(), tekst_lower):
                        start = max(0, match.start() - 50)
                        end = min(len(tekst), match.end() + 50)
                        context = tekst[start:end]
                        matches.append({
                            "keyword": keyword,
                            "context": context.strip()
                        })
            
            resultaten[competentie] = {
                "aantal_mentions": len(matches),
                "voorbeelden": matches[:3],  # Max 3 voorbeelden
                "aanwezig": len(matches) > 0
            }
        
        return resultaten
    
    def analyseer_vergelijk(self, transcripties: List[Dict]) -> Dict:
        """Vergelijk Rutte en De Jonge op EI-kenmerken"""
        rutte_tekst = ""
        dejonge_tekst = ""
        
        for t in transcripties:
            if "Mark Rutte" in t["sprekers"]:
                rutte_tekst += t["tekst"]
            if "Hugo de Jonge" in t["sprekers"]:
                dejonge_tekst += t["tekst"]
        
        return {
            "Mark Rutte": self.analyseer_ei_kenmerken(rutte_tekst),
            "Hugo de Jonge": self.analyseer_ei_kenmerken(dejonge_tekst)
        }
    
    def valideer_handleiding(self, analyse: Dict) -> Dict:
        """Valideer of de analyse voldoet aan de handleiding eisen"""
        handleiding_eisen = {
            "minimaal_3_bronnen": len(analyse["per_transcriptie"]) >= 3,
            "beide_leiders_geanalyseerd": len(analyse.get("vergelijk", {})) >= 2,
            "alle_4_ei_competenties": all(
                analyse.get("vergelijk", {}).get("Mark Rutte", {}).get(comp, {}).get("aanwezig", False)
                or analyse.get("vergelijk", {}).get("Hugo de Jonge", {}).get(comp, {}).get("aanwezig", False)
                for comp in self.ei_competenties.keys()
            )
        }
        
        return handleiding_eisen
    
    def voer_analyse_uit(self, data_map: str) -> Dict:
        """Voer volledige analyse uit op alle transcripties in de map"""
        
        # Zoek alle .txt bestanden
        transcriptie_bestanden = []
        for bestand in os.listdir(data_map):
            if bestand.endswith('.txt'):
                transcriptie_bestanden.append(os.path.join(data_map, bestand))
        
        print(f"📄 Gevonden transcripties: {len(transcriptie_bestanden)}")
        
        # Analyseer elke transcriptie
        for bestand in transcriptie_bestanden:
            print(f"   Analyseren: {os.path.basename(bestand)}")
            data = self.laad_transcriptie(bestand)
            ei_analyse = self.analyseer_ei_kenmerken(data["tekst"])
            
            self.analyse_resultaten["per_transcriptie"].append({
                "metadata": {
                    "bestand": data["bestand"],
                    "datum": data["datum"],
                    "type": data["type"],
                    "sprekers": data["sprekers"],
                    "aantal_woorden": data["aantal_woorden"]
                },
                "ei_analyse": ei_analyse
            })
        
        # Voer vergelijkende analyse uit
        self.analyse_resultaten["vergelijk"] = self.analyseer_vergelijk(
            [self.laad_transcriptie(b) for b in transcriptie_bestanden]
        )
        
        # Valideer tegen handleiding
        self.analyse_resultaten["handleiding_validatie"] = self.valideer_handleiding(
            self.analyse_resultaten
        )
        
        # Voeg totaal overzicht toe
        totaal_mentions = {}
        for comp in self.ei_competenties.keys():
            totaal_mentions[comp] = sum(
                t["ei_analyse"].get(comp, {}).get("aantal_mentions", 0)
                for t in self.analyse_resultaten["per_transcriptie"]
            )
        
        self.analyse_resultaten["totaal_overzicht"] = {
            "aantal_transcripties": len(transcriptie_bestanden),
            "totaal_aantal_woorden": sum(
                self.laad_transcriptie(b)["aantal_woorden"] 
                for b in transcriptie_bestanden
            ),
            "totaal_ei_mentions": totaal_mentions,
            "meest_voorkomende_competentie": max(totaal_mentions, key=totaal_mentions.get)
        }
        
        return self.analyse_resultaten
    
    def exporteer_naar_json(self, output_path: str):
        """Exporteer analyse resultaten naar JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analyse_resultaten, f, indent=2, ensure_ascii=False)
        print(f"✅ Analyse geëxporteerd naar: {output_path}")
    
    def genereer_rapport(self) -> str:
        """Genereer een leesbaar rapport van de analyse"""
        rapport = []
        rapport.append("=" * 70)
        rapport.append("📘 THESIS ANALYSE RAPPORT - MASTER BESTUURSKUNDE")
        rapport.append("Erasmus Universiteit Rotterdam")
        rapport.append(f"Datum: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
        rapport.append("=" * 70)
        rapport.append("")
        
        # Overzicht
        rapport.append("📊 OVERZICHT GEANALYSEERDE DATA")
        rapport.append("-" * 40)
        rapport.append(f"Aantal transcripties: {self.analyse_resultaten['totaal_overzicht']['aantal_transcripties']}")
        rapport.append(f"Totaal aantal woorden: {self.analyse_resultaten['totaal_overzicht']['totaal_aantal_woorden']:,}")
        rapport.append("")
        
        # Per transcriptie
        rapport.append("📄 PER TRANSCRIPTIE")
        rapport.append("-" * 40)
        for t in self.analyse_resultaten["per_transcriptie"]:
            meta = t["metadata"]
            rapport.append(f"\n📌 {meta['bestand']}")
            rapport.append(f"   Datum: {meta['datum']} | Type: {meta['type']}")
            rapport.append(f"   Sprekers: {', '.join(meta['sprekers'])}")
            rapport.append(f"   Woorden: {meta['aantal_woorden']:,}")
        
        # EI-kenmerken vergelijking
        rapport.append("")
        rapport.append("🧠 EMOTIONELE INTELLIGENTIE - VERGELIJKING")
        rapport.append("-" * 40)
        
        for leider, analyse in self.analyse_resultaten.get("vergelijk", {}).items():
            rapport.append(f"\n👤 {leider}:")
            for comp, data in analyse.items():
                comp_naam = comp.replace("_", " ").title()
                status = "✅" if data["aanwezig"] else "❌"
                rapport.append(f"   {status} {comp_naam}: {data['aantal_mentions']} mentions")
                if data["voorbeelden"]:
                    for ex in data["voorbeelden"][:1]:  # Eerste voorbeeld
                        rapport.append(f"      → \"...{ex['context']}...\"")
        
        # Handleiding validatie
        rapport.append("")
        rapport.append("📚 VALIDATIE TEGEN HANDLEIDING")
        rapport.append("-" * 40)
        for criterium, voldaan in self.analyse_resultaten["handleiding_validatie"].items():
            status = "✅" if voldaan else "❌"
            rapport.append(f"   {status} {criterium.replace('_', ' ').title()}")
        
        # Conclusie
        rapport.append("")
        rapport.append("🎯 CONCLUSIE")
        rapport.append("-" * 40)
        if all(self.analyse_resultaten["handleiding_validatie"].values()):
            rapport.append("✅ Analyse voldoet aan alle handleiding eisen!")
            rapport.append("   De scriptie kan worden beoordeeld volgens de matrix in bijlage 2.")
        else:
            rapport.append("⚠️ Analyse voldoet niet aan alle handleiding eisen.")
            rapport.append("   Controleer de ontbrekende onderdelen hierboven.")
        
        rapport.append("")
        rapport.append("=" * 70)
        
        return "\n".join(rapport)


# ========== VOORBEELD GEBRUIK ==========
if __name__ == "__main__":
    # Pad naar de map met transcripties
    # Pas dit aan naar jouw situatie
    transcriptie_map = "data/transcripties/"
    
    # Controleer of de map bestaat
    if not os.path.exists(transcriptie_map):
        print(f"⚠️ Map niet gevonden: {transcriptie_map}")
        print("   Maak de map aan en plaats de transcriptie bestanden erin.")
        print("   Of pas het pad aan in de code.")
    else:
        # Voer analyse uit
        analyser = TranscriptieAnalyse()
        resultaten = analyser.voer_analyse_uit(transcriptie_map)
        
        # Exporteer naar JSON
        analyser.exporteer_naar_json("data/analyse_output/analyse_resultaten.json")
        
        # Genereer en print rapport
        rapport = analyser.genereer_rapport()
        print(rapport)
        
        # Sla rapport op
        with open("data/analyse_output/analyse_rapport.txt", "w", encoding="utf-8") as f:
            f.write(rapport)
        print("\n✅ Rapport opgeslagen in: data/analyse_output/analyse_rapport.txt")