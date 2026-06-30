# ConsultaAI: Audio Transcription (STT) and SOAP Structuring for Telemedicine

An academic project developed as part of the **INF2475 - Introduction to Deep Learning** course at **PUC-Rio** (Semester 2026.1).

## Overview
This project aims to evaluate and implement a low-cost clinical transcription and structuring pipeline for telemedicine in Portuguese. The core goal is to transcribe medical dialogues using cost-effective, lightweight Automatic Speech Recognition (ASR) models and subsequently extract clinical insights structured into the standard SOAP (Subjective, Objective, Assessment, Plan) format.

---

## Project Structure & Stages

### Stage 1: Audio Transcription (STT) & Benchmarking (Current Focus)
The primary objective of the current phase is to benchmark lightweight ASR architectures on Portuguese medical/conversational audio to identify the best trade-off between hardware requirements (CPU/GPU) and transcription accuracy.

1. **Model Selection**: Evaluating lightweight architectures including Connectionist Temporal Classification (CTC) models (like Meta MMS-1B and Wav2Vec2) and Encoder-Decoder models (like Whisper Base/Small optimized via CTranslate2).
2. **Dataset & Preprocessing**:
   - Using the **C-ORAL-ESQ** dataset.
   - Standardizing audio files to 16 kHz mono WAV format.
   - Simulating speaker diarization by segmenting audio tracks into individual conversational turns based on timestamp annotations.
3. **Ground Truth Variations**:
   - **Colloquial (Ground Truth A)**: Keeps conversational variations and colloquial terms but removes annotations.
   - **Normalized (Ground Truth B)**: Standardizes colloquial speech into formal Portuguese (e.g., mapping conversational contractions/slang to standard grammatical words).
4. **Evaluation**:
   - Utilizing **Word Error Rate (WER)** to evaluate how accurately models capture natural, colloquial speech vs. formal, normalized speech.
   - Benchmarking hardware footprint (execution time, peak RAM/VRAM usage) to identify efficient local deployment options.

#### Future Enhancements (Stage 1 Extension)
- **Semantic Evaluation (BERTScore)**: Ensuring transcription differences do not alter clinical meaning.
- **Medical Named Entity Metrics**: Tracking accuracy on critical terms like medication names, dosages, and diagnoses to safeguard patient safety.

---

### Stage 2: SOAP Structuring (Future Phase)
Once transcription is reliable, the project will focus on extracting medical structured data from the resulting texts.

1. **Clinical LLM Processing**: Feeding dialogue transcripts into lightweight local LLMs or cost-effective cloud APIs (such as Gemini 1.5 Flash).
2. **SOAP JSON Output**: Structuring output strictly into a standardized medical SOAP format containing:
   - **Subjective**: Patient symptoms, medical history, and complaints.
   - **Objective**: Vital signs, clinical observations, and physical exam details.
   - **Assessment**: Diagnostic impressions and clinical reasoning.
   - **Plan**: Prescribed treatments, prescriptions, exams, and follow-up instructions.
3. **Robustness Evaluation**: Testing how downstream SOAP generation holds up when transcriptions contain ASR errors compared to using the gold-standard ground truth.
