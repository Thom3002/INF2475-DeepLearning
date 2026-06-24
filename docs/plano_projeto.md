# Plano de Projeto: Transcrição de Áudio (STT) e Estruturação SOAP para Telemedicina

Este plano estabelece as fases para avaliar e implementar um pipeline de transcrição clínica em português (STT) de baixo custo e sua posterior estruturação no formato SOAP em formato JSON.

---

## ETAPA 1: Transcrição de Áudio (STT) e Benchmarking (Foco Atual)

Esta etapa foca em encontrar a melhor relação custo-benefício de modelos de ASR (Automatic Speech Recognition) em português rodando em servidores leves.

### 1.1. Revisão Literária e Seleção de Modelos Leves
Identificação e justificativa na literatura de modelos de ASR compactos que caibam em infraestruturas enxutas (CPU ou GPUs básicas como T4):
- **Modelos CTC**: Meta MMS-1B ou Wav2Vec2 (`xlsr-53-portuguese`). Rápido consumo de CPU e sem risco de alucinação.
- **Modelos Encoder-Decoder**: Whisper (Base e Small) via `faster-whisper` (`int8`). Transcrição com pontuação nativa otimizada pelo CTranslate2.

### 1.2. Preparação e Segmentação dos Áudios e Gabaritos (C-ORAL-ESQ)
Para estruturar o ambiente de testes, faremos a preparação dos dados tanto a nível de áudio quanto de texto:

#### A. Pré-processamento e Segmentação de Áudio
1. **Ajuste Técnico (Resampling)**: Os áudios originais do C-ORAL-ESQ serão convertidos para a taxa de amostragem padrão de **16 kHz, mono, formato WAV**, exigida pelos modelos Whisper e Wav2Vec2.
2. **Simulação de Separação de Locutor (Diarização)**: Na prática de telemedicina, assume-se que a gravação do áudio será feita em canais separados (médico e paciente). Para simular esse cenário ideal a partir dos áudios de canal único (mono) do C-ORAL-ESQ, utilizaremos as marcações de tempo (*timestamps*) originais das transcrições para recortar o áudio principal em **pequenos segmentos correspondentes a turnos de fala individuais**.

#### B. Pós-processamento e Geração do Texto de Gabarito (Gabaritos A e B)
Cada segmento de áudio recortado será pareado com sua respectiva linha de transcrição textual limpa. Criaremos duas versões de texto de gabarito para avaliar o comportamento de modelos fonéticos (CTC) vs. semânticos (Whisper):
- **Gabarito A (Coloquial Mantido)**: Remoção de marcações CHAT (pausas `/` e `//`, overlaps `< >`, disfluências `[/N]` e stutters), mas **preservando o vocabulário e variações fonéticas coloquiais** originais (ex: `nũ`, `cê`, `tamo`, `sior`).
- **Gabarito B (Normalizado)**: Remoção das tags CHAT e **mapeamento sistemático de todos os termos coloquiais para a norma escrita padrão** do português (ex: `nũ` -> `não`, `cê` -> `você`, `tamo` -> `estamos`, `tava` -> `estava`, `sior` -> `senhor`, `ea` -> `ela`, `e'` -> `ele`, `es` -> `eles`).

### 1.3. Inferência e Avaliação Base (WER)
Nesta fase, faremos a inferência dos áudios do dataset C-ORAL-ESQ usando as arquiteturas instanciadas e avaliaremos a acurácia dos modelos por meio da métrica **WER (Word Error Rate)**.

#### O que é o WER?
O WER é a métrica padrão na literatura para avaliar a precisão de sistemas de transcrição automática de fala. Ele calcula o percentual de palavras incorretas em relação ao total de palavras do gabarito (referência), baseando-se na distância de edição (Levenshtein distance) a nível de palavra:

$$WER = \frac{S + D + I}{N}$$

Onde:
- **$S$ (Substitutions)**: Palavras substituídas incorretamente (ex: ouvir "glicose" e transcrever "glicosez").
- **$D$ (Deletions)**: Palavras omitidas na transcrição (palavras faladas que o modelo pulou).
- **$I$ (Insertions)**: Palavras inseridas extra na transcrição (palavras que o modelo alucinou).
- **$N$**: Quantidade total de palavras no texto de referência (gabarito).

#### Como vamos fazer o cálculo?
1. **Pré-processamento das Transcrições**: Antes do cálculo da métrica, tanto o texto gerado pelo modelo (hipótese) quanto o gabarito (referência) passarão por um pré-processamento de padronização textual:
   - Conversão de todas as letras para minúsculo.
   - Remoção de pontuação básica (pontos, vírgulas, exclamações, interrogações).
   - Remoção de espaços duplos ou em branco no início/fim das frases.
2. **Computação da Métrica**: Usaremos a biblioteca padrão de avaliação de ASR em Python (como `jiwer`) ou uma implementação robusta baseada em programação dinâmica para alinhar os textos e contar $S$, $D$ e $I$.
3. **Avaliação em Duas Frentes**: Para cada áudio inferido, calcularemos dois valores de WER:
   - **WER Coloquial**: Comparação da transcrição com o **Gabarito A**. Ajuda a medir a fidelidade do modelo ao áudio cru e à linguagem natural do paciente.
   - **WER Normalizado**: Comparação da transcrição com o **Gabarito B**. Mede a acurácia do modelo em transcrever na grafia culta formal, que é o formato ideal esperado para a posterior extração de entidades médicas e SOAP.
4. **Agregação dos Resultados**: Os resultados serão agregados por modelo, calculando-se a média aritmética e o desvio padrão do WER ao longo de todos os arquivos de áudio avaliados no dataset de teste.

### 1.4. Benchmark de Custo-Benefício de Hardware
Documentação dos recursos computacionais (memória RAM/VRAM máxima, tempo de processamento por áudio) e acurácia (WER) de cada modelo para propor a melhor escolha custo-benefício local.

---

## TRABALHOS FUTUROS DA ETAPA 1

Se o cronograma permitir, a Etapa 1 será estendida com:
- **BERTScore**: Avaliação de similaridade semântica para verificar se erros de transcrição distorcem o sentido clínico.
- **Métricas Clínicas de Entidades Médicas (Afonja et al., 2026)**: Extração de entidades (medicamentos, dosagens, diagnósticos) e alinhamento com predições ASR para calcular **Medical Named Entity Recall**, **Medical WER** e **Medical CER**, mitigando riscos de segurança do paciente.

---

## ETAPA 2: Estruturação SOAP (Trabalhos Futuros)

Fase de estruturação das consultas em prontuários clínicos formais.

### 2.1. Modelagem com LLMs Clínicos
Utilização de LLMs leves locais (ex: Llama-3-8B-Instruct) ou APIs econômicas (ex: Gemini 1.5 Flash) alimentados com os diálogos transcritos.

### 2.2. Mapeamento SOAP em JSON
Estruturação da saída da consulta no seguinte formato JSON estrito:
```json
{
  "subjective": "Histórico, queixas principais e sintomas relatados pelo paciente.",
  "objective": "Achados clínicos, sinais vitais e exames mencionados.",
  "assessment": "Impressão diagnóstica ou diagnósticos diferenciais do médico.",
  "plan": "Condutas prescritas, receitas, exames pedidos e retorno."
}
```

### 2.3. Avaliação de Robustez SOAP
Simulação de impacto de erros do ASR no prontuário, comparando o SOAP JSON gerado da transcrição ASR com o gerado do gabarito limpo (usando BERTScore por seção do JSON e checagem de dosagens/medicamentos).
