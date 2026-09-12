// Minimal C# example. Compile with bindings/csharp/ZiweiCalculator.cs
using System;
using Mystilink.Ziwei;

class Program
{
    static void Main()
    {
        string json = ZiweiCalculator.Chart(
            "1990-05-15 14:30",
            "Asia/Shanghai",
            "male",
            "same-day",
            true,
            2026,
            121.5);
        Console.WriteLine(json);
    }
}
