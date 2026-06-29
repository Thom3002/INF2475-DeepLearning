import math
from pathlib import Path
import soundfile as sf
import numpy as np
import scipy.signal

def resample_and_mono(audio_path: str | Path, target_sr: int = 16000) -> tuple[np.ndarray, int]:
    """
    Carrega um arquivo de áudio WAV, converte para Mono (se for Estéreo)
    e altera a taxa de amostragem para target_sr usando scipy.signal.resample_poly.
    
    Retorna:
        tuple[np.ndarray, int]: (dados do áudio em mono resamparado, target_sr)
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Áudio não encontrado em: {audio_path}")
        
    data, sr = sf.read(audio_path)
    
    # 1. Se for estéreo (2 canais), calcula a média dos canais para obter Mono
    if len(data.shape) > 1 and data.shape[1] > 1:
        data = data.mean(axis=1)
        
    # 2. Se a taxa de amostragem for diferente da desejada, faz o resampling
    if sr != target_sr:
        gcd = math.gcd(target_sr, sr)
        up = target_sr // gcd
        down = sr // gcd
        data = scipy.signal.resample_poly(data, up, down)
        
    return data, target_sr

def slice_audio(audio_data: np.ndarray, sr: int, start_ms: float, end_ms: float) -> np.ndarray:
    """
    Fatia um trecho do array de áudio correspondente ao intervalo em milissegundos.
    """
    start_idx = int(round(start_ms * sr / 1000.0))
    end_idx = int(round(end_ms * sr / 1000.0))
    
    # Garantir limites válidos do array
    start_idx = max(0, start_idx)
    end_idx = min(len(audio_data), end_idx)
    
    return audio_data[start_idx:end_idx]

def save_wav(output_path: str | Path, audio_data: np.ndarray, sr: int) -> None:
    """
    Salva o array de áudio em formato WAV utilizando a biblioteca soundfile.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_path, audio_data, sr)
