import os
import numpy as np
from pathlib import Path
import pytest

from src.preprocessing.text import clean_text_gabarito_a, normalize_text_gabarito_b
from src.preprocessing.parser import EAFParser
from src.preprocessing.audio import resample_and_mono, slice_audio

# --- Testes de Limpeza e Normalização de Texto ---

def test_clean_text_gabarito_a():
    # Caso 1: Remocão de pausas e convertendo para minúsculo
    assert clean_text_gabarito_a("Vozes // né /") == "vozes né"
    
    # Caso 2: Remoção de overlap < > mantendo o conteúdo
    assert clean_text_gabarito_a("<hum hum> //") == "hum hum"
    
    # Caso 3: Remoção de stutters (&)
    assert clean_text_gabarito_a("pa &fan &van pa mim") == "pa pa mim"
    
    # Caso 4: Remoção de disfluência [/N]
    assert clean_text_gabarito_a("eu nũ dou [/1] faço nada") == "eu nũ dou faço nada"
    
    # Caso 5: Remoção de ininteligíveis xxx/yyyy e interrupção +
    assert clean_text_gabarito_a("falar yyyy + xxx") == "falar"
    
    # Caso 6: Manutenção de apóstrofos em contrações coloquiais
    assert clean_text_gabarito_a("p' cê fazer e'") == "p' cê fazer e'"


def test_normalize_text_gabarito_b():
    # Caso 1: Normalização básica de coloquiais e manutenção de "né"
    text = "eu nũ tava tomando / né //"
    assert normalize_text_gabarito_b(text) == "eu não estava tomando né"
    
    # Caso 2: Normalização de contrações coloquiais com apóstrofo
    text = "p' cê fazer com e'"
    assert normalize_text_gabarito_b(text) == "para você fazer com ele"
    
    # Caso 3: Interjeição expressiva "uai" deve ser mantida
    text = "uai / ficou muito tempo //"
    assert normalize_text_gabarito_b(text) == "uai ficou muito tempo"
    
    # Caso 4: Mapeamento de termos diversos
    text = "tamo aqui / sior e siora"
    assert normalize_text_gabarito_b(text) == "estamos aqui senhor e senhora"


# --- Testes do Parser de EAF ---

def test_eaf_parser():
    # Usando o arquivo real besqau01.eaf para testar
    eaf_path = Path("data/input/raw/C-ORAL-ESQ/c-oral-esq_audio_alignment/besqau01/besqau01.eaf")
    assert eaf_path.exists(), "O arquivo besqau01.eaf precisa existir no workspace para rodar os testes"
    
    segments = EAFParser.parse(eaf_path)
    
    assert len(segments) > 0
    assert segments[0]["file_id"] == "besqau01"
    assert "speaker" in segments[0]
    assert "start_ms" in segments[0]
    assert "end_ms" in segments[0]
    assert "raw_text" in segments[0]
    
    # Verifica ordenação temporal cronológica
    for i in range(1, len(segments)):
        assert segments[i]["start_ms"] >= segments[i-1]["start_ms"]


# --- Testes de Processamento de Áudio ---

def test_audio_resample_and_slice(tmp_path):
    # Cria um sinal de áudio sintético (1 segundo de estéreo a 22050 Hz)
    sr_orig = 22050
    duration = 1.0
    t = np.linspace(0, duration, int(sr_orig * duration), endpoint=False)
    # Sinal estéreo (2 canais)
    signal = np.stack([np.sin(2 * np.pi * 440 * t), np.cos(2 * np.pi * 440 * t)], axis=1)
    
    test_wav_path = tmp_path / "test_synth.wav"
    import soundfile as sf
    sf.write(test_wav_path, signal, sr_orig)
    
    # Teste de resampling e mono
    mono_data, target_sr = resample_and_mono(test_wav_path, target_sr=16000)
    
    assert target_sr == 16000
    assert len(mono_data.shape) == 1  # Deve ser mono (1D array)
    # Comprimento esperado = 1s * 16000Hz = 16000 samples
    assert abs(len(mono_data) - 16000) < 5
    
    # Teste de corte (slicing) de 250ms a 750ms (duração de 500ms)
    sliced = slice_audio(mono_data, target_sr, start_ms=250.0, end_ms=750.0)
    expected_length = int(0.500 * 16000)
    assert abs(len(sliced) - expected_length) < 5
