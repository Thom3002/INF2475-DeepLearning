import re
import jiwer
from typing import List, Union

def normalize_for_eval(text: str) -> str:
    """
    Normalização padrão para avaliação de ASR:
    Converte para minúsculas, remove pontuação e normaliza múltiplos espaços.
    """
    if not text:
        return ""
    text = text.lower()
    # Remove pontuação básica: . , ? ! ; : " ( ) [ ] * - / e aspas simples isoladas
    text = re.sub(r'[.,?!;:\"(){}\[\]\*\-\/]', ' ', text)
    # Garante que apóstrofos que restaram no texto não causem problemas (opcional)
    text = text.replace("'", "")
    # Remove múltiplos espaços e espaços no início/fim
    return " ".join(text.split()).strip()

def calculate_wer(reference: Union[str, List[str]], hypothesis: Union[str, List[str]]) -> float:
    """
    Calcula o Word Error Rate (WER) entre a(s) referência(s) e hipótese(s).
    """
    if isinstance(reference, str):
        ref_norm = normalize_for_eval(reference)
        hyp_norm = normalize_for_eval(hypothesis)
        if not ref_norm:
            return 0.0 if not hyp_norm else 1.0
        return jiwer.wer(ref_norm, hyp_norm)
    else:
        # Lista de referências/hipóteses
        refs_norm = [normalize_for_eval(r) for r in reference]
        hyps_norm = [normalize_for_eval(h) for h in hypothesis]
        
        # Filtra pares onde a referência ficou vazia após normalização (evita divisão por zero)
        valid_pairs = [(r, h) for r, h in zip(refs_norm, hyps_norm) if r]
        if not valid_pairs:
            return 0.0
            
        refs_filtered, hyps_filtered = zip(*valid_pairs)
        return jiwer.wer(list(refs_filtered), list(hyps_filtered))

def calculate_cer(reference: Union[str, List[str]], hypothesis: Union[str, List[str]]) -> float:
    """
    Calcula o Character Error Rate (CER) entre a(s) referência(s) e hipótese(s).
    """
    if isinstance(reference, str):
        ref_norm = normalize_for_eval(reference)
        hyp_norm = normalize_for_eval(hypothesis)
        if not ref_norm:
            return 0.0 if not hyp_norm else 1.0
        return jiwer.cer(ref_norm, hyp_norm)
    else:
        refs_norm = [normalize_for_eval(r) for r in reference]
        hyps_norm = [normalize_for_eval(h) for h in hypothesis]
        
        valid_pairs = [(r, h) for r, h in zip(refs_norm, hyps_norm) if r]
        if not valid_pairs:
            return 0.0
            
        refs_filtered, hyps_filtered = zip(*valid_pairs)
        return jiwer.cer(list(refs_filtered), list(hyps_filtered))
