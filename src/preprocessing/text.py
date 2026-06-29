import re

# Dicionário de mapeamento coloquial -> padrão para o Gabarito B
COLLOQUIAL_MAP = {
    "nũ": "não",
    "cê": "você",
    "ocê": "você",
    "tamo": "estamos",
    "tamos": "estamos",
    "tava": "estava",
    "tavam": "estavam",
    "tar": "estar",
    "tá": "está",
    "tão": "estão",
    "sior": "senhor",
    "siora": "senhora",
    "ea": "ela",
    "eas": "elas",
    "e'": "ele",
    "es": "eles",
    "p'": "para",
    "c'": "com",
    "co": "com o",
    "cos": "com os",
    "pa": "para",
    "pra": "para",
    "pro": "para o",
    "pras": "para as",
    "num": "em um",
    "numa": "em uma",
    "dum": "de um",
    "duma": "de uma",
    "tendi": "entendi",
    "tendeu": "entendeu",
    "aque'": "aquele",
    "to": "estou",
    "tô": "estou",
}

def clean_text_gabarito_a(text: str) -> str:
    """
    Preprocessamento para o Gabarito A (Coloquial Mantido):
    1. Remove marcas de pausa '/' e '//'
    2. Remove marcadores de overlap '<' e '>', mantendo o texto interno
    3. Remove disfluências '[/N]' (onde N é um número)
    4. Remove stutters (palavras iniciadas com '&')
    5. Remove marcadores de interrupção '+'
    6. Remove marcadores de ininteligível 'xxx' e 'yyyy'
    7. Converte para minúsculo
    8. Remove pontuação básica (mantendo o apóstrofo "'" para contrações)
    9. Remove espaços múltiplos
    """
    if not text:
        return ""
        
    # Converte para minúsculo primeiro para simplificar processamento
    text = text.lower()
    
    # 1. Remove disfluências '[/N]' (ex: [/1], [/2], [/3])
    text = re.sub(r'\[/\d+\]', ' ', text)
    
    # 2. Remove stutters (palavras que começam com '&')
    text = re.sub(r'&\w+', ' ', text)
    
    # 3. Remove marcas de ininteligível 'xxx' e 'yyyy'
    text = re.sub(r'\bxxx\b', ' ', text)
    text = re.sub(r'\byyyy\b', ' ', text)
    
    # 4. Remove marcações de overlap '<' e '>', mantendo o texto interno
    text = text.replace('<', ' ').replace('>', ' ')
    
    # 5. Remove marcas de pausa e interrupção
    text = text.replace('//', ' ').replace('/', ' ').replace('+', ' ')
    
    # 6. Remove pontuação básica, mantendo apenas letras, espaços e o apóstrofo "'"
    # Exclui: .,?!;:"()[]{}*- e outros caracteres especiais
    text = re.sub(r'[.,?!;:\"(){}\[\]\*\-\s]+', ' ', text)
    
    # 7. Normaliza espaçamentos extras
    text = " ".join(text.split())
    
    return text.strip()

def normalize_text_gabarito_b(text: str) -> str:
    """
    Preprocessamento para o Gabarito B (Normalizado):
    1. Executa a limpeza básica do Gabarito A.
    2. Mapeia os termos coloquiais de acordo com o COLLOQUIAL_MAP.
    3. Mantém 'né' e interjeições expressivas (ex: 'uai').
    """
    # 1. Limpa o texto usando a regra do Gabarito A
    cleaned = clean_text_gabarito_a(text)
    if not cleaned:
        return ""
        
    # 2. Mapeia termo a termo para evitar substituição parcial em palavras completas
    tokens = cleaned.split()
    normalized_tokens = []
    
    for token in tokens:
        # Se o token estiver no dicionário coloquial, substitui
        if token in COLLOQUIAL_MAP:
            normalized_tokens.append(COLLOQUIAL_MAP[token])
        else:
            normalized_tokens.append(token)
            
    # 3. Reconstrói o texto e normaliza espaços
    return " ".join(normalized_tokens)
