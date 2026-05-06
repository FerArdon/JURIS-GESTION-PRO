# JURIS-GESTIÓN-PRO — Manual de Usuario

## Sistema de Gestión Jurídica para Despachos y Abogados Independientes

Versión 2.0 · Mayo 2026

---

## Tabla de Contenidos

1. [Introducción y Zonas de la Interfaz](#1-introducción-y-zonas-de-la-interfaz)
2. [Menú Lateral — Navegación Principal](#2-menú-lateral--navegación-principal)
3. [Barra Superior y Panel JURIS-AI (Copilot)](#3-barra-superior-y-panel-juris-ai-copilot)
4. [Dashboard Analítico](#4-dashboard-analítico)
5. [Clientes — Directorio CRM](#5-clientes--directorio-crm)
6. [Expedientes y Casos — Pantalla Principal](#6-expedientes-y-casos--pantalla-principal)
   - 6.1 [Barra de Herramientas](#61-barra-de-herramientas)
   - 6.2 [Pestañas de Estado](#62-pestañas-de-estado)
   - 6.3 [Registrar Nuevo Expediente](#63-registrar-nuevo-expediente)
   - 6.4 [Panel de Gestión del Expediente](#64-panel-de-gestión-del-expediente)
   - 6.5 [Editor de Documentos y Plantillas](#65-editor-de-documentos-y-plantillas)
   - 6.6 [Selector de Caso para Redactar](#66-selector-de-caso-para-redactar)
7. [Protocolo Notarial](#7-protocolo-notarial)
8. [Calendario de Audiencias y Plazos](#8-calendario-de-audiencias-y-plazos)
   - 8.1 [Selector de Fecha — Calendario dd-mm-aaaa](#81-selector-de-fecha--calendario-dd-mm-aaaa)
   - 8.2 [Programar Nueva Audiencia](#82-programar-nueva-audiencia)
   - 8.3 [Ficha Técnica de Audiencia](#83-ficha-técnica-de-audiencia)
9. [Configuración del Sistema](#9-configuración-del-sistema)
   - 9.1 [Identidad Institucional](#91-identidad-institucional)
   - 9.2 [Catálogos Externos](#92-catálogos-externos)
   - 9.3 [Seguridad de Acceso — PIN](#93-seguridad-de-acceso--pin)
   - 9.4 [Personalización Visual](#94-personalización-visual)
   - 9.5 [Escudo de Datos — Backups](#95-escudo-de-datos--backups)
10. [JURIS-AI — Asistente Inteligente](#10-juris-ai--asistente-inteligente)
11. [Indicador de Estado del Sistema](#11-indicador-de-estado-del-sistema)
12. [Flujo de Trabajo Recomendado](#12-flujo-de-trabajo-recomendado)
13. [Preguntas Frecuentes](#13-preguntas-frecuentes)
14. [Estructura de Archivos del Sistema](#14-estructura-de-archivos-del-sistema)

---

## 1. Introducción y Zonas de la Interfaz

JURIS-GESTIÓN-PRO es una aplicación de escritorio nativa para Windows diseñada para la gestión integral de despachos jurídicos y abogados independientes. Funciona completamente sin conexión a internet (offline) y almacena todos los datos de forma local y segura en tu equipo.

La interfaz utiliza el **Windows 11 Fluent Design System**: colores neutros integrados, bordes redondeados sutiles, tipografía Segoe UI y sombras suaves. El panel de JURIS-AI ya **no ocupa espacio permanente** — se abre como un overlay lateral (estilo Copilot) al pulsarlo.

La interfaz se divide en **dos zonas permanentes** más el panel IA opcional:

```text
┌──────────────────────────────────────────────────────────────┐
│  MENÚ LATERAL   │            BARRA SUPERIOR                  │
│  (navegación)   │  [ Título del módulo ]   [ ⚖️ JURIS-AI ]  │
│─────────────────│────────────────────────────────────────────│
│  📊 Dashboard   │                                            │
│  👥 Clientes    │         ÁREA DE TRABAJO CENTRAL            │
│  📁 Expedientes │         (pantalla de la sección            │
│  📜 Protocolo   │          seleccionada en el menú)          │
│  📅 Calendario  │                                            │
│  ⚙️  Config     │                                            │
│  📺 Tutorial    │                            ● Escudo OK     │
└──────────────────────────────────────────────────────────────┘
```

> **Panel JURIS-AI:** Al hacer clic en el botón **⚖️ JURIS-AI** (esquina superior derecha), el asistente se despliega como panel flotante desde la derecha sin interrumpir el área de trabajo. Un fondo semitransparente indica que el panel está activo. Se cierra con el botón **✕** dentro del panel o volviendo a pulsar el botón del header.

| Zona | Función |
|------|---------|
| **Menú Lateral** | Navegación entre las 7 secciones. Colapsable al hacer clic en el logo |
| **Barra Superior** | Muestra el título del módulo activo y el botón de acceso a JURIS-AI |
| **Área de Trabajo** | Pantalla activa según la sección seleccionada |
| **Panel JURIS-AI** | Overlay flotante (Copilot style). Se abre/cierra con el botón del header |
| **Indicador inferior** | Pastilla en esquina inferior derecha con el estado del Escudo de Datos |

---

## 2. Menú Lateral — Navegación Principal

La barra izquierda siempre está visible. Fondo neutro claro integrado con el área de trabajo (Windows 11 NavigationView). El ítem activo se resalta con el color azul de acento y un indicador vertical a su izquierda.

| Ícono | Sección | Para qué sirve |
|-------|---------|----------------|
| 📊 | **Dashboard** | Vista general con estadísticas, gráficos y metas |
| 👥 | **Clientes (CRM)** | Directorio completo de clientes registrados |
| 📁 | **Expedientes** | Gestión de todos los casos. **Pantalla principal del sistema** |
| 📜 | **Protocolo** | Libro digital de protocolo notarial |
| 📅 | **Calendario** | Cronograma de audiencias y plazos procesales |
| ⚙️ | **Configuración** | Ajustes del despacho, seguridad y apariencia |
| 📺 | **Tutorial (Ayuda)** | Video y manual integrado del sistema |

**Colapsar el menú lateral:** Haz clic sobre la zona del logo (parte superior del menú). El menú se contrae mostrando solo los íconos. Vuelve a hacer clic para expandirlo.

> Al hacer clic en cualquier ítem del menú, el área de trabajo cambia de pantalla instantáneamente sin recargar la aplicación.

---

## 3. Barra Superior y Panel JURIS-AI (Copilot)

La barra superior (64px de altura) contiene:

| Elemento | Posición | Función |
|----------|----------|---------|
| **Título del módulo** | Centro | Muestra el nombre de la sección activa |
| **Nombre del despacho** | Subtítulo (centro) | Nombre institucional configurado |
| **Botón ⚖️ JURIS-AI** | Derecha | Abre / cierra el panel del asistente IA |

### Abrir el Panel JURIS-AI

1. Pulsa el botón **⚖️ JURIS-AI** en la esquina superior derecha de la barra.
2. El panel se desliza desde la derecha (360px de ancho).
3. Un fondo semitransparente cubre el área de trabajo indicando que el panel está activo.
4. Para cerrar: pulsa **✕** dentro del panel, o vuelve a pulsar el botón **⚖️ JURIS-AI**.

> El panel siempre arranca **cerrado** al iniciar la aplicación para no interferir con el flujo de trabajo. No hay estado persistido entre sesiones.

---

## 4. Dashboard Analítico

Pantalla de resumen ejecutivo del despacho. Se actualiza automáticamente cada vez que se realizan cambios en expedientes o audiencias.

### Tarjetas de Estadística

| Tarjeta | Qué muestra |
|---------|-------------|
| **Casos Activos** | Total de expedientes con estado "Activo" |
| **En Proceso** | Total de expedientes con estado "En Proceso" |
| **Casos Cerrados** | Expedientes finalizados o archivados |
| **Honorarios Proyectados (L.)** | Suma de todas las cuantías registradas en expedientes y audiencias |

### Gráfico de Distribución

Gráfico de barras (Chart.js) que muestra la cantidad de casos por estado (Activo / En Proceso / Cerrado). Requiere el archivo `assets/js/chart.js` instalado localmente. Si no está disponible, el sistema funciona normalmente sin el gráfico y registra un aviso en consola.

### Estado del Protocolo

Indica si el libro notarial está dentro del límite de 200 folios por tomo:
- Instrumentos registrados y número del último folio utilizado.
- Alerta visual `⚠️ Protocolo por llenarse` cuando supera los 180 folios.
- Indicador `✅ Protocolo OK` cuando está dentro del límite.

### Metas Mensuales

Barra de progreso que compara los honorarios acumulados contra la meta mensual configurada.

- **✏️ Editar** — Abre un cuadro para modificar la meta mensual de ingresos en Lempiras.

### Botones de Exportación

| Botón | Función |
|-------|---------|
| **📊 Exportar CSV** | Descarga un archivo `.csv` con todos los expedientes para abrir en Excel |
| **📄 Reporte PDF** | Genera un reporte ejecutivo e invoca el diálogo de impresión del sistema |

---

## 5. Clientes — Directorio CRM

Aquí se registra y administra la información de todas las personas naturales o jurídicas que son clientes del despacho. **Todo expediente debe estar vinculado a un cliente registrado.**

### Tabla de Clientes

Columnas visibles: `DNI / RTN` · `Nombre Completo` · `Teléfono` · `Fecha Registro` · `Acciones`

**Botones de acción por fila:**
- **✏️ Editar** — Abre el formulario de edición (requiere PIN si está configurado).
- **🗑️ Eliminar** — Elimina el registro del cliente (requiere PIN). **No se puede deshacer.**

### Botón: + Nuevo Cliente

Abre el formulario de registro con los siguientes campos:

| Campo | Obligatorio | Descripción |
|-------|:-----------:|-------------|
| **Nombre Completo** | ✅ | Nombre de la persona natural o razón social |
| **DNI / RTN** | ✅ | Documento Nacional de Identidad o Registro Tributario. **Debe ser único** |
| **Teléfono** | ❌ | Número de contacto. Ejemplo: `9911-2233` |
| **Correo Electrónico** | ❌ | Email del cliente |
| **Dirección** | ❌ | Ciudad y departamento de residencia |

**Botones del formulario:**
- **✅ Guardar Cliente** — Registra al cliente en la base de datos.
- **Cancelar** — Cierra el formulario sin guardar cambios.

> **⚠️ Importante:** Si intentas registrar un DNI que ya existe en el sistema, recibirás un error. Verifica que el cliente no esté ya registrado antes de crearlo.

---

## 6. Expedientes y Casos — Pantalla Principal

Es el núcleo del sistema. Aquí se crean, consultan, gestionan y redactan todos los expedientes judiciales del despacho.

---

### 6.1 Barra de Herramientas

#### 🔍 Campo de Búsqueda
Filtra la tabla en **tiempo real** al escribir cualquier texto. Busca en todas las columnas: ID del caso, nombre del cliente, juzgado, materia y estado. No requiere presionar Enter.

#### Botón: + Nuevo Expediente
Abre el formulario de registro de un nuevo caso. Ver [sección 6.3](#63-registrar-nuevo-expediente).

#### Botón: 📄 Redactar Escrito
Abre el editor de documentos jurídicos.
- Si hay un expediente seleccionado (fila clicada), abre el editor directamente.
- Si no hay ninguno seleccionado, muestra el [Selector de Caso](#66-selector-de-caso-para-redactar).

---

### 6.2 Pestañas de Estado

Filtran la tabla mostrando solo los expedientes del estado elegido. Cada pestaña tiene un contador (badge) con la cantidad de casos.

| Pestaña | Estado | Significado |
|---------|--------|-------------|
| **Activos** | `Activo` | Casos recién abiertos o en etapa inicial |
| **En Proceso** | `En Proceso` | Casos con actuaciones procesales en marcha |
| **Cerrados** | `Cerrado` | Casos finalizados, archivados o resueltos |

---

### 6.3 Registrar Nuevo Expediente

| Campo | Obligatorio | Descripción |
|-------|:-----------:|-------------|
| **Materia Legal** | ✅ | Selector desplegable. Al elegir la materia, el ID se genera automáticamente |
| **ID del Expediente 🔒** | Auto | Campo de solo lectura. Formato: `AÑO-COD-NÚM`. Ejemplo: `2026-CIV-003` |
| **Cliente** | ✅ | Selector con todos los clientes del CRM |
| **Juzgado** | ❌ | Nombre del tribunal competente |
| **Cuantía / Honorarios (L.)** | ❌ | Monto en Lempiras. Se suma a los "Honorarios Proyectados" del Dashboard |

**Materias disponibles y sus códigos:**

| Materia | Código | Ejemplo de ID |
|---------|--------|---------------|
| Civil | `CIV` | `2026-CIV-001` |
| Penal | `PEN` | `2026-PEN-001` |
| Laboral | `LAB` | `2026-LAB-001` |
| Familia | `FAM` | `2026-FAM-001` |
| Mercantil y Empresarial | `MER` | `2026-MER-001` |
| Administrativo | `ADM` | `2026-ADM-001` |
| Agrario | `AGR` | `2026-AGR-001` |
| Constitucional | `CON` | `2026-CON-001` |
| Notarial | `NOT` | `2026-NOT-001` |

---

### 6.4 Panel de Gestión del Expediente

Se abre al **hacer clic sobre cualquier fila** de la tabla. Muestra el ID del caso y el nombre del cliente en la cabecera.

#### Cambiar Estado del Expediente

| Botón | Estado destino | Cuándo usarlo |
|-------|---------------|---------------|
| **🟢 Activo** | `Activo` | Al reactivar un caso o en etapa inicial |
| **🟡 En Proceso** | `En Proceso` | Cuando el caso tiene actuaciones activas |
| **🔴 Cerrado** | `Cerrado` | Al concluir el caso por cualquier vía |

#### Botones de Acción

| Botón | Función |
|-------|---------|
| **🗑️ Eliminar** | Elimina el expediente permanentemente. Requiere PIN. **No se puede deshacer.** |
| **✏️ Editar** | Modifica la materia legal y el juzgado del expediente. Requiere PIN. |
| **📄 Redactar Documento** | Abre el editor de escritos con este expediente como contexto activo. |

---

### 6.5 Editor de Documentos y Plantillas

Panel de redacción jurídica que se despliega dentro de la pantalla de Expedientes. Vincula cada documento a un expediente e **inyecta automáticamente** los datos del cliente y caso al cargar una plantilla.

#### Elementos del Editor

| Elemento | Función |
|----------|---------|
| **📄 Caso: [ID]** | Muestra el ID del expediente activo |
| **🔍 Buscador de plantillas** | Filtra en tiempo real (ej: `divorcio`, `compraventa`, `penal`) |
| **Selector desplegable** | Lista todas las plantillas disponibles por categoría |
| **Cargar y Autocompletar** | Carga la plantilla e inyecta los datos reales del caso |
| **Área de edición** | Campo libre donde aparece la plantilla autocompletada |

#### Formato Markdown soportado

| Sintaxis | Resultado en Word |
|----------|-------------------|
| `# Título` | Título en negrita centrado |
| `## Subtítulo` | Subtítulo en negrita centrado |
| `**texto**` | Texto en negrita |
| `- ítem` | Ítem de lista con viñeta |
| `---` | Línea horizontal separadora |
| Texto normal | Párrafo justificado |

#### Botones del Editor

| Botón | Función |
|-------|---------|
| **📄 Exportar como Word (.docx)** | Convierte el contenido a documento Word profesional |
| **Cerrar** | Cierra el editor y regresa a la tabla de expedientes |

#### Especificaciones del documento Word generado

| Atributo | Valor |
|----------|-------|
| Formato | `.docx` (Microsoft Word) |
| Tamaño de papel | Legal (8.5" × 14") |
| Fuente | Times New Roman 14 pt |
| Espaciado | 1.5 líneas, alineación justificada |
| Márgenes | Izquierdo 3.0 cm · Resto 2.5 cm |

> **⚠️ El editor no guarda automáticamente.** Exporta a Word antes de cerrar.

#### Plantillas precargadas disponibles

**Derecho Civil:** Acuerdo de Partición · Contrato de Arrendamiento · Compraventa · Fianza · Opción de Compra · Transporte de Mercancías · Demanda Abreviada · Patrimonio Familiar · Manifestación · Comunicación Subsidiaria · Testamento Abierto · Testamento Cerrado

**Derecho Familiar:** Reconocimiento de Hijos · Acuerdo de Convivencia · Pasaporte de Menores · Convenio Regulador · Solicitud de Alimentos y Custodia

**Derecho Laboral:** Junta para Fusión · Carta de Renuncia/Despido · Contrato Individual · Convenio de Terminación · Reglamento Interno

**Derecho Mercantil:** Acta Constitutiva · Cesión de Patentes · Compraventa de Empresa · Franquicia · Licencia de Patentes · Representación Comercial · Estatutos y Poderes

**Derecho Penal y Administrativo:** Denuncia y Querella · Defensa/Contestación · Apelación/Amparo · Habilitación Inhábiles · Medidas Cautelares · Revisión de Sentencia

**Otros:** Acta Notarial · Carta Poder · Arrendamiento Rústico · Comodato · Donación · Préstamo/Mutuo · Declaración Jurada · Poder General y Especial · Apostilla

---

### 6.6 Selector de Caso para Redactar

Se muestra cuando pulsas **📄 Redactar Escrito** sin haber seleccionado ningún expediente.

| Elemento | Función |
|----------|---------|
| **🔍 Filtrar expedientes...** | Busca en tiempo real dentro de la lista |
| **Lista de expedientes** | Muestra todos los casos con ID, cliente, materia y estado |
| **Clic sobre un expediente** | Selecciona el caso y abre el editor vinculado |

---

## 7. Protocolo Notarial

Módulo exclusivo para abogados con función notarial. Lleva el control digital del libro de protocolo, instrumentos autorizados y control de folios por tomo.

### Tarjetas de Resumen

| Tarjeta | Descripción |
|---------|-------------|
| **Instrumentos Registrados** | Cantidad total de escrituras en el tomo actual |
| **Último Folio Utilizado** | Número del último folio registrado |

### Tabla de Protocolo

Columnas: `No.` · `Fecha` · `Cliente / Otorgante` · `Naturaleza del Acto` · `Folios` · `Acciones`

**Botones de acción por fila:**
- **🗑️ Eliminar** — Elimina el instrumento (requiere PIN).

### Botón: + Nuevo Instrumento

| Campo | Descripción |
|-------|-------------|
| **Cliente / Otorgante (ID)** | Número de ID del cliente en el CRM |
| **Naturaleza del Acto** | Tipo de escritura. Ejemplo: `Escritura de Compraventa` |
| **Cantidad de Folios** | Folios que ocupará el instrumento |

### Botón: 📄 Exportar Índice

Genera el índice notarial completo del tomo y lo exporta como archivo `.md`.

---

## 8. Calendario de Audiencias y Plazos

Cronograma de todas las actuaciones procesales programadas.

### Tabla de Audiencias

Columnas: `Fecha y Hora` · `Expediente` · `Tipo de Audiencia` · `Juzgado` · `Observaciones` · `Acciones`

| Botón | Función |
|-------|---------|
| **📋 Ver Ficha** | Abre la Ficha Técnica completa de preparación |
| **✏️ Editar** | Modifica los datos (requiere PIN) |
| **🗑️ Eliminar** | Elimina la audiencia (requiere PIN) |

---

### 8.1 Selector de Fecha — Calendario dd-mm-aaaa

Todos los campos de fecha del sistema usan un **calendario desplegable personalizado** en lugar del selector nativo del navegador. El formato de visualización es siempre `dd-mm-aaaa`.

```text
┌─────────────────────────────────┐
│  ‹       Mayo 2026        ›     │
├─────────────────────────────────┤
│  Lu  Ma  Mi  Ju  Vi  Sá  Do    │
│                   1   2   3     │
│   4   5   6   7   8   9  10    │
│  11  12  13  14  15  16  17    │
│  18  19  20  21  22  23  24    │
│  [25] 26  27  28  29  30  31   │  <- día seleccionado en azul
├─────────────────────────────────┤
│  [ Hoy ] [ Cancelar ] [Aceptar] │
└─────────────────────────────────┘
```

**Cómo usar el selector de fecha:**

1. Haz clic sobre el campo de fecha — se despliega el calendario.
2. Usa **‹** y **›** para navegar entre meses.
3. Haz clic sobre el día deseado — queda marcado en azul.
4. Ajusta la hora directamente en el campo de tiempo (`08:00`) dentro del campo visible.
5. Pulsa **Aceptar** para confirmar.
6. El campo muestra la fecha en formato `dd-mm-aaaa`. Internamente se guarda en formato ISO para el backend.

**Botones del calendario:**

| Botón | Función |
|-------|---------|
| **‹ / ›** | Navegar al mes anterior / siguiente |
| **Hoy** | Saltar al día de hoy y marcarlo |
| **Cancelar** | Cerrar el calendario sin guardar |
| **Aceptar** | Confirmar la fecha seleccionada |

---

### 8.2 Programar Nueva Audiencia

**Botón: + Programar Audiencia**

| Campo | Obligatorio | Descripción |
|-------|:-----------:|-------------|
| **Tipo de Audiencia** | ✅ | Selector con 9 tipos disponibles |
| **ID del Expediente** | ✅ | Código del expediente. Ejemplo: `2026-CIV-001` |
| **Fecha y Hora** | ✅ | Usa el [calendario desplegable](#81-selector-de-fecha--calendario-dd-mm-aaaa) + campo de hora inline |
| **Cuantía / Honorarios (L.)** | ✅ | Monto que se acumula en los honorarios del Dashboard |
| **Observaciones Especiales** | ❌ | Notas relevantes. Ejemplo: `Llevar peritos, preparar testigos` |

**Tipos de audiencia disponibles:**
1. Audiencia Inicial
2. Audiencia Preliminar
3. Audiencia de Juicio Oral y Público
4. Audiencia de Conciliación
5. Audiencia de Medidas Cautelares
6. Audiencia de Revisión o Apelación
7. Audiencia de Ejecución de Sentencia
8. Audiencia de Reconocimiento o Ratificación
9. Audiencia de Tutela o Protección

---

### 8.3 Ficha Técnica de Audiencia

Documento interno de preparación. Se accede desde **📋 Ver Ficha** en la tabla.

**Sección 1 — Datos Generales del Expediente:**
Número de caso, materia/juzgado, partes del proceso y cuantía.

**Sección 2 — Control Operativo:**
- Tipo de audiencia y fecha/hora programada.
- **Anotaciones Pre-Audiencia (JURIS-AI):** Recordatorios automáticos:
  - Verificar plazos fatales de la etapa probatoria.
  - Confirmar comparecencia del perito técnico.
  - Revisar incidentes procesales pendientes de resolución.
- **Espacio de Observaciones:** Campo editable para notas en tiempo real.

**Sección 3 — Resolución y Seguimiento:**
- Resultado de la audiencia (Pendiente / Favorable / Desfavorable / Suspendida / Conciliada).
- Campo de texto libre para registrar el resultado y próximas acciones.

**Botones de la Ficha:**

| Botón | Función |
|-------|---------|
| **🖨️ Imprimir / PDF** | Abre ventana de impresión con logo del despacho y formato profesional |
| **Guardar Ficha** | Cierra el modal guardando las notas ingresadas |
| **Cancelar** | Cierra sin guardar los cambios |

---

## 9. Configuración del Sistema

Panel de ajustes generales. Los cambios se aplican a toda la aplicación.

> **Importante:** Siempre pulsa **💾 Guardar Configuración** al finalizar los cambios en esta pantalla.

---

### 9.1 Identidad Institucional

| Campo / Control | Descripción |
|-----------------|-------------|
| **Nombre del Despacho / Unidad** | Aparece en el header, Ficha Técnica y todos los reportes |
| **Lema Legal (Opcional)** | Subtítulo del despacho |
| **Exequatur** | Número de exequatur notarial (si aplica) |
| **📂 Seleccionar Archivo...** (Logo) | Selecciona el logo oficial (PNG recomendado, 200×200 px). Aparece en el menú lateral, Ficha y reportes PDF |
| **🗑️ Quitar Logo** | Elimina el logo institucional configurado |

---

### 9.2 Catálogos Externos

| Control | Descripción |
|---------|-------------|
| **Campo: Base de Incidentes** | Ruta del archivo JSON con el catálogo de incidentes procesales |
| **📂 Enlazar Archivo...** | Vincula un JSON personalizado con incidentes adicionales |

---

### 9.3 Seguridad de Acceso — PIN

| Campo | Descripción |
|-------|-------------|
| **PIN de Administrador** | Contraseña numérica (4-8 dígitos). Se solicita antes de editar o eliminar cualquier registro |

> **⚠️ Recomendación:** Configura siempre un PIN de administrador para proteger los datos del despacho.

**¿Olvidaste el PIN?**
En la pantalla de ingreso de PIN, usa el enlace **"¿Olvidó su PIN de Administrador?"** e introduce el código maestro del sistema para restablecerlo.

---

### 9.4 Personalización Visual

#### Modo de Visualización

| Opción | Descripción |
|--------|-------------|
| **Claro (Estilo Windows)** | Fondo `#F3F3F3`, texto oscuro. Estilo Windows 11 nativo |
| **Oscuro (Estilo Windows)** | Fondo `#202020`, texto claro. Ideal para trabajo nocturno |
| **Personalizado** | Habilita el selector libre de color de fondo |

#### Color de Acento

Cinco círculos que cambian el color principal de botones, bordes y elementos destacados:

| Color | Código hex |
|-------|-----------|
| Azul (predeterminado) | `#0067C0` |
| Verde | `#23F860` |
| Morado | `#8B5CF6` |
| Rojo | `#F43F5E` |
| Dorado | `#EAB308` |

---

### 9.5 Escudo de Datos — Backups

El sistema crea automáticamente un respaldo comprimido (`.jgpbackup`) de la base de datos y las plantillas **cada vez que se cierra la aplicación**. Los respaldos se guardan en la carpeta `backups/`.

| Control | Descripción |
|---------|-------------|
| **🛡️ Generar Respaldo Manual Ahora** | Crea un respaldo inmediato sin necesidad de cerrar la aplicación |

**Nombre del archivo de respaldo:** `escudo_jgp_YYYYMMDD_HHMMSS.jgpbackup`

Para restaurar un respaldo, copia el archivo `.jgpbackup` a la carpeta `backups/` y contacta al administrador del sistema.

---

## 10. JURIS-AI — Asistente Inteligente

Asistente de inteligencia artificial integrado que ayuda a redactar escritos, analizar incidentes procesales y generar borradores jurídicos usando los datos reales del expediente activo.

### Cómo Abrir JURIS-AI

Pulsa el botón **⚖️ JURIS-AI** en la barra superior (esquina derecha). El panel se desliza desde la derecha sin bloquear el área de trabajo principal.

### Cómo Usar JURIS-AI

1. Haz clic sobre un expediente en la tabla (establece el "caso activo").
2. Abre el panel JURIS-AI con el botón del header.
3. Escribe tu consulta en el campo de texto inferior del panel.
4. Presiona **Enter** o el botón **➤** para enviar.
5. JURIS-AI responde usando los datos reales del expediente activo.

### Ejemplos de Consultas

| Consulta | Resultado esperado |
|----------|-------------------|
| `"Redacta un escrito de contestación para el caso 2026-CIV-001"` | Borrador con datos del caso inyectados |
| `"Genera un resumen ejecutivo de este expediente"` | Resumen estructurado |
| `"¿Qué incidentes son comunes en materia laboral?"` | Lista del catálogo integrado |
| `"Dame un borrador de poder especial para el cliente activo"` | Poder con nombre y DNI del cliente |

### Elementos del Panel

| Elemento | Función |
|----------|---------|
| **⚖️ / Imagen del agente** | Identifica al asistente |
| **JURIS-AI / Asistente legal inteligente** | Cabecera del panel |
| **✕ (botón cerrar)** | Cierra el panel sin perder el historial de la sesión |
| **Área de chat** | Historial de la conversación durante la sesión |
| **Campo de texto** | Entrada de consultas en lenguaje natural |
| **Botón ➤** | Envía la consulta (equivalente a **Enter**) |

### Generación de Borradores

Cuando JURIS-AI genera un borrador completo, aparece un botón especial en el chat:

**📄 Abrir Documento Completo en Editor**

Al pulsarlo, el borrador se carga directamente en el Editor de Documentos del expediente activo para su revisión y exportación a Word.

> **Nota:** Para respuestas de IA completas se requiere una API Key configurada en la sección de Configuración. Sin ella, JURIS-AI usa el catálogo de plantillas e incidentes procesales integrado.

> **Nota:** Para que JURIS-AI tenga contexto específico del caso, primero haz clic sobre un expediente en la tabla.

---

## 11. Indicador de Estado del Sistema

Pastilla permanente en la **esquina inferior derecha** de la pantalla.

| Indicador | Significado |
|-----------|-------------|
| **● verde — Escudo de Datos OK** | El sistema de respaldos está activo y operativo |

El respaldo se ejecuta automáticamente al cerrar la aplicación. Contiene la base de datos completa y la configuración del sistema.

---

## 12. Flujo de Trabajo Recomendado

Para gestionar un nuevo caso que llega al despacho, sigue este orden:

### Paso 1 — Registrar al Cliente

```text
Menú: 👥 Clientes
→ Clic en "+ Nuevo Cliente"
→ Llenar: Nombre completo, DNI (obligatorio), teléfono, correo, dirección
→ Clic en "✅ Guardar Cliente"
```

### Paso 2 — Abrir el Expediente

```text
Menú: 📁 Expedientes
→ Clic en "+ Nuevo Expediente"
→ Seleccionar Materia Legal → el ID se genera automáticamente
→ Seleccionar el Cliente registrado en el Paso 1
→ Escribir el Juzgado y la Cuantía/Honorarios (opcional)
→ Clic en "✅ Guardar Expediente"
```

### Paso 3 — Programar la Primera Audiencia

```text
Menú: 📅 Calendario
→ Clic en "+ Programar Audiencia"
→ Seleccionar Tipo de Audiencia
→ Escribir el ID del expediente (ej: 2026-CIV-001)
→ Seleccionar la fecha con el calendario desplegable (formato dd-mm-aaaa)
→ Ajustar la hora en el campo inline
→ Pulsar "Aceptar" para confirmar la fecha
→ Ingresar cuantía / honorarios
→ Clic en "Guardar en Cronograma"
```

### Paso 4 — Consultar JURIS-AI

```text
Header: Botón ⚖️ JURIS-AI
→ El panel se abre desde la derecha
→ Hacer clic sobre el expediente en la tabla primero (contexto activo)
→ Escribir consulta: "Redacta una demanda para el caso 2026-CIV-001"
→ Revisar el borrador generado
→ Pulsar "📄 Abrir Documento Completo en Editor" si el borrador es útil
```

### Paso 5 — Redactar el Primer Escrito

```text
Menú: 📁 Expedientes
→ Clic sobre la fila del caso → se selecciona como caso activo
→ Clic en "📄 Redactar Documento" (en el panel de gestión)
→ Buscar plantilla con el buscador
→ Seleccionar la plantilla del desplegable
→ Clic en "Cargar y Autocompletar"
→ Editar el texto según el caso específico
→ Clic en "📄 Exportar como Word (.docx)"
→ Elegir carpeta de destino en el diálogo del sistema
```

### Paso 6 — Preparar la Audiencia (día anterior)

```text
Menú: 📅 Calendario
→ Localizar la audiencia en la tabla
→ Clic en "📋 Ver Ficha"
→ Revisar las Anotaciones Pre-Audiencia de JURIS-AI
→ Escribir observaciones propias en el campo de texto
→ Clic en "🖨️ Imprimir / PDF" para llevar la ficha
```

### Paso 7 — Actualizar Estado del Caso

```text
Menú: 📁 Expedientes
→ Clic sobre la fila del expediente
→ En el panel de gestión, clic en el estado correspondiente:
   • "🟡 En Proceso" → cuando hay actuaciones activas
   • "🔴 Cerrado"    → cuando el caso concluye
```

### Paso 8 — Revisar el Dashboard

```text
Menú: 📊 Dashboard
→ Verificar que los honorarios proyectados se actualizaron
→ Revisar la distribución de casos en el gráfico de barras
→ Comparar avance contra las metas mensuales
```

---

## 13. Preguntas Frecuentes

**¿Puedo usar el sistema sin internet?**
Sí. JURIS-GESTIÓN-PRO funciona completamente offline. Todos los datos se almacenan localmente.

**¿Dónde se guarda la base de datos?**
En `data/juris_gestion_pro.db` dentro del directorio de instalación. Es un archivo SQLite estándar.

**¿Qué pasa si olvido el PIN?**
Usa el enlace **"¿Olvidó su PIN de Administrador?"** en la pantalla de ingreso de PIN e introduce el código maestro del sistema.

**¿Puedo tener dos clientes con el mismo DNI?**
No. El DNI es único en el sistema. Si un cliente tiene DNI personal y RTN de empresa, regístralo dos veces con los distintos documentos.

**¿El ID del expediente se puede cambiar?**
No. El ID es generado automáticamente y es la llave primaria. Para corregirlo, elimina el expediente y créalo nuevamente.

**¿Cuántos respaldos se guardan?**
Uno por cada cierre de la aplicación, más los generados manualmente. No hay límite. Puedes borrar los más antiguos desde la carpeta `backups/`.

**¿Puedo agregar mis propias plantillas?**
Sí. Crea un archivo `.md` en la carpeta correspondiente dentro de `plantillas/` y el sistema lo detectará al reiniciar.

**¿Cómo agrego una plantilla personalizada?**
1. Crea un archivo de texto con extensión `.md` en la carpeta de la materia (ej: `plantillas/derecho_civil/mi_plantilla.md`).
2. Usa los marcadores: `[NOMBRE_CLIENTE]`, `[DNI_CLIENTE]`, `[TELEFONO]`, `[DOMICILIO_CLIENTE]`, `[JUZGADO CORRESPONDIENTE]`.
3. Reinicia la aplicación. La plantilla aparecerá en el selector del editor.

**¿Los documentos Word generados se pueden editar?**
Sí. El `.docx` generado es compatible con Microsoft Word, LibreOffice Writer y cualquier procesador de texto estándar.

**¿Por qué el gráfico del Dashboard no aparece?**
La librería `chart.js` debe estar en `assets/js/chart.js`. Si no está instalada, el Dashboard muestra las tarjetas de estadística normalmente pero sin el gráfico de barras. El sistema registra un aviso en la consola del desarrollador.

**¿El panel de JURIS-AI guarda el historial entre sesiones?**
No. El historial del chat es temporal (solo dura la sesión actual). Al cerrar y reabrir la aplicación, el chat comienza en blanco.

**¿Cómo limpio datos de prueba?**
Los datos de prueba cargados durante testing se eliminan directamente desde la base de datos SQLite en `data/juris_gestion_pro.db`. La tabla `configuracion` nunca se toca; solo se limpian `clientes`, `expedientes`, `actuaciones` y `protocolo`.

---

## 14. Estructura de Archivos del Sistema

```text
JURIS-GESTIÓN-PRO/
│
├── main.py                          ← Punto de entrada. Ejecutar para iniciar la app
├── MANUAL_DE_USUARIO.md             ← Este documento
│
├── ui/
│   ├── juris_gestion_pro_app.html   ← Interfaz principal (Fluent Design v2.0)
│   └── tutorial.mp4                 ← Video tutorial integrado
│
├── src/
│   ├── database.py                  ← Módulo de base de datos (schema y migraciones)
│   ├── seguridad.py                 ← Módulo del Escudo de Datos (respaldos)
│   └── licencia.py                  ← Módulo de verificación de licencia
│
├── data/
│   ├── juris_gestion_pro.db         ← Base de datos SQLite principal
│   └── licencia.key                 ← Archivo de licencia del sistema
│
├── plantillas/
│   ├── derecho_civil/               ← 12 plantillas de derecho civil
│   ├── derecho_familiar/            ← 5 plantillas de derecho familiar
│   ├── derecho_laboral/             ← 5 plantillas de derecho laboral
│   ├── derecho_mercantil_y_empresarial/  ← 7 plantillas mercantiles
│   ├── derecho_penal_y_administrativo/   ← 6 plantillas penales/administrativas
│   └── otros_formatos_comunes/      ← 9 plantillas de uso general
│
├── assets/
│   ├── js/
│   │   ├── chart.js                 ← Librería de gráficos (instalar para Dashboard)
│   │   └── html2pdf.bundle.min.js  ← Librería de exportación PDF
│   ├── juris_gestion_pro_logo.png   ← Logo por defecto del sistema
│   └── *.png                        ← Recursos gráficos
│
├── config/
│   └── incidentes_procesales.json   ← Catálogo integrado de incidentes procesales
│
├── backups/
│   └── escudo_jgp_YYYYMMDD_HHMMSS.jgpbackup  ← Respaldos automáticos
│
└── build/ · dist/                   ← Archivos de compilación (no modificar)
```

### Tablas de la Base de Datos

| Tabla | Contenido |
|-------|-----------|
| `configuracion` | Datos institucionales, logo, API key, PIN, tema visual |
| `clientes` | Directorio CRM (nombre, DNI, teléfono, correo, dirección) |
| `expedientes` | Casos jurídicos (ID, cliente, materia, juzgado, cuantía, estado) |
| `actuaciones` | Audiencias y plazos (tipo, fecha, expediente, honorarios, observaciones) |
| `protocolo` | Instrumentos notariales (otorgante, acto, folios, fecha) |

---

*JURIS-GESTIÓN-PRO · Manual de Usuario v2.0 · Mayo 2026*
*Desarrollado para despachos jurídicos en Honduras*
