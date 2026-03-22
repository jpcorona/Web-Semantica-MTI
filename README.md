# Web Semántica y Datos Abiertos — MTI Chile 2026

[![Open Tarea 1 In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jpcorona/Web-Semantica-MTI/blob/main/notebook/Tarea1_Produccion_Animal_RDF_ShEx.ipynb)
[![Open Tarea 2 In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jpcorona/Web-Semantica-MTI/blob/main/notebook/Tarea2_SPARQL_Wikidata_LLM.ipynb)

**Magíster en Tecnologías de la Información**  
**Curso:** Web Semántica y Datos Abiertos — Enero 2026

---

## Dominio seleccionado

**Producción Animal en Chile.** Se modeló un sistema de gestión de granjas con animales (cerdos y pollos), registros de peso y ubicación geográfica, integrando datos privados simulados con datos abiertos de la división político-administrativa de Chile (codificación CUT del INE).

Entidades principales del modelo:

- **Farm** — Granjas de producción (porcina o avícola)
- **Animal** — Animales individuales con especie, raza, sexo y fecha de nacimiento
- **WeightRecord** — Registros de pesaje con fecha y peso en kg
- **Comuna** — Comunas de Chile (dato abierto, codificación CUT)
- **Region** — Regiones de Chile (dato abierto)

Relaciones: `Animal → raisedInFarm → Farm → locatedInComuna → Comuna → inRegion → Region`

---

## Estructura del repositorio

```
.
├── README.md
├── data/
│   ├── farms_private.csv          # 7 granjas (dato privado simulado)
│   ├── animals_private.csv        # 15 animales (dato privado simulado)
│   ├── weights_private.csv        # 36 registros de peso (dato privado simulado)
│   └── comunas_open.csv           # 31 comunas de Chile (dato abierto, fuente: INE/CUT)
├── rdf/
│   ├── private.ttl                # Grafo RDF de datos privados
│   ├── open.ttl                   # Grafo RDF de datos abiertos
│   └── merged.ttl                 # Grafo fusionado (410 triples)
├── validation/
│   ├── schema.shex                # Esquema Shape Expressions
│   ├── schema.shacl.ttl           # Esquema SHACL (opcional)
│   └── invalid_examples.ttl       # Datos erróneos para validación
├── notebook/
│   ├── Tarea1_Produccion_Animal_RDF_ShEx.ipynb   # Transformación + validación
│   └── Tarea2_SPARQL_Wikidata_LLM.ipynb          # Consultas + comparación LLM
├── task2_llm_logs.md              # Logs de conversaciones con LLMs
├── task3_knowledge_graphs_llms.md # Análisis KG + LLMs
└── task4_open_data_privacy_solid.md # Análisis datos abiertos + privacidad + Solid
```

---

## Tarea 1 — Grafos RDF y validación ShEx/SHACL

**Notebook:** `notebook/Tarea1_Produccion_Animal_RDF_ShEx.ipynb`

### Fuentes de datos

- **Datos privados (no públicos):** Información simulada de 7 granjas, 15 animales y 36 registros de peso de un sistema de producción animal. No corresponden a datos reales de ninguna empresa.
- **Datos abiertos:** 31 comunas de Chile con sus regiones, basados en la codificación oficial CUT (Código Único Territorial) del Instituto Nacional de Estadísticas. Fuente original: [datos.gob.cl](http://datos.gob.cl/).

### Proceso de transformación

1. Lectura de archivos CSV con `pandas`.
2. Generación de URIs bajo el namespace `https://kg.example.cl/animal/`.
3. Creación de triples RDF usando `rdflib`.
4. Exportación en formato Turtle (`.ttl`).
5. Fusión de grafos privado y abierto en `merged.ttl`.

### Validación

- **ShEx:** Se definieron shapes para Farm, Animal, WeightRecord, Comuna y Region en `schema.shex`. Se validan múltiples entidades correctas y se demuestra la detección de errores con `invalid_examples.ttl`.
- **SHACL (opcional):** Se definió un modelo equivalente en `schema.shacl.ttl` con restricciones de cardinalidad, tipo de dato y valores permitidos. Se ejecuta validación con `pyshacl`.

### Ejecución

```bash
pip install rdflib pyshex pyshacl pandas
```

Ejecutar el notebook en Google Colab o localmente (cambiar `USE_COLAB = False`).

---

## Tarea 2 — Consultas SPARQL y comparación con LLMs

**Notebook:** `notebook/Tarea2_SPARQL_Wikidata_LLM.ipynb`  
**Logs LLM:** `task2_llm_logs.md`

### Consultas SPARQL implementadas

| ID | Consulta | Interés |
|----|----------|---------|
| Q1 | Animales por granja y tipo | Agregación + propiedades de granja |
| Q2 | Registros de peso por especie y raza | Análisis de seguimiento por línea genética |
| Q3 | Ganancia de peso por animal | Subconsultas anidadas con MIN/MAX |
| Q4 | Peso promedio actual por especie | AVG sobre último registro por animal |
| Q5 | Granjas por región y comuna | Integración datos privados + abiertos |
| Q6 | Animales nacidos después de agosto 2025 | Filtro temporal + traversal completo del grafo |
| Q7 | Top 5 animales por ganancia de peso | Ranking con LIMIT y HAVING |

### Consultas a Wikidata

- WD1: Taxonomía de cerdo y pollo
- WD2: Razas de cerdo registradas
- WD3: Razas de pollo registradas
- WD4: Regiones de Chile (consulta federada)
- WD5: Masa del cerdo doméstico

### Comparación con LLMs

Se compararon respuestas de **ChatGPT-4o** y **Claude 3.5 Sonnet** en 5 escenarios:

1. **Datos privados** — El LLM no puede saber → ChatGPT alucinó con rangos inventados.
2. **Peso específico** — Ambos LLMs estimaron incorrectamente basándose en promedios industriales.
3. **Conocimiento de razas** — Respuestas plausibles pero sin trazabilidad.
4. **Pregunta engañosa** — Ambos respondieron correctamente (Cobb 500 es pollo, no cerdo).
5. **Distribución geográfica** — Inconsistencias parciales respecto a los datos reales del sistema.

**Hallazgo principal:** Los LLMs tienden a generar respuestas plausibles sin datos reales, lo que constituye un riesgo en contextos operacionales.

### Ejecución

```bash
pip install rdflib SPARQLWrapper pandas
```

---

## Tarea 3 — Knowledge Graphs y LLMs

**Documento:** `task3_knowledge_graphs_llms.md`

Análisis de ~2 páginas que cubre:

- Beneficios de la integración KG + LLM (grounding, trazabilidad, integración de datos)
- Retos (escalabilidad, mantenimiento, alineación semántica)
- Casos de uso concretos: GraphRAG (Microsoft), Google Knowledge Graph + Gemini, Amazon Product KG, Wikidata + KBQA
- Referencia a la presentación de Ora Lassila (2024)
- Aplicación al dominio de producción animal: asistente de consulta, alertas inteligentes, trazabilidad normativa
- 6 referencias bibliográficas

---

## Tarea 4 — Datos abiertos, privacidad y Solid

**Documento:** `task4_open_data_privacy_solid.md`

Análisis de ~3 páginas que cubre:

- Convivencia datos abiertos y privacidad (anonimización, clasificación, licenciamiento)
- Riesgos de la combinación de datasets (re-identificación, inferencia competitiva, riesgo en cadena)
- Ejemplos concretos en producción animal: trazabilidad SAG, datos ambientales RETC, datos de empleo INE
- Proyecto Solid: principios, arquitectura de PODs, Web Access Control
- Cómo Solid aborda los riesgos identificados
- Limitaciones de Solid en el contexto actual
- Aplicación al dominio trabajado
- 7 referencias bibliográficas

---

## Requisitos

```bash
pip install rdflib pyshex pyshacl SPARQLWrapper pandas
```

Python 3.9+ recomendado. Los notebooks están diseñados para ejecutarse en **Google Colab** (variable `USE_COLAB = True`) o localmente.

---

## Autores

Magíster en Tecnologías de la Información — Universidad Técnica Federico Santa Maria, 2026.
