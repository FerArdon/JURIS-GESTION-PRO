# ============================================================
#  JURIS GESTIÓN PRO — Descargador masivo de plantillas legales
#  Fer Ardón · SEDCAF · 2026
#  Ejecutar: powershell -ExecutionPolicy Bypass -File descargar_plantillas.ps1
# ============================================================

$PlantillasDir = "C:\Users\frard\Mi unidad\2_Desarrollo_Software_2026\JURIS-GESTION-PRO\plantillas"

function Slugify($text) {
    $s = $text.ToLower()
    $s = $s -replace '[áàäâ]','a' -replace '[éèëê]','e' -replace '[íìïî]','i' -replace '[óòöô]','o' -replace '[úùüû]','u'
    $s = $s -replace '[ñ]','n' -replace '[ç]','c'
    $s = $s -replace '[^a-z0-9\s]','' -replace '\s+','_'
    if ($s.Length -gt 60) { $s = $s.Substring(0, 60) }
    return $s.Trim('_')
}

function GuardarPlantilla($categoria, $titulo, $contenido) {
    $dir = Join-Path $PlantillasDir $categoria
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $filename = Slugify $titulo
    $filepath = Join-Path $dir "$filename.md"
    $md = @"
---
titulo: $titulo
categoria: $categoria
---

# $titulo

$contenido
"@
    [System.IO.File]::WriteAllText($filepath, $md, [System.Text.Encoding]::UTF8)
    Write-Host "  ✅ $titulo" -ForegroundColor Green
}

function DetectarCategoria($titulo) {
    $t = $titulo.ToLower()
    if ($t -match 'laboral|trabajo|patrono|salario|despido|prestacion|sindicato') { return 'derecho_laboral' }
    if ($t -match 'penal|delito|querella|denuncia|imputado|fiscal|casacion') { return 'derecho_penal_y_administrativo' }
    if ($t -match 'mercantil|sociedad|empresa|comercio|franquicia|accion|acta') { return 'derecho_mercantil_y_empresarial' }
    if ($t -match 'familia|divorcio|alimento|custodia|matrimoni|hijo|adopcion|union') { return 'derecho_familiar' }
    if ($t -match 'notari|escritura|protocolo|exequatur|instrumento|tomo') { return 'derecho_notarial' }
    if ($t -match 'civil|contrato|demanda|arrendamiento|compraventa|herencia|testamento|prescripcion') { return 'derecho_civil' }
    return 'otros_formatos_comunes'
}

function ExtraerTextoHtml($html) {
    # Eliminar scripts, estilos y tags HTML
    $texto = $html -replace '<script[^>]*>[\s\S]*?</script>', ''
    $texto = $texto -replace '<style[^>]*>[\s\S]*?</style>', ''
    $texto = $texto -replace '<[^>]+>', ' '
    $texto = $texto -replace '&nbsp;', ' ' -replace '&amp;', '&' -replace '&lt;', '<' -replace '&gt;', '>'
    $texto = $texto -replace '&quot;', '"' -replace '&#[0-9]+;', ''
    $texto = $texto -replace '\s{3,}', "`n`n"
    return $texto.Trim()
}

# ── SITIO 1: Blogspot (Modelos y Formularios Derecho Procesal Honduras) ──────
Write-Host "`n🔵 Descargando de Blogspot..." -ForegroundColor Cyan

$blogUrl = "https://modelosyformulariosdederechoprocesal.blogspot.com"
$contador = 0
$pagina = 1

do {
    try {
        $url = if ($pagina -eq 1) { $blogUrl } else { "$blogUrl/search?updated-max=&max-results=20&start=$(($pagina-1)*20)&by-date=false" }
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
        $html = $resp.Content

        # Extraer links de posts individuales
        $links = [regex]::Matches($html, 'href="(https://modelosyformulariosdederechoprocesal\.blogspot\.com/\d{4}/\d{2}/[^"]+\.html)"') |
                 ForEach-Object { $_.Groups[1].Value } | Select-Object -Unique

        if ($links.Count -eq 0) { break }

        foreach ($link in $links) {
            try {
                $postResp = Invoke-WebRequest -Uri $link -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
                $postHtml = $postResp.Content

                # Extraer título
                $tituloMatch = [regex]::Match($postHtml, '<h3[^>]*class=''post-title[^>]*>(.*?)</h3>', 'IgnoreCase,Singleline')
                if (-not $tituloMatch.Success) {
                    $tituloMatch = [regex]::Match($postHtml, '<title>(.*?)\|', 'IgnoreCase')
                }
                $titulo = if ($tituloMatch.Success) { ([regex]::Replace($tituloMatch.Groups[1].Value, '<[^>]+>', '')).Trim() } else { "Plantilla $contador" }

                # Extraer contenido del post
                $contenidoMatch = [regex]::Match($postHtml, '<div[^>]*class=''post-body[^>]*>([\s\S]*?)</div>\s*<div[^>]*class=''post-footer', 'IgnoreCase')
                if (-not $contenidoMatch.Success) {
                    $contenidoMatch = [regex]::Match($postHtml, '<div[^>]*class=''entry-content[^>]*>([\s\S]*?)</div>', 'IgnoreCase')
                }

                if ($contenidoMatch.Success -and $contenidoMatch.Groups[1].Value.Length -gt 200) {
                    $contenido = ExtraerTextoHtml $contenidoMatch.Groups[1].Value
                    $categoria = DetectarCategoria $titulo
                    GuardarPlantilla $categoria $titulo $contenido
                    $contador++
                }
                Start-Sleep -Milliseconds 500
            } catch { Write-Host "  ⚠️ Error en $link" -ForegroundColor Yellow }
        }
        $pagina++
    } catch { break }
} while ($pagina -le 10)

Write-Host "  📊 Blogspot: $contador plantillas" -ForegroundColor Cyan

# ── SITIO 2: WordPress (Cambio Generacional) ─────────────────────────────────
Write-Host "`n🟣 Descargando de WordPress..." -ForegroundColor Magenta

$wpContador = 0
try {
    $wpResp = Invoke-WebRequest -Uri "https://cambiogeneracional.wordpress.com/formatos/" -UseBasicParsing -TimeoutSec 30
    $wpHtml = $wpResp.Content

    # Extraer todos los links de la página de formatos
    $wpLinks = [regex]::Matches($wpHtml, 'href="(https://cambiogeneracional\.wordpress\.com/[^"#]+)"') |
               ForEach-Object { $_.Groups[1].Value } |
               Where-Object { $_ -notmatch '/formatos/$' -and $_ -notmatch '\.(jpg|png|gif|css|js)' } |
               Select-Object -Unique

    foreach ($link in $wpLinks) {
        try {
            $postResp = Invoke-WebRequest -Uri $link -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
            $postHtml = $postResp.Content

            $tituloMatch = [regex]::Match($postHtml, '<h1[^>]*class=''entry-title[^>]*>(.*?)</h1>', 'IgnoreCase,Singleline')
            if (-not $tituloMatch.Success) {
                $tituloMatch = [regex]::Match($postHtml, '<title>(.*?)[\|\-]', 'IgnoreCase')
            }
            $titulo = if ($tituloMatch.Success) { ([regex]::Replace($tituloMatch.Groups[1].Value, '<[^>]+>', '')).Trim() } else { continue }

            $contenidoMatch = [regex]::Match($postHtml, '<div[^>]*class=''entry-content[^>]*>([\s\S]*?)</div>\s*<footer', 'IgnoreCase')
            if (-not $contenidoMatch.Success) {
                $contenidoMatch = [regex]::Match($postHtml, '<div[^>]*class=''[^"]*post-content[^"]*[^>]*>([\s\S]*?)</div>', 'IgnoreCase')
            }

            if ($contenidoMatch.Success -and $contenidoMatch.Groups[1].Value.Length -gt 200) {
                $contenido = ExtraerTextoHtml $contenidoMatch.Groups[1].Value
                $categoria = DetectarCategoria $titulo
                GuardarPlantilla $categoria $titulo $contenido
                $wpContador++
            }
            Start-Sleep -Milliseconds 500
        } catch { Write-Host "  ⚠️ Error en $link" -ForegroundColor Yellow }
    }
} catch { Write-Host "  ❌ Error accediendo a WordPress" -ForegroundColor Red }

Write-Host "  📊 WordPress: $wpContador plantillas" -ForegroundColor Magenta

# ── SITIO 3: MiDespacho.cloud ─────────────────────────────────────────────────
Write-Host "`n🟢 Descargando de MiDespacho.cloud..." -ForegroundColor Green

$mdContador = 0
try {
    $mdResp = Invoke-WebRequest -Uri "https://app.midespacho.cloud/recursos-legales-gratuitos/formatos-juridicos" -UseBasicParsing -TimeoutSec 30
    $mdHtml = $mdResp.Content

    $mdLinks = [regex]::Matches($mdHtml, 'href="(/recursos-legales-gratuitos/formatos-juridicos/[^"]+)"') |
               ForEach-Object { "https://app.midespacho.cloud" + $_.Groups[1].Value } |
               Select-Object -Unique

    foreach ($link in $mdLinks) {
        try {
            $postResp = Invoke-WebRequest -Uri $link -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
            $postHtml = $postResp.Content

            $tituloMatch = [regex]::Match($postHtml, '<h1[^>]*>(.*?)</h1>', 'IgnoreCase,Singleline')
            $titulo = if ($tituloMatch.Success) { ([regex]::Replace($tituloMatch.Groups[1].Value, '<[^>]+>', '')).Trim() } else { continue }

            $contenidoMatch = [regex]::Match($postHtml, '<div[^>]*class=''[^"]*content[^"]*[^>]*>([\s\S]*?)</div>', 'IgnoreCase')

            if ($contenidoMatch.Success -and $contenidoMatch.Groups[1].Value.Length -gt 200) {
                $contenido = ExtraerTextoHtml $contenidoMatch.Groups[1].Value
                $categoria = DetectarCategoria $titulo
                GuardarPlantilla $categoria $titulo $contenido
                $mdContador++
            }
            Start-Sleep -Milliseconds 300
        } catch { Write-Host "  ⚠️ Error en $link" -ForegroundColor Yellow }
    }
} catch { Write-Host "  ❌ Error accediendo a MiDespacho" -ForegroundColor Red }

Write-Host "  📊 MiDespacho: $mdContador plantillas" -ForegroundColor Green

# ── RESUMEN FINAL ─────────────────────────────────────────────────────────────
$total = (Get-ChildItem $PlantillasDir -Recurse -Filter "*.md").Count
Write-Host "`n============================================================" -ForegroundColor White
Write-Host "  ✅ DESCARGA COMPLETADA" -ForegroundColor White
Write-Host "  📁 Total plantillas en disco: $total" -ForegroundColor White
Write-Host "  📂 Carpeta: $PlantillasDir" -ForegroundColor White
Write-Host "============================================================`n" -ForegroundColor White
