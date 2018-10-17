param (
    [string]$path = ".\",
    [string]$output,
    [switch]$recurse = $false,
    [switch]$dl,
    [switch]$h
)

if ($h) {
    Write-Host "Usage: .\ads-reporter.ps1 <path_to_directory> -output <output_file> -recurse -dl"
    Write-Host "          -recurse will recursively check through all subdirectories for ads"
    Write-Host "          -dl will only search for ADS where 'ZoneId=3' to reconstruct an internet download history within the directory"
    exit
}
# set file name if output filename given
if ($output) { $json_file = '.\'+$output+'.json' }

# get list of files (uses recursion if option set)
if ($recurse) { $files = Get-ChildItem -LiteralPath $path -Attributes !Directory -Force -Recurse | Sort-Object -Property CreationTimeUtc}
else { $files = Get-ChildItem -LiteralPath $path -Attributes !Directory -Force | Sort-Object -Property CreationTimeUtc}


### this function takes a list of files and returns a hash of all ads items from that list
function getAllADS ($files)
{
    $adsMap = [ordered]@{}

    foreach ($f in $files) {
        # initalise hashmap
        $adsMap[$f]=@()
    
        # get all data streams -- somehow this actually gets all ads per file
        $alternateData = Get-Item -Path $f.FullName -Force | Get-Item -Stream *  -Force
        
        foreach ($item in $alternateData) {
            if ($item.Stream.Contains('DATA') -eq $true){continue}
            $adsMap[$f] += $item
        }
    }
    return $adsMap
}

### this function returns a hashmap of all ads items where ZoneId=3
Function getDLHistory($adsMap)
{
    $dlMap = [ordered]@{}
    foreach($file in $adsMap.Keys) {
        $dlMap[$file] = @()
        foreach($ads in $adsMap[$file]) {
            $content = Get-Content -Path $file.FullName -Stream $ads.Stream
            if($content.Contains("ZoneId=3")) {
                $dlMap[$file] += $ads
            }
        }
    }
    return $dlMap
}

# dumps ads information to screen
function writeADSToScreen($adsMap)
{
    foreach($key in $adsMap.Keys)
    {
        foreach($item in $adsMap[$key]) {
        Write-Host "Path: " $item.PSPath -ForegroundColor Green
        Write-Host "Creation Date: " $key.CreationTimeUtc  -ForegroundColor Green
        Write-Host "PSChildName: " $item.PSChildName -ForegroundColor Red
        Write-Host "Parent Path: " $item.PSParentPath -ForegroundColor Yellow
        Write-Host "Filename: " $item.FileName -ForegroundColor Yellow
        Write-Host "Length: " $item.Length -ForegroundColor Yellow
        Write-Host "Content:" -ForegroundColor Cyan
        Get-Content -Path $key.FullName -Stream $item.Stream
        Write-Host "`n"
        }
    }
}

# takes hash of ads and returns json report style hash
function getJsonOutput($adsMap)
{
    $jsonOutput = [ordered]@{}
    foreach($key in $adsMap.Keys)
    {
        foreach($item in $adsMap[$key]) {
            $jsonOutput[$key.FullName + $item.Stream.ToString()] += @{  "File Name" = $key.Name
                                                                        "Creation Date UTC" = $key.CreationTimeUTC.DateTime
                                                                        "ADS Stream" = $item.Stream
                                                                     }
        }
    }
    return $jsonOutput
}



$adsMap = getALLADS($files)

if ($output) {
    if ($dl) { 
        $dlmap = getDLHistory($adsMap);
        $jsonOutput = getJsonOutput($dlmap)
        Write-Output $jsonOutput | ConvertTo-Json | Out-File $json_file -Encoding utf8
    } else {
        $jsonOutput = getJsonOutput($adsMap)
        Write-Output $jsonOutput | ConvertTo-Json | Out-File $json_file -Encoding utf8
    }
} else {
    if ($dl) {
        $dlmap = getDLHistory($adsMap);
        writeADSToScreen($dlmap)
    } else {
        writeADSToScreen($adsMap)
    }
}
