# SOAP Format — Reference

## Definition

**SOAP** is a structured clinical documentation method used in medical records.

| Section | Name | Description |
|---|---|---|
| **S** | Subjective | Patient's reported symptoms, complaints, and history (in their own words) |
| **O** | Objective | Measurable clinical findings: vital signs, physical exam, lab results |
| **A** | Assessment | Clinician's diagnosis or differential diagnosis |
| **P** | Plan | Treatment plan, prescriptions, referrals, follow-up |

## Expected Output Format

```json
{
  "subjective": "Patient reports persistent cough for 3 weeks, accompanied by low-grade fever and fatigue.",
  "objective": "Temperature: 37.8°C. SpO2: 97%. Lung auscultation: decreased breath sounds in right base.",
  "assessment": "Possible community-acquired pneumonia. Rule out tuberculosis given endemic context.",
  "plan": "Chest X-ray ordered. Amoxicillin 500mg TID for 7 days. Return in 5 days or sooner if worsening."
}
```
