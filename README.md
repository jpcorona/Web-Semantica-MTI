
# Web Semántica – Tarea 1
## Knowledge Graph de Producción Animal
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jpcorona/Web-Semantica-MTI/blob/main/notebook/Tarea1_Produccion_Animal_RDF_ShEx.ipynb)

Magíster en Tecnologías de la Información  
Curso: Web Semántica y Datos Abiertos

---

# 1. Objetivo

El objetivo de esta tarea es construir un **grafo RDF a partir de datos privados y datos abiertos**, definir un **modelo de validación mediante Shape Expressions (ShEx)** y validar los datos generados.

El ejercicio demuestra cómo la **Web Semántica** permite integrar datasets heterogéneos mediante grafos de conocimiento.

---

# 2. Dominio seleccionado

Se eligió el dominio **Producción Animal**, modelando información básica de:

- Granjas (Farm)
- Animales (Animal)
- Registros de peso (WeightRecord)
- Ubicación geográfica (Comuna / Región)

Este dominio permite representar información típica de sistemas agroindustriales.

---

# 3. Fuentes de datos

## 3.1 Datos privados

Se utilizaron datasets simulados no públicos:

### farms_private.csv

| farm_id | name | comuna_code |
|---|---|---|
| F001 | Granja San Vicente | 13101 |
| F002 | Granja Norte | 05101 |

### animals_private.csv

| animal_id | farm_id | species | birth_date |
|---|---|---|---|
| A001 | F001 | pig | 2025-05-10 |
| A002 | F001 | pig | 2025-05-12 |
| A003 | F002 | chicken | 2025-11-01 |

### weights_private.csv

| record_id | animal_id | date | weight_kg |
|---|---|---|---|
| W001 | A001 | 2026-02-10 | 42.1 |
| W002 | A001 | 2026-02-24 | 55.4 |
| W003 | A002 | 2026-02-24 | 52.0 |

---

## 3.2 Datos abiertos

Se utilizó un dataset abierto de **comunas y regiones de Chile** en formato CSV.

| comuna_code | comuna_name | region_name |
|---|---|---|
| 13101 | Santiago | Región Metropolitana |
| 05101 | Valparaíso | Región de Valparaíso |

Este dataset originalmente no está representado en RDF.

---

# 4. Modelo RDF

Se definieron las siguientes clases:

- Farm
- Animal
- WeightRecord
- Comuna
- Region

Relaciones principales:

Animal → raisedInFarm → Farm  
Farm → locatedInComuna → Comuna  
Comuna → inRegion → Region  
WeightRecord → forAnimal → Animal

Ejemplo RDF (Turtle):

```turtle
ex:animal/A001 a ex:Animal ;
  ex:species "pig" ;
  ex:birthDate "2025-05-10" ;
  ex:raisedInFarm ex:farm/F001 .
```

---

# 5. Transformación de datos

Los datos CSV fueron transformados a RDF utilizando **Python y la librería rdflib**.

El proceso consiste en:

1. Leer archivos CSV
2. Generar URIs para cada entidad
3. Crear triples RDF
4. Exportar el grafo en formato Turtle

Archivos generados:

- private.ttl
- open.ttl
- merged.ttl

---

# 6. Validación con Shape Expressions (ShEx)

Se definió un esquema de validación para asegurar la consistencia del grafo.

Ejemplo de shape:

```
ex:AnimalShape {
  a [ex:Animal] ;
  ex:species xsd:string ;
  ex:birthDate xsd:date ;
  ex:raisedInFarm IRI
}
```

Las entidades del grafo se validan contra estas restricciones.

---

# 7. Validación de errores

Para demostrar el funcionamiento del esquema ShEx se incluyó un ejemplo con errores:

```
ex:weightRecord/WBAD a ex:WeightRecord ;
  ex:forAnimal ex:animal/A001 ;
  ex:recordDate "2026-02-30" ;
  ex:weightKg "cincuenta" .
```

Errores detectados:

- Fecha inválida
- Tipo de dato incorrecto

La validación ShEx detecta correctamente estas inconsistencias.

---

# 8. Estructura del repositorio

```
project
│
├── data
│   ├── farms_private.csv
│   ├── animals_private.csv
│   ├── weights_private.csv
│   └── comunas_open.csv
│
├── rdf
│   ├── private.ttl
│   ├── open.ttl
│   └── merged.ttl
│
├── validation
│   ├── schema.shex
│   └── invalid_examples.ttl
│
└── README.md
```

---

# 9. Ejecución

Instalar dependencias:

```
pip install rdflib pyshex pandas
```

Ejecutar el script o notebook que transforma los CSV a RDF.

---

# 10. Resultados

El ejercicio demuestra cómo:

- integrar **datos privados y datos abiertos**
- modelar información con **RDF**
- validar estructuras de datos mediante **ShEx**
- detectar inconsistencias automáticamente

Esto ilustra el potencial de la **Web Semántica en sistemas productivos agroindustriales**.

---

# 11. Trabajo futuro

En las siguientes tareas se utilizará este grafo para:

- consultas **SPARQL**
- comparación con **Wikidata**
- evaluación con **Large Language Models**
