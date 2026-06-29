import pytest
from src.evaluation.metrics import normalize_for_eval, calculate_wer, calculate_cer

def test_normalize_for_eval():
    assert normalize_for_eval("O Gato, comeu: o Rato!") == "o gato comeu o rato"
    assert normalize_for_eval("p' cê fazer e'") == "p cê fazer e"  # Remove apóstrofo na avaliação padrão
    assert normalize_for_eval("   muitos   espaços   ") == "muitos espaços"
    assert normalize_for_eval("") == ""

def test_calculate_wer():
    # Caso simples: 1 substituição
    # ref:  "glicose alta" (2 palavras)
    # hyp:  "glicose baixa" (2 palavras)
    # 1 substituição / 2 palavras = 0.50 WER
    assert calculate_wer("glicose alta", "glicose baixa") == pytest.approx(0.50)
    
    # Caso com lista de sentenças
    refs = ["o gato comeu", "banana é bom"]
    hyps = ["o gato correu", "banana é bom"]
    # Primeiro par: 1 subst em 3 palavras = 0.333
    # Segundo par: 0 erros em 3 palavras = 0.0
    # Total de erros: 1 subst em 6 palavras = 1/6 = 0.1666...
    assert calculate_wer(refs, hyps) == pytest.approx(1/6)

def test_calculate_cer():
    # Caso simples: 1 erro de caractere
    # ref: "casa" (4 chars)
    # hyp: "caza" (4 chars)
    # 1 erro / 4 chars = 0.25 CER
    assert calculate_cer("casa", "caza") == pytest.approx(0.25)
    
    # Caso com listas
    refs = ["casa", "bola"]
    hyps = ["caza", "bola"]
    # Total chars: 8. Total erros: 1. CER = 1/8 = 0.125
    assert calculate_cer(refs, hyps) == pytest.approx(0.125)

def test_empty_edge_cases():
    assert calculate_wer("", "") == 0.0
    assert calculate_wer("glicose", "") == 1.0
    assert calculate_wer("", "glicose") == 1.0
