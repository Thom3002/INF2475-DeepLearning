import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any

class EAFParser:
    """
    Parser para arquivos ELAN (.eaf) que extrai turnos de fala,
    locutores, tempos de início/fim (em milissegundos) e a transcrição original.
    """
    @staticmethod
    def parse(eaf_path: str | Path) -> List[Dict[str, Any]]:
        eaf_path = Path(eaf_path)
        if not eaf_path.exists():
            raise FileNotFoundError(f"Arquivo EAF não encontrado: {eaf_path}")
            
        tree = ET.parse(eaf_path)
        root = tree.getroot()
        
        # 1. Mapeia TIME_SLOT_ID -> TIME_VALUE (ms)
        time_slots = {}
        time_order_node = root.find("TIME_ORDER")
        if time_order_node is not None:
            for slot in time_order_node.findall("TIME_SLOT"):
                slot_id = slot.attrib.get("TIME_SLOT_ID")
                val = slot.attrib.get("TIME_VALUE")
                if slot_id and val is not None:
                    time_slots[slot_id] = int(val)
                    
        # 2. Itera sobre cada TIER (locutor)
        segments = []
        file_id = eaf_path.stem
        for tier in root.findall("TIER"):
            speaker = tier.attrib.get("TIER_ID")
            # Ignora a tier default sem dados relevantes
            if not speaker or speaker.lower() == "default":
                continue
                
            for annotation in tier.findall("ANNOTATION"):
                align_annot = annotation.find("ALIGNABLE_ANNOTATION")
                if align_annot is not None:
                    ref1 = align_annot.attrib.get("TIME_SLOT_REF1")
                    ref2 = align_annot.attrib.get("TIME_SLOT_REF2")
                    val_node = align_annot.find("ANNOTATION_VALUE")
                    
                    if ref1 and ref2 and val_node is not None:
                        start_ms = time_slots.get(ref1, 0)
                        end_ms = time_slots.get(ref2, 0)
                        text = val_node.text or ""
                        
                        segments.append({
                            "file_id": file_id,
                            "speaker": speaker,
                            "start_ms": start_ms,
                            "end_ms": end_ms,
                            "raw_text": text.strip()
                        })
                        
        # Ordena os segmentos cronologicamente pelo tempo de início
        segments.sort(key=lambda x: (x["start_ms"], x["speaker"]))
        return segments
