param (
    [string]$path = ".\",
    [string]$output,
    [switch]$recurse = $false
)

$adsMap = @{}

# set file name if output filename given
if ($output) { $json_file = '.\'+$output+'.json' }

# get list of files (uses recursion if option set)
if ($recurse) { $files = Get-ChildItem -Path $path -Attributes !Directory -Force -Recurse }
else { $files = Get-ChildItem -Path $path -Attributes !Directory -Force }

foreach ($f in $files)
{
    # initalise hashmap
    $adsMap[$f]=@()

    # get all data streams -- somehow this actually gets all ads per file
    $alternateData = Get-Item -Path $f.FullName | Get-Item -Stream *
    
    foreach ($item in $alternateData) {
        if ($item.Stream.Contains('DATA') -eq $true){continue}
        $adsMap[$f] += $item
    }
}

$jsonOutput = @{}
foreach($key in $adsMap.Keys)
{
    foreach($item in $adsMap[$key]) {
        if (!$output) {
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
        else {
            $jsonOutput[$key.FullName + $item.Stream.ToString()] += @{ "File Name" = $key.Name
            "Creation Date UTC" = $key.CreationTimeUTC.DateTime
                                            "ADS Stream" = $item.Stream
                                           }
        }
    }
}

#foreach( $item in $jsonOutput.GetEnumerator() | Sort -Property "Creation Date UTC"
if ($output) { Write-Output $jsonOutput | ConvertTo-Json | File $json_file}