$WebResponse = Invoke-WebRequest "http://127.0.0.1:5000" 
$content = $WebResponse.Content

# Check for connnection
$Code = $WebResponse.StatusCode
$Working = 200
if ($Code -ne 200){
    echo "Fail" $Code
    exit
}
if ($Code -eq $Working){
    echo "Success"
    echo "creating script"
} 

# Create Script
$content = $content | ConvertFrom-Json
$content = "C:\temp\script.ps1"

# Run Script 
$resp = .$content | ConvertTo-Json

# Send results back to URL as Post
Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:5000"  -ContentType "application/json" -Method POST -Body $resp

$Code = $WebResponse.StatusCode
$Working = 200
if ($Code -ne 200){
    echo "Failed to Return" $Code
    exit
}
if ($Code -eq $Working){
    echo "Success"
} 
