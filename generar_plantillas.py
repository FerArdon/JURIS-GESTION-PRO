import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANTILLAS_DIR = os.path.join(BASE_DIR, 'plantillas')

if not os.path.exists(PLANTILLAS_DIR):
    os.makedirs(PLANTILLAS_DIR)

# Diccionario de todas las plantillas solicitadas por categoría
plantillas = {
    "Derecho Civil": [
        "Demanda por procedimiento abreviado",
        "Solicitud de comunicación subsidiaria",
        "Manifestación en materia civil",
        "Acuerdo de partición de bienes",
        "Escritura de constitución de patrimonio familiar",
        "Solicitud de constitución de patrimonio familiar",
        "Contrato de arrendamiento de vivienda habitacion bienes muebles rustico",
        "Contrato de opción de compra",
        "Contrato de compraventa de bienes o empresa",
        "Contrato de transporte de mercancías por carretera",
        "Contrato de fianza",
        "Testamento abierto y testamento cerrado"
    ],
    "Derecho Familiar": [
        "Convenio regulador para divorcio o separación de mutuo acuerdo",
        "Autorización de madre o padre para solicitud de pasaporte de menores",
        "Acta de reconocimiento de hijos",
        "Solicitud de alimentos y custodia",
        "Acuerdo de convivencia o separación"
    ],
    "Derecho Laboral": [
        "Contrato individual de trabajo",
        "Reglamento interno de conducta para empleados",
        "Carta de renuncia o despido",
        "Convenio de terminación laboral",
        "Acta de junta general para aprobacion de fusion o reorganizacion empresarial"
    ],
    "Derecho Mercantil y Empresarial": [
        "Contrato de franquicia",
        "Contrato de licencia de uso de patentes y modelos de utilidad",
        "Contrato de cesión de patentes modelos y diseños industriales",
        "Contrato de compraventa de empresa",
        "Acta constitutiva de sociedad mercantil",
        "Estatutos sociales y poderes notariales",
        "Contrato de representación comercial"
    ],
    "Derecho Penal y Administrativo": [
        "Denuncia penal y querella",
        "Solicitud de medidas cautelares",
        "Escrito de defensa o contestación de demanda penal",
        "Solicitud de revisión de sentencia",
        "Recurso de apelación o amparo",
        "Solicitud de habilitación de días y horas inhábiles"
    ],
    "Otros formatos comunes": [
        "Poder general y especial",
        "Carta poder simple",
        "Declaración jurada",
        "Solicitud de apostilla o legalización de documentos",
        "Acta notarial de hechos",
        "Contrato de préstamo o mutuo",
        "Contrato de donación",
        "Contrato de comodato",
        "Contrato de arrendamiento rústico o urbano"
    ]
}

def clean_filename(name):
    # Crear un nombre de archivo seguro eliminando caracteres extraños
    keepcharacters = (' ', '.', '_', '-')
    filename = "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()
    return filename.replace(" ", "_").lower()

def generate_markdown(categoria, nombre):
    # Generar el esqueleto base en Markdown con las etiquetas requeridas por JURIS-AI
    md = f"""# {nombre.upper()}

**A QUIEN CORRESPONDA / JUZGADO CORRESPONDIENTE**

Yo, **[NOMBRE_ABOGADO]**, mayor de edad, [ESTADO_CIVIL], Abogado(a), inscrito en el Colegio de Abogados de Honduras bajo el número **[NUMERO_COLEGIO]**, con despacho profesional en [DIRECCION_DESPACHO], teléfono [TELEFONO] y correo electrónico [CORREO]...

*(Esta plantilla ha sido clasificada en: **{categoria}** y generada por JURIS-GESTIÓN-PRO. Está optimizada para que JURIS-AI la autocomplete en base al expediente de **[NOMBRE_CLIENTE]**)*

## HECHOS / CLÁUSULAS

**PRIMERO:** Que en fecha [FECHA_HECHO], las partes / mi representado(a) acordaron/sufrieron...

**SEGUNDO:** Que...

## FUNDAMENTOS DE DERECHO

Se fundamenta el presente instrumento legal en las disposiciones vigentes en la República de Honduras aplicables a la materia de {categoria}, así como en las normas procesales pertinentes.

## PETICIÓN / ACUERDO

Al Honorable Juzgado o Entidad, respetuosamente **PIDO/ACORDAMOS:**
1. Admitir y dar trámite a la presente.
2. [OBJETIVO_PRINCIPAL].

Tegucigalpa, M.D.C. (O ciudad correspondiente), a los [DIA] días del mes de [MES] del año [ANIO].

___________________________________
**Abg. [NOMBRE_ABOGADO]**
Carné No. [NUMERO_COLEGIO]
"""
    return md

def procesar():
    total = 0
    for categoria, lista in plantillas.items():
        cat_dir = os.path.join(PLANTILLAS_DIR, clean_filename(categoria))
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)
            
        for nombre in lista:
            fname = clean_filename(nombre) + ".md"
            fpath = os.path.join(cat_dir, fname)
            # Solo crear si no existe para no sobrescribir trabajo previo (como la demanda abreviada)
            if not os.path.exists(fpath):
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(generate_markdown(categoria, nombre))
            total += 1
            
    print(f"✅ ¡Éxito! Se generaron/verificaron {total} plantillas en la biblioteca local: {PLANTILLAS_DIR}")

if __name__ == '__main__':
    procesar()
