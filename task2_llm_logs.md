# Tarea 2 — Logs de comparación LLM vs RDF/SPARQL y Wikidata

**Objetivo:** Comparar respuestas obtenidas mediante consultas SPARQL sobre el grafo RDF con respuestas generadas por Large Language Models (ChatGPT-4o y Claude 3.5 Sonnet), identificando alucinaciones e inconsistencias.

**Fecha de las pruebas:** Febrero 2026

---

## Caso 1 — Conteo de animales en una granja (datos privados)

### Pregunta formulada al LLM (sin darle contexto ni datos)

> "En un sistema de producción animal en Chile, la Granja San Vicente (código F001) está ubicada en la comuna de Melipilla. ¿Cuántos animales tiene actualmente?"

### Respuesta de ChatGPT-4o

> "Las granjas porcinas en la zona central de Chile suelen manejar entre 500 y 2.000 cerdos en producción. Si es una granja mediana en Melipilla, es probable que tenga alrededor de 800-1.200 animales en distintas etapas de crecimiento."

### Respuesta de Claude 3.5 Sonnet

> "No tengo acceso a información operacional específica de esa granja. Para obtener datos reales sobre el número de animales, necesitarías consultar el sistema interno de gestión de la granja o los registros del SAG."

### Evidencia RDF/SPARQL

```sparql
SELECT ?farmName (COUNT(?animal) AS ?nAnimals)
WHERE {
  ?animal a ex:Animal ; ex:raisedInFarm ex:farm/F001 .
  ex:farm/F001 schema:name ?farmName .
}
GROUP BY ?farmName
```

**Resultado:** Granja San Vicente → 3 animales (A001, A002, A003).

### Análisis

**Alucinación detectada en ChatGPT:** Fabricó un rango numérico (800-1.200) sin ninguna base, extrapolando desde promedios de la industria. Este es un caso clásico de alucinación donde el modelo genera datos específicos plausibles pero completamente inventados. Claude, en cambio, reconoció correctamente su limitación.

---

## Caso 2 — Peso de un animal específico (datos privados)

### Pregunta formulada al LLM

> "El animal A001 es un cerdo raza Landrace nacido el 10 de marzo de 2025 en una granja en Melipilla. ¿Cuál fue su peso más reciente registrado y en qué fecha?"

### Respuesta de ChatGPT-4o

> "Un cerdo Landrace de aproximadamente 10 meses de edad típicamente pesa entre 90 y 110 kg. Si nació en marzo de 2025, para enero de 2026 debería estar cerca de los 100 kg, considerando una ganancia diaria de peso de unos 700-800 gramos."

### Respuesta de Claude 3.5 Sonnet

> "No puedo acceder a registros específicos de ese animal. Sin embargo, un Landrace de esa edad bajo manejo intensivo en Chile podría pesar entre 85-115 kg. Recomiendo verificar en el sistema de trazabilidad de la granja."

### Evidencia RDF/SPARQL

```sparql
SELECT ?date ?weight
WHERE {
  ?wr a ex:WeightRecord ;
      ex:forAnimal ex:animal/A001 ;
      ex:recordDate ?date ;
      ex:weightKg ?weight .
}
ORDER BY DESC(?date)
LIMIT 1
```

**Resultado:** Fecha: 2025-07-10, Peso: 72.1 kg.

### Análisis

**Alucinación en ambos LLMs:** Ambos estimaron pesos basados en promedios de la industria, pero ninguno puede saber el peso real. ChatGPT fue más específico y dio un número concreto (100 kg) que resulta incorrecto: el último registro real es 72.1 kg al 10/07/2025, no en enero 2026. Claude fue más cauteloso con un rango, pero también es incorrecto. Solo la consulta SPARQL proporciona el dato exacto y trazable.

---

## Caso 3 — Peso promedio de pollos Ross 308 (conocimiento general vs. datos)

### Pregunta formulada al LLM

> "¿Cuál es el peso promedio de un pollo Ross 308 a las 6 semanas de edad?"

### Respuesta de ChatGPT-4o

> "Un pollo Ross 308 a las 6 semanas (42 días) de edad alcanza un peso promedio de 2.8-3.0 kg según las tablas de rendimiento de Aviagen 2024. Es una de las líneas genéticas más eficientes para producción broiler."

### Respuesta de Claude 3.5 Sonnet

> "El Ross 308 es un pollo broiler desarrollado por Aviagen. A los 42 días, el peso objetivo según las guías del fabricante es de aproximadamente 2.7-2.9 kg para machos y 2.4-2.6 kg para hembras, dependiendo de las condiciones de manejo y alimentación."

### Evidencia RDF/SPARQL (nuestro grafo)

```sparql
SELECT ?animal ?date ?weight
WHERE {
  ?animal a ex:Animal ; ex:breed "Ross 308" ; ex:species "chicken" .
  ?wr a ex:WeightRecord ; ex:forAnimal ?animal ;
      ex:recordDate ?date ; ex:weightKg ?weight .
}
ORDER BY ?animal ?date
```

**Resultado:** Los pollos Ross 308 en nuestro grafo (A004, A005, A009, A010, A013) muestran pesos de 1.78-2.91 kg a las 8-13 semanas, valores que están dentro del rango esperado pero son específicos de nuestro sistema.

### Evidencia Wikidata

Wikidata no tiene datos de peso específicos por raza de pollo broiler. La entidad Q15623649 (chicken breed) no incluye propiedades de rendimiento productivo.

### Análisis

Ambos LLMs dieron respuestas plausibles y generalmente correctas sobre conocimiento público de la raza. Sin embargo, no pueden distinguir entre el rendimiento teórico y el rendimiento real en nuestras granjas. El grafo RDF proporciona datos operacionales reales, mientras que los LLMs solo pueden ofrecer datos de referencia genéricos.

---

## Caso 4 — Pregunta engañosa: raza incorrecta para una especie

### Pregunta formulada al LLM

> "¿La raza Cobb 500 es una buena raza de cerdo para producción en Chile?"

### Respuesta de ChatGPT-4o

> "No, la Cobb 500 no es una raza de cerdo. Es una línea genética de pollo broiler desarrollada por Cobb-Vantress. Para producción porcina en Chile, las razas más utilizadas son Landrace, Large White y Duroc."

### Respuesta de Claude 3.5 Sonnet

> "La Cobb 500 no es una raza porcina, sino una línea de pollo de engorde (broiler) producida por Cobb-Vantress, una subsidiaria de Tyson Foods. Para cerdos en Chile, las razas más comunes son Landrace, Large White, Duroc y sus cruces."

### Evidencia RDF/SPARQL

```sparql
SELECT ?animal ?species ?breed
WHERE {
  ?animal a ex:Animal ; ex:species ?species ; ex:breed "Cobb 500" .
}
```

**Resultado:** Cobb 500 aparece asociada únicamente a especie "chicken" (animales A006, A010).

### Análisis

En este caso, ambos LLMs respondieron correctamente. La pregunta era engañosa pero el conocimiento sobre razas animales comerciales está bien representado en los datos de entrenamiento de los modelos. Sin embargo, el grafo RDF permite verificar formalmente esta asociación especie-raza.

---

## Caso 5 — Distribución geográfica (integración datos abiertos)

### Pregunta formulada al LLM

> "¿En qué regiones de Chile hay granjas de producción porcina según los datos del sistema?"

### Respuesta de ChatGPT-4o

> "Las principales regiones de producción porcina en Chile son la Región de O'Higgins, la Región del Maule y la Región Metropolitana, donde se concentra más del 80% de la producción nacional. Empresas como Agrosuper y Maxagro tienen sus principales operaciones en estas zonas."

### Respuesta de Claude 3.5 Sonnet

> "No tengo acceso a datos de un sistema específico, pero las principales zonas de producción porcina en Chile históricamente se concentran en la zona central: Región Metropolitana, O'Higgins, Maule y Biobío."

### Evidencia RDF/SPARQL

```sparql
SELECT ?regionName (COUNT(DISTINCT ?farm) AS ?nFarms)
WHERE {
  ?farm a ex:Farm ; ex:farmType "porcina" ;
        ex:locatedInComuna ?comuna .
  ?comuna ex:inRegion ?region .
  ?region schema:name ?regionName .
}
GROUP BY ?regionName
```

**Resultado:**
- Región Metropolitana de Santiago: 1 granja
- Región del Libertador General Bernardo O'Higgins: 1 granja
- Región del Biobío: 1 granja
- Región de Los Lagos: 1 granja

### Análisis

**Inconsistencia parcial en ChatGPT:** Mencionó O'Higgins y RM correctamente, pero agregó Maule (que en nuestro sistema tiene solo granjas avícolas, no porcinas) y omitió Biobío y Los Lagos. Claude mencionó Biobío pero también incluyó Maule. Ambos LLMs respondieron con conocimiento general de la industria, no con los datos específicos de nuestro sistema. Solo la consulta SPARQL refleja la distribución real en nuestro grafo.

---

## Conclusiones

| Aspecto | RDF + SPARQL | Wikidata | LLMs |
|---------|-------------|----------|------|
| Datos privados/operacionales | ✅ Exacto y verificable | ❌ No disponibles | ❌ Inventan o estiman |
| Datos públicos estables | ✅ Si están en el grafo | ✅ Confiable | ✅ Generalmente correcto |
| Trazabilidad de respuestas | ✅ Total (triple → fuente) | ✅ Total (entidad → statement) | ❌ Ninguna |
| Conocimiento general | Limitado al grafo | ✅ Amplio | ✅ Amplio pero sin fuente |
| Riesgo de alucinación | Ninguno | Ninguno | Alto para datos específicos |
| Detección de errores | ✅ Formal (ShEx/SHACL) | ✅ Constraints | ❌ No aplica |

**Hallazgo principal:** Los LLMs tienden a generar respuestas plausibles incluso cuando no tienen datos reales, lo que constituye un riesgo significativo en contextos operacionales donde la precisión es crítica. Los grafos de conocimiento con consultas SPARQL garantizan trazabilidad y exactitud.
