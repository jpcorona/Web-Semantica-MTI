# Tarea 4 — Datos abiertos, privacidad y el proyecto Solid

## 1. Introducción

El crecimiento de los datos abiertos (Open Data) ha permitido avances significativos en transparencia gubernamental, innovación y análisis de datos. Sin embargo, la apertura de datos plantea tensiones fundamentales con la privacidad y la protección de información sensible. Este documento analiza cómo pueden convivir los datos abiertos y la privacidad, los riesgos de su combinación, y cómo el proyecto Solid propone un nuevo modelo de control de datos. El análisis se relaciona con el dominio de producción animal utilizado en las tareas anteriores.

## 2. Convivencia entre datos abiertos y privacidad

Los datos abiertos y la privacidad no son necesariamente opuestos, pero su coexistencia requiere diseño cuidadoso. Existen múltiples mecanismos que permiten publicar datos útiles sin comprometer información sensible.

**Anonimización y agregación:** Los datos pueden publicarse en forma agregada (por ejemplo, producción total por región) sin revelar datos individuales de cada granja. Técnicas como *k-anonimidad* y *privacidad diferencial* permiten proteger identidades individuales dentro de datasets publicados (Dwork & Roth, 2014).

**Clasificación de datos por sensibilidad:** En el contexto de producción animal, datos como las comunas donde operan las granjas o las especies criadas pueden ser públicos, mientras que volúmenes de producción, costos operacionales o datos sanitarios específicos deben ser privados. La taxonomía de datos es fundamental.

**Licenciamiento y control de uso:** Datos abiertos no significa datos sin restricciones. Licencias como Creative Commons permiten establecer condiciones de uso, atribución y redistribución.

## 3. Riesgos de la combinación de datos

El mayor riesgo emerge cuando se combinan múltiples fuentes de datos abiertos, lo que puede generar inferencias no deseadas.

**Re-identificación por cruce de datasets:** En el ejercicio de este curso, al combinar datos de granjas (privados) con datos de comunas y regiones (abiertos), se puede identificar la ubicación precisa de operaciones productivas. Si alguien publicara además datos del SAG (Servicio Agrícola y Ganadero) sobre autorizaciones sanitarias por comuna, podría triangular la identidad de granjas específicas. Sweeney (2002) demostró que el 87% de la población de EE.UU. puede ser re-identificada combinando código postal, fecha de nacimiento y sexo.

**Inferencia de información competitiva:** En la industria agroindustrial, datos aparentemente inocuos como la distribución geográfica de granjas y las especies criadas, combinados con datos de transporte o consumo energético (disponibles en portales como energiaabierta.cne.cl), podrían permitir a competidores estimar capacidades de producción.

**Riesgo en cadena:** Los datos abiertos de una fuente pueden combinarse con datos de redes sociales, imágenes satelitales u otras fuentes para generar perfiles detallados de operaciones privadas. En producción animal, imágenes satelitales públicas combinadas con datos de permisos ambientales (disponibles en retc.mma.gob.cl) podrían revelar información operacional sensible.

## 4. Ejemplos concretos en el dominio de producción animal

**Ejemplo 1 — Trazabilidad pública vs. secreto comercial:** Chile exige trazabilidad animal a través del SAG. Los datos de movimiento de animales entre predios son necesarios para control sanitario, pero si se publicaran abiertamente, revelarían las cadenas de suministro de cada empresa.

**Ejemplo 2 — Datos ambientales:** El Registro de Emisiones y Transferencias de Contaminantes (RETC) publica datos de emisiones por establecimiento. Cruzando estos datos con la ubicación de granjas, se podría inferir la escala de operación de cada instalación.

**Ejemplo 3 — Datos de empleo:** Los datos abiertos de empleo por sector y comuna (disponibles en el INE) combinados con la ubicación de granjas podrían revelar la dependencia laboral de una comunidad respecto a una empresa específica, información que podría usarse en negociaciones laborales o regulatorias.

## 5. El proyecto Solid y su relación con estos desafíos

**Solid** (Social Linked Data) es un proyecto impulsado por Tim Berners-Lee cuyo objetivo es devolver a los usuarios el control sobre sus datos personales mediante una arquitectura descentralizada (Berners-Lee, 2018). En Solid, cada usuario o entidad almacena sus datos en un **POD** (Personal Online Data Store) y las aplicaciones solicitan permisos explícitos para acceder a datos específicos.

### Principios relevantes de Solid

**Desacoplamiento datos-aplicación:** Los datos se almacenan independientemente de las aplicaciones que los consumen. Una granja podría tener su POD con datos de producción, y distintas aplicaciones (control sanitario, reportes al SAG, análisis interno) acceden solo a la porción autorizada.

**Control granular de acceso:** Solid utiliza Web Access Control (WAC) que permite definir permisos a nivel de recurso individual. Una granja podría permitir que el SAG acceda a datos de trazabilidad, que su empresa matriz acceda a datos de producción, y que investigadores accedan solo a datos agregados anonimizados.

**Interoperabilidad semántica:** Solid utiliza estándares de la Web Semántica (RDF, Linked Data) como formato nativo de datos, lo que lo hace compatible con los grafos de conocimiento trabajados en este curso. Los datos en un POD se representan como triples RDF, facilitando la integración con ontologías y consultas SPARQL.

### Cómo Solid aborda los riesgos identificados

**Re-identificación:** Si los datos están en PODs separados con control de acceso, la combinación no autorizada de datasets se dificulta significativamente. Cada propietario decide qué datos comparte y con quién.

**Inferencia competitiva:** Una empresa agroindustrial podría compartir datos agregados de sustentabilidad (para cumplir con regulaciones de ESG) sin exponer datos operacionales detallados, usando los permisos granulares de Solid.

**Soberanía de datos:** En el modelo actual, plataformas centralizadas acumulan datos de múltiples actores. Solid invierte este modelo: cada granja, cada veterinario, cada organismo regulador mantiene sus datos en su POD y comparte selectivamente.

### Limitaciones de Solid en el contexto actual

Solid es un proyecto en desarrollo y presenta desafíos prácticos: adopción limitada en la industria, inmadurez de herramientas, y la complejidad de migrar sistemas existentes a una arquitectura descentralizada. En el contexto agroindustrial chileno, la transición requeriría un esfuerzo significativo de estandarización y capacitación.

## 6. Aplicación en el dominio trabajado

En nuestro ejercicio, combinamos datos privados de granjas con datos abiertos de comunas. Un modelo basado en Solid permitiría:

- Que cada granja almacene sus datos de producción en un POD privado.
- Que el SAG acceda a datos de trazabilidad con permisos específicos.
- Que investigadores de universidades accedan a datos anonimizados y agregados.
- Que los datos abiertos de comunas y regiones (INE) se mantengan como Linked Open Data accesible para todos.
- Que las consultas SPARQL se ejecuten de forma federada entre PODs autorizados y endpoints públicos.

## 7. Conclusión

Los datos abiertos y la privacidad pueden coexistir cuando se implementan mecanismos adecuados de anonimización, control de acceso y gobernanza de datos. El principal riesgo no está en la apertura de un dataset individual, sino en la combinación no anticipada de múltiples fuentes. Solid propone un modelo prometedor que, al descentralizar el almacenamiento y poner el control en el propietario de los datos, podría mitigar significativamente estos riesgos. Sin embargo, su adopción en contextos industriales como la producción animal en Chile requiere madurez tecnológica y voluntad de estandarización sectorial.

## Referencias

- Berners-Lee, T. (2018). One Small Step for the Web... *Inrupt Blog*. https://www.inrupt.com/blog/one-small-step-for-the-web
- Dwork, C., & Roth, A. (2014). The Algorithmic Foundations of Differential Privacy. *Foundations and Trends in Theoretical Computer Science*, 9(3-4), 211-407.
- Sweeney, L. (2002). k-Anonymity: A Model for Protecting Privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, 10(5), 557-570.
- Sambra, A. V., Mansour, E., Hawke, S., et al. (2016). Solid: A Platform for Decentralized Social Applications Based on Linked Data. *MIT CSAIL Technical Report*.
- Verborgh, R. (2020). Re-decentralizing the Web, for good this time. In *Linking the World's Information: Essays on Tim Berners-Lee's Invention of the World Wide Web*, ACM.
- Gobierno de Chile. (2024). Portal de Datos Abiertos. http://datos.gob.cl/
- RETC Chile. (2024). Registro de Emisiones y Transferencias de Contaminantes. https://retc.mma.gob.cl/
