$getPath = Read-Host "What is the path you would like to search?`n"

$files = Get-ChildItem -Path $getPath -Attributes !Directory -Force -Recurse
foreach ($f in $files)
{
    # use '$array += $element' to add item to end of array dynamically
    $alternateData = Get-Item -Path $f.FullName | Get-Item -Stream *
    foreach ($item in $alternateData)
    {
        if ($item.Stream.Contains('DATA') -eq $true){continue}
        Write-Host "Path: " $item.PSPath -ForegroundColor Green 
        Write-Host "Parent Path: " $item.PSParentPath -ForegroundColor Yellow
        Write-Host "PSChildName: " $item.PSChildName -ForegroundColor Yellow 
        Write-Host "PSProvider: " $item.PSProvider -ForegroundColor Yellow
        Write-Host "PSIsContainer: " $item.PSIsContainer -ForegroundColor Yellow
        Write-Host "Filename: " $item.FileName -ForegroundColor Yellow
        Write-Host "Stream: " $item.Stream -ForegroundColor Red
        Write-Host "Length: " $item.Length -ForegroundColor Yellow
        Write-Host "Content:" -ForegroundColor Cyan
        Get-Content -Path $f.FullName -Stream $item.Stream
        Write-Host "`n"
    }
}