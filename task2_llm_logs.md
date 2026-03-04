
# Tarea 2 — Logs de comparación LLM vs RDF/SPARQL (+ Wikidata)

Objetivo: comparar respuestas obtenidas mediante **consultas SPARQL sobre el grafo RDF** con respuestas generadas por **Large Language Models (LLMs)**, identificando posibles **alucinaciones o inconsistencias**.

---

# Caso 1 — Conteo de animales en una granja (F001)

## Pregunta al LLM (sin datos)

¿Cuántos animales hay en la granja F001?

## Respuesta del LLM (sin datos)

“No tengo acceso a la base de datos específica de esa granja, pero normalmente una granja puede tener entre decenas y cientos de animales dependiendo de su tamaño.”

## Evidencia RDF/SPARQL

Consulta utilizada:

```sparql
SELECT ?farm ?farmName (COUNT(?animal) AS ?nAnimals)
WHERE {
  ?animal a ex:Animal ;
          ex:raisedInFarm ?farm .
  ?farm schema:name ?farmName .
}
GROUP BY ?farm ?farmName
```

Resultado esperado:

| farm | farmName | nAnimals |
|-----|-----|-----|
| farm/F001 | Granja San Vicente | 2 |
| farm/F002 | Granja Norte | 1 |

## Análisis

El LLM no puede responder correctamente porque **no tiene acceso al dataset**.  
La consulta SPARQL proporciona un resultado **exacto y verificable** basado en el grafo RDF.

---

# Caso 2 — Último peso del animal A001

## Pregunta al LLM (sin datos)

¿Cuál fue el último peso registrado del animal A001?

## Respuesta del LLM (sin datos)

“No dispongo de datos específicos sobre ese animal.”

## Evidencia RDF/SPARQL

Consulta utilizada:

```sparql
SELECT ?animal ?date ?weight
WHERE {
  {
    SELECT ?animal (MAX(?d) AS ?maxD)
    WHERE {
      ?wr a ex:WeightRecord ;
          ex:forAnimal ?animal ;
          ex:recordDate ?d .
    }
    GROUP BY ?animal
  }

  ?wr2 a ex:WeightRecord ;
       ex:forAnimal ?animal ;
       ex:recordDate ?date ;
       ex:weightKg ?weight .

  FILTER (?date = ?maxD)
}
```

Resultado esperado:

| animal | date | weight |
|------|------|------|
| animal/A001 | 2026-02-24 | 55.4 |

## Análisis

La consulta SPARQL identifica correctamente **el último registro de peso del animal A001**.  
Un LLM sin acceso al dataset **no puede inferir esta información**.

---

# Caso 3 — Ubicación de una granja

## Pregunta al LLM (sin datos)

¿En qué región está ubicada la granja F002?

## Respuesta del LLM (sin datos)

“No dispongo de información sobre la ubicación de esa granja específica.”

## Evidencia RDF/SPARQL

Consulta utilizada:

```sparql
SELECT ?regionName (COUNT(DISTINCT ?farm) AS ?nFarms)
WHERE {
  ?farm a ex:Farm ;
        ex:locatedInComuna ?comuna .
  ?comuna ex:inRegion ?region .
  ?region schema:name ?regionName .
}
GROUP BY ?regionName
```

Resultado esperado:

| regionName | nFarms |
|-----------|-------|
| Región Metropolitana | 1 |
| Región de Valparaíso | 1 |

## Análisis

El grafo RDF permite relacionar:

Farm → Comuna → Región

Esto demuestra cómo **los datos abiertos (comunas/regiones)** pueden integrarse con **datos privados (granjas)** mediante un **grafo de conocimiento**.

---

# Comparación con Wikidata

Se realizaron consultas en el endpoint SPARQL de **Wikidata** para obtener información general sobre las especies utilizadas.

Ejemplo:

| entidad | descripción |
|-------|-------|
| pig | especie de mamífero doméstico |
| chicken | ave doméstica |

Wikidata proporciona **conocimiento general y taxonómico**, mientras que el grafo RDF construido en esta tarea contiene **datos operacionales específicos del sistema productivo**.

---

# Conclusiones

El uso de grafos RDF y consultas SPARQL permite:

- representar relaciones complejas entre entidades
- integrar **datos privados y datos abiertos**
- realizar consultas analíticas reproducibles
- validar información mediante esquemas como **ShEx**

Los LLMs son útiles para **interpretar o explicar información**, pero no reemplazan a los **sistemas basados en grafos de conocimiento** cuando se requiere precisión y trazabilidad.

---

# Resultado

La comparación muestra:

- **RDF + SPARQL → precisión y trazabilidad**
- **Wikidata → conocimiento general**
- **LLMs → interpretación en lenguaje natural**

La combinación de estas tecnologías permite construir **sistemas inteligentes basados en conocimiento estructurado**.
