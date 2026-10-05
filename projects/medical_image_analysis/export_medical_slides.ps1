$pptx = "C:\Users\panka\.gemini\antigravity\scratch\medical_image_analysis\MedVision_AI_Executive_Medical_Presentation.pptx"
$outDir = "C:\Users\panka\.gemini\antigravity\scratch\medical_image_analysis\slides_png"

if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptx, 1, 0, 0)
    $pres.SaveAs($outDir, 17) # 17 = ppSaveAsPNG
    $pres.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    Write-Output "SUCCESS: Medical presentation slides exported to $outDir"
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}
