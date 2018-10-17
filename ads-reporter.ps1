param (
    [string]$path = ".\",
    [switch]$recurse = $false
)
#$getPath = Read-Host "What is the path you would like to search?`n"
$adsMap = @{}
if ($recurse) { $files = Get-ChildItem -Path $path -Attributes !Directory -Force -Recurse }
else { $files = Get-ChildItem -Path $path -Attributes !Directory -Force }
foreach ($f in $files)
{
    # initalise hashmap
    $adsMap[$f]=@()

    # get all data streams -- somehow this actually gets all ads per file
    $alternateData = Get-Item -Path $f.FullName | Get-Item -Stream *
    
    foreach ($item in $alternateData)
    {
        if ($item.Stream.Contains('DATA') -eq $true){continue}
        $adsMap[$f] += $item

    }
}

foreach($key in $adsMap.Keys)
{
    foreach($item in $adsMap[$key])
    {
        Write-Host "Path: " $item.PSPath -ForegroundColor Green
        Write-Host "Creation Date: " $key.CreationTimeUtc  -ForegroundColor Green
        Write-Host "Parent Path: " $item.PSParentPath -ForegroundColor Yellow
        Write-Host "PSChildName: " $item.PSChildName -ForegroundColor Yellow 
        Write-Host "PSProvider: " $item.PSProvider -ForegroundColor Yellow
        Write-Host "PSIsContainer: " $item.PSIsContainer -ForegroundColor Yellow
        Write-Host "Filename: " $item.FileName -ForegroundColor Yellow
        Write-Host "Stream: " $item.Stream -ForegroundColor Red
        Write-Host "Length: " $item.Length -ForegroundColor Yellow
        Write-Host "Content:" -ForegroundColor Cyan
        Get-Content -Path $key.FullName -Stream $item.Stream
        Write-Host "`n"
    }
}