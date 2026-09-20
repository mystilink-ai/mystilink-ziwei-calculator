using System;
using System.Diagnostics;
using System.Text;

namespace Mystilink.Ziwei
{
    /// <summary>
    /// Thin CLI wrapper. Requires mystilink-ziwei on PATH or MYSTILINK_ZIWEI_CLI.
    /// </summary>
    public static class ZiweiCalculator
    {
        private static string CliPath()
        {
            var env = Environment.GetEnvironmentVariable("MYSTILINK_ZIWEI_CLI");
            return string.IsNullOrWhiteSpace(env) ? "ziwei" : env;
        }

        private static string Run(string arguments)
        {
            var psi = new ProcessStartInfo
            {
                FileName = CliPath(),
                Arguments = arguments,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8,
            };
            using var proc = Process.Start(psi)
                ?? throw new InvalidOperationException("failed to start ziwei");
            string stdout = proc.StandardOutput.ReadToEnd();
            string stderr = proc.StandardError.ReadToEnd();
            proc.WaitForExit();
            if (proc.ExitCode != 0)
            {
                throw new InvalidOperationException(
                    string.IsNullOrWhiteSpace(stderr) ? stdout : stderr);
            }
            return stdout;
        }

        public static string Chart(
            string datetime,
            string timezone,
            string gender,
            string midnightZi = "same-day",
            bool siHua = false,
            int? year = null,
            double? longitude = null)
        {
            var args = new StringBuilder();
            args.Append("chart");
            args.Append(" --datetime \"").Append(datetime).Append('"');
            args.Append(" --timezone \"").Append(timezone).Append('"');
            args.Append(" --gender ").Append(gender);
            args.Append(" --midnight-zi ").Append(midnightZi);
            if (siHua) args.Append(" --si-hua");
            if (year.HasValue) args.Append(" --year ").Append(year.Value);
            if (longitude.HasValue)
            {
                args.Append(" --longitude ").Append(
                    longitude.Value.ToString(System.Globalization.CultureInfo.InvariantCulture));
            }
            return Run(args.ToString());
        }

        public static string Version() => Run("version");
    }
}
