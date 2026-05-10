# Standardize bottom nav across all Treqe pages
$ErrorActionPreference = "Stop"
$base = "C:\Users\Shadow\.openclaw\workspace\treqe-dev-2026\treqe-app\designs"

# Standard nav CSS to insert
$standardNavCSS = @'
    /* ===== BOTTOM NAV ===== */
    .bottom-nav {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: rgba(255,255,255,0.85);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-top: 1px solid var(--border);
      display: flex; justify-content: space-evenly; align-items: center;
      padding: 0; height: 72px; padding-bottom: 12px; z-index: 100; isolation: isolate;
    }
    .nav-item {
      display: flex; flex-direction: column; align-items: center; gap: 2px;
      font-size: 0.65rem; font-weight: 500; color: var(--text-tertiary);
      transition: color 0.2s; padding: 4px 0; flex: 1; max-width: 80px;
      position: relative; border: none; background: none; cursor: pointer;
      font-family: inherit; text-decoration: none;
    }
    .nav-item i { font-size: 1.3rem; }
    .nav-item.active { color: var(--accent); }
    .nav-add { position: relative; top: 0; }
    .nav-add-btn {
      width: 48px; height: 48px; background: var(--accent); color: #FFFFFF;
      border-radius: 50%; display: flex; align-items: center; justify-content: center;
      box-shadow: 0 4px 12px rgba(255,106,53,0.3); margin-bottom: 2px;
    }
    .nav-add-btn i { font-size: 1.1rem; }
    .nav-badge {
      width: 6px; height: 6px; background: var(--accent); border-radius: 50%;
      position: absolute; top: -2px; right: -6px;
    }
'@

# Standard nav HTML template (no active class, sub-page version)
$navHTMLNoActive = @'
  <nav class="bottom-nav">
    <a href="../v1-catalogo/" class="nav-item"><i class="fas fa-search"></i><span>Buscar</span></a>
    <a href="../v12-mis-matches/" class="nav-item"><i class="fas fa-exchange-alt"></i><span>Treqes</span></a>
    <a href="../v3-subir/" class="nav-item nav-add"><div class="nav-add-btn"><i class="fas fa-plus"></i></div></a>
    <a href="../v11-notificaciones/" class="nav-item"><i class="fas fa-bell"></i><span>Avisos</span><span class="nav-badge"></span></a>
    <a href="../v4-perfil/" class="nav-item"><i class="fas fa-user"></i><span>Perfil</span></a>
  </nav>
'@

# Page definitions: path, which item gets active class
$pages = @(
    @{ path="v1-catalogo"; active="buscar" },
    @{ path="v2-detalle"; active="none" },
    @{ path="v3-subir"; active="nav-add" },
    @{ path="v4-perfil"; active="perfil" },
    @{ path="v7-seguimiento"; active="none" },
    @{ path="v11-notificaciones"; active="avisos" },
    @{ path="v12-mis-matches"; active="treqes" },
    @{ path="v13-favoritos"; active="none" },
    @{ path="v14-editar-perfil"; active="none" },
    @{ path="v15-verificar-identidad"; active="none" },
    @{ path="v16-portada"; active="none" },
    @{ path="v8-ajustes"; active="perfil" }
)

function Get-NavHTML {
    param([string]$Active)
    $lines = @(
        '  <nav class="bottom-nav">',
        '    <a href="../v1-catalogo/" class="nav-item' + $(if ($Active -eq "buscar") { ' active' } else { '' }) + '"><i class="fas fa-search"></i><span>Buscar</span></a>',
        '    <a href="../v12-mis-matches/" class="nav-item' + $(if ($Active -eq "treqes") { ' active' } else { '' }) + '"><i class="fas fa-exchange-alt"></i><span>Treqes</span></a>',
        '    <a href="../v3-subir/" class="nav-item nav-add' + $(if ($Active -eq "nav-add") { ' active' } else { '' }) + '"><div class="nav-add-btn"><i class="fas fa-plus"></i></div></a>',
        '    <a href="../v11-notificaciones/" class="nav-item' + $(if ($Active -eq "avisos") { ' active' } else { '' }) + '"><i class="fas fa-bell"></i><span>Avisos</span><span class="nav-badge"></span></a>',
        '    <a href="../v4-perfil/" class="nav-item' + $(if ($Active -eq "perfil") { ' active' } else { '' }) + '"><i class="fas fa-user"></i><span>Perfil</span></a>',
        '  </nav>'
    )
    return ($lines -join "`n")
}

function Remove-NavCSSBlock {
    param([string]$content)
    # Remove all existing nav-related CSS blocks
    # Pattern 1: /* ===== BOTTOM NAV ===== */ through the end of nav-badge or similar
    # Use regex to remove everything from ".bottom-nav" to the closing "}" of nav-badge block
    
    # First, remove any comment block before nav CSS
    $content = $content -replace '(?s)\s*/\* =+\s*BOTTOM NAV\s*=+\s*\*/\s*', "`n`n"
    
    # Remove .bottom-nav { ... } block (multiline)
    $content = $content -replace '(?s)\s*\.bottom-nav\s*\{[^}]*position:\s*fixed[^}]*z-index:\s*\d+[^}]*isolate;?\s*\}', ""
    
    # Remove .nav-item { ... } blocks (multiline - these appear BEFORE .bottom-nav in some files)
    $content = $content -replace '(?s)\s*\.nav-item\s*\{[^}]*display:\s*flex;[^}]*flex-direction:\s*column[^}]*position:\s*relative;?\s*\}', ""
    
    # Remove .nav-item i { ... }
    $content = $content -replace '(?s)\s*\.nav-item\s+i\s*\{[^}]*font-size:\s*1\.[23]rem[^}]*\}', ""
    
    # Remove .nav-item.active { ... }
    $content = $content -replace '(?s)\s*\.nav-item\.active\s*\{[^}]*color:\s*var\(--accent\)[^}]*\}', ""
    # Remove .nav-item.active i { ... }
    $content = $content -replace '(?s)\s*\.nav-item\.active\s+i\s*\{[^}]*\}', ""
    
    # Remove .nav-item .nav-badge { ... }
    $content = $content -replace '(?s)\s*\.nav-item\s+\.nav-badge\s*\{[^}]*\}', ""
    $content = $content -replace '(?s)\s*\.nav-item\s*\.nav-badge\s*\{[^}]*\}', ""
    
    # Remove .nav-item.nav-add { ... }
    $content = $content -replace '(?s)\s*\.nav-item\.nav-add\s*\{[^}]*\}', ""
    
    # Remove .nav-item.nav-add .nav-add-btn { ... }
    $content = $content -replace '(?s)\s*\.nav-item\.nav-add\s+\.nav-add-btn\s*\{[^}]*\}', ""
    $content = $content -replace '(?s)\s*\.nav-item\.nav-add\s+\.nav-add-btn:active\s*\{[^}]*\}', ""
    
    # Remove .nav-add { ... }
    $content = $content -replace '(?s)\s*\.nav-add\s*\{[^}]*position:\s*relative[^}]*\}', ""
    
    # Remove .nav-add-btn { ... }
    $content = $content -replace '(?s)\s*\.nav-add-btn\s*\{[^}]*width:\s*48px[^}]*\}', ""
    $content = $content -replace '(?s)\s*\.nav-add-btn\s+i\s*\{[^}]*\}', ""
    
    # Remove .nav-badge { ... }
    $content = $content -replace '(?s)\s*\.nav-badge\s*\{[^}]*width:\s*6px[^}]*\}', ""
    
    # Remove .nav-add.active .nav-add-btn { ... } (v3-subir specific)
    $content = $content -replace '(?s)\s*\.nav-add\.active\s+\.nav-add-btn\s*\{[^}]*\}', ""
    
    # Remove .nav-plus blocks
    $content = $content -replace '(?s)\s*\.nav-plus[^}]*\{[^}]*\}', ""
    
    # Clean up excessive blank lines (max 2 consecutive)
    $content = $content -replace "`n`n`n`n+", "`n`n`n"
    
    return $content
}

function Replace-NavHTML {
    param([string]$content, [string]$newHTML)
    # Remove existing nav HTML block (handle both <a> and <button> variants)
    # Pattern: <nav class="bottom-nav"> ... </nav>
    $content = $content -replace '(?s)\s*<nav class="bottom-nav">.*?</nav>', ""
    # Clean up multiple blank lines
    $content = $content -replace "`n`n`n`n+", "`n`n`n"
    # Insert new nav before </body>
    $content = $content -replace '(?s)(\s*)</body>', "`n$newHTML`n`n`$1</body>"
    return $content
}

function Ensure-PaddingBottom {
    param([string]$content)
    # If padding-bottom is present but not 80px, fix it
    if ($content -match 'padding-bottom:\s*(\d+)px') {
        $current = $matches[1]
        if ($current -ne "80") {
            $content = $content -replace 'padding-bottom:\s*\d+px', 'padding-bottom: 80px'
        }
    }
    return $content
}

function Insert-NavCSS {
    param([string]$content)
    # Insert standard nav CSS before the closing </style> tag
    $content = $content -replace '(?s)(\s*)</style>', "`n$standardNavCSS`n`$1</style>"
    return $content
}

# Process each page
foreach ($page in $pages) {
    $filePath = Join-Path $base "$($page.path)\index.html"
    if (-not (Test-Path $filePath)) {
        Write-Host "SKIP: $filePath not found" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "Processing: $($page.path) (active=$($page.active))" -ForegroundColor Cyan
    
    $content = Get-Content $filePath -Raw -Encoding UTF8
    
    # Step 1: Remove existing nav CSS
    $content = Remove-NavCSSBlock -content $content
    
    # Step 2: Insert standard nav CSS
    $content = Insert-NavCSS -content $content
    
    # Step 3: Replace nav HTML
    $navHTML = Get-NavHTML -Active $page.active
    $content = Replace-NavHTML -content $content -newHTML $navHTML
    
    # Step 4: Ensure padding-bottom
    $content = Ensure-PaddingBottom -content $content
    
    # Write back
    Set-Content $filePath -Value $content -Encoding UTF8 -NoNewline
    
    Write-Host "  Done: $($page.path)" -ForegroundColor Green
}

Write-Host "`nAll pages standardized!" -ForegroundColor Green
