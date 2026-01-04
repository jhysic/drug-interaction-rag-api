# drug-interaction-rag-api 
research on drug interactions 💊

Study of how drug–drug interactions and individual genetic profiles jointly influence drug metabolism,
with a focus on pharmacokinetic pathways, variability in enzyme activity,
and resulting differences in efficacy and adverse effect risk across patients.

## Flow chart 
![generated-image](https://github.com/user-attachments/assets/fd3ecf19-a82b-450d-88d4-57fdc6e9b70a)

## Pseudo Code
```
ALGORITHM AnalyzeDrugInteractionsWithGenetics
    INPUT:
        med_list              // list of all medications the patient is taking
        genotype_data         // patient genetic variant data (e.g., star alleles, diplotypes)

    OUTPUT:
        interaction_report    // structured summary of DDIs
        medication_recommendations

    BEGIN
        // 1. Input cleaning and validation
        CLEAN med_list
        VALIDATE genotype_data

        // 2. Generate all drug pairs
        pair_list ← ALL_UNORDERED_PAIRS(med_list)      // size = nC2

        interaction_report ← EMPTY_LIST

        // 3. Query base drug–drug interaction (DDI) information
        FOR EACH pair IN pair_list DO
            d1 ← pair.drug1
            d2 ← pair.drug2

            base_ddi_info ← QUERY_DDI_DATABASES(d1, d2)
            // uses curated drug–drug interaction resources

            // 4. Check for relevant genetic variants
            IF HAS_RELEVANT_VARIANTS(genotype_data, d1, d2) THEN
                pgx_data ← QUERY_PHARMVAR_AND_PGx_GUIDELINES(genotype_data, d1, d2)
                adjusted_risk ← ADJUST_RISK_WITH_GENETICS(base_ddi_info, pgx_data)
                recommendation ← GENERATE_RECOMMENDATION(adjusted_risk, med_list)
            ELSE
                adjusted_risk ← base_ddi_info.risk_level
                recommendation ← GENERATE_RECOMMENDATION(adjusted_risk, med_list)
            END IF

            APPEND(
                interaction_report,
                BUILD_PAIR_ENTRY(d1, d2, base_ddi_info, adjusted_risk, recommendation)
            )
        END FOR

        // 5. Summarize global recommendations across all pairs
        medication_recommendations ← SUMMARIZE_GLOBAL_RECOMMENDATIONS(interaction_report)

        RETURN interaction_report, medication_recommendations
    END
```

## 🧰 Tech Stack

### Core Architecture
- **Pattern:** Retrieval-Augmented Generation (RAG)
- **Goal:** Analyze drug–drug interactions and pharmacogenomic effects
  based on patient medication lists and genetic variant data.

### Model & Inference

- **LLM (Generation)**
  - **Model:** BioMistral 7B (medical-domain LLM)
  - **Variant:** Quantized (e.g., 4-bit) for CPU-only inference
  - **Rationale:** Optimized for biomedical text; small enough to run on a
    CPU-only laptop while still providing clinically relevant reasoning.

- **Embedding Model (Retrieval)**
  - **Model:** Lightweight, open-source sentence embedding model
    (e.g., `BAAI/bge-small-en` or similar)
  - **Use:** Create vector embeddings for:
    - Drug information documents (mechanism, PK, DDIs, etc.)
    - Pharmacogenomic / genetic reference documents
  - **Rationale:** Smaller footprint and faster CPU inference while
    maintaining good retrieval quality for RAG.

### Vector Store

- **Vector Database:** ChromaDB
  - **Deployment:** Local, file-based
  - **Use Cases:**
    - Store embeddings for drug documents
    - Store embeddings for genetic / pharmacogenomic documents
    - Perform k‑NN similarity search during RAG
  - **Rationale:** Simple to integrate with Python, no external server
    required, ideal for a personal research project.

### API Layer

- **Framework:** FastAPI (Python)
  - **Endpoints:**
    - `POST /analyze` — accept medications + genotype + question,
      run RAG pipeline, return interaction summary and recommendations.
  - **Role:** Orchestrate:
    1. Input validation & normalization
    2. Retrieval from Chroma
    3. Prompt construction
    4. LLM (BioMistral 7B) call and response formatting

### Runtime Environment

- **Hardware:** CPU-only laptop (no CUDA / GPU)
- **OS / Host:** Local development environment
- **Optimization:**
  - Quantized LLM weights
  - Lightweight embedding model
  - Limited context size and efficient chunking to keep latency acceptable.

