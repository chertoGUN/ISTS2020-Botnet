# contact Web server

$URL    = 'http://127.0.0.1:5000/'
$webRequest  = [system.Net.WebRequest]::Create($URL)

try {
    $res = $webRequest.GetResponse()
} 
catch [System.Net.WebException] {
    $res = $_.Exception.Response
}

$Code = [int]$res.StatusCode
$Working = 200
if ($Code -ne 200){
    echo "Fail" $Code
}
if ($Code -eq $Working){
    echo "Success"
}

# request.ContentType = "application/json; charset=utf-8"


