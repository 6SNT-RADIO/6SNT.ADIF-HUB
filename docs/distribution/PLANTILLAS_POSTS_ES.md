# Plantillas de posts ES

## Discovery

Estoy trabajando en una herramienta local para limpiar y consolidar logs antes de subirlos a plataformas como LoTW/eQSL/ClubLog. Que formato les causa mas problemas hoy: ADIF, Cabrillo, CSV, Excel u otro?

## Explicacion ADIF

ADIF es excelente como formato de intercambio, pero muchos problemas aparecen antes: columnas incompletas, duplicados, horas diferentes y exports mezclados. Estoy probando un flujo local para revisar eso antes de subir.

## Cabrillo

Los logs Cabrillo son buenos para concursos, pero reutilizarlos como log general puede ser dificil porque el exchange cambia por concurso. Estoy validando un mapper local hacia ADIF con revision manual.

## Excel/CSV

Muchos operadores mantienen QSOs historicos en Excel o CSV. El reto no es abrir el archivo, sino mapear columnas y evitar duplicados antes de exportar ADIF.

## Invitacion beta cerrada

Busco pocos operadores para una beta cerrada de una app local de limpieza ADIF. No necesito logs reales publicos: solo feedback y, si aparece un error, un caso saneado minimo.

## Demo deduplicacion

Demo tecnica: importar, normalizar, detectar duplicados probables y resolver conflictos antes de exportar `ADI`. La idea no es automatizar a ciegas, sino mantener control del operador.

## Release notes

Nueva build beta: mejoras en formatos, mapper, deduplicacion y documentacion. Limitaciones conocidas documentadas. Feedback tecnico bienvenido.

