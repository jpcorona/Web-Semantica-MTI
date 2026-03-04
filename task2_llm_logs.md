# Tarea 2 — Logs de comparación LLM vs RDF/SPARQL (+ Wikidata)

> Objetivo: comparar respuestas obtenidas con RDF/SPARQL (evidencia estructurada) vs respuestas de LLMs, identificando alucinaciones o inconsistencias.

---

## Instrucciones de uso
1. Haz la pregunta al LLM **sin entregarle el dataset** (sin pegar tu RDF ni resultados SPARQL).
2. Copia la respuesta del LLM aquí.
3. Ejecuta la query SPARQL correspondiente y pega el resultado (tabla/captura o texto).
4. Describe la discrepancia (si el LLM inventó datos o respondió con excesiva seguridad).

---

## Caso 1 — Conteo de animales en una granja (F001)

### Pregunta al LLM (sin datos)
¿CUÁNTOS ANIMALES HAY EN LA GRANJA F001?

### Respuesta del LLM (sin datos)
(pegue aquí)

### Evidencia RDF/SPARQL
- Query usada: Q1 (Animales por granja)
- Resultado (pegue tabla o captura)

### Discrepancia / análisis
- (ej: el LLM inventó un número / se negó correctamente / pidió datos)

---

## Caso 2 — Último peso del animal A001

### Pregunta al LLM (sin datos)
¿CUÁL FUE EL ÚLTIMO PESO DEL ANIMAL A001 Y EN QUÉ FECHA?

### Respuesta del LLM (sin datos)
(pegue aquí)

### Evidencia RDF/SPARQL
- Query usada: Q4 (Peso más reciente por animal)
- Resultado (pegue tabla o captura)

### Discrepancia / análisis
- (ej: inventó fecha/peso / confundió formato / etc.)

---

## Caso 3 — Región de una granja (F002)

### Pregunta al LLM (sin datos)
¿EN QUÉ REGIÓN ESTÁ LA GRANJA F002?

### Respuesta del LLM (sin datos)
(pegue aquí)

### Evidencia RDF/SPARQL
- Query usada: Q7 (Granjas por región) o una query específica por granja
- Resultado (pegue tabla o captura)

### Discrepancia / análisis
- (ej: el LLM asumió una región sin base)

---

## Comparación breve con Wikidata (conocimiento general)
Describe aquí 2–3 hallazgos al comparar con Wikidata, por ejemplo:
- Definición/taxonomía de “pig” y “chicken”
- Diferencias entre conocimiento general (Wikidata) vs datos operacionales (tu KG)

---

## Conclusiones
- ¿Qué tipo de preguntas responde mejor RDF/SPARQL en tu dominio?
- ¿Qué tipo de preguntas responde mejor el LLM?
- ¿Dónde se observaron alucinaciones o inconsistencias?
