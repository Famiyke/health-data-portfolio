using System.Text.Json;
using Microsoft.AnalysisServices.AdomdClient;
using Microsoft.AnalysisServices.Tabular;

if (args.Length != 3) throw new ArgumentException("Use: port expected-model.json evidence-directory");
var port = int.Parse(args[0]);
using var expectedFile = JsonDocument.Parse(File.ReadAllText(args[1]));
var expected = expectedFile.RootElement;
var evidence = args[2];
Directory.CreateDirectory(evidence);
var address = $"localhost:{port}";
using var server = new Server();
server.Connect(address);
var database = server.Databases.Cast<Database>().Single(db => expected.EnumerateObject().All(t => db.Model.Tables.Any(modelTable => modelTable.Name == t.Name)));
Console.WriteLine($"Connected to the running Desktop model ({database.Model.Tables.Count} tables)");

bool MatchNumber(double actual, double target) => Math.Abs(actual - target) <= 1e-8 * Math.Max(1, Math.Abs(target));

Dictionary<string, object> VerifyData()
{
    var result = new Dictionary<string, object>();
    using var connection = new AdomdConnection($"Data Source={address};Initial Catalog={database.Name}");
    connection.Open();
    foreach (var table in expected.EnumerateObject())
    {
        var modelTable = table.Value;
        var rows = modelTable.GetProperty("rows").EnumerateArray().ToDictionary(row => (row[0].GetString()!, row[1].GetString()!));
        using var command = connection.CreateCommand();
        command.CommandTimeout = 120;
        command.CommandText = $"EVALUATE SELECTCOLUMNS('{table.Name}', \"Period\", '{table.Name}'[Period], \"Category\", '{table.Name}'[Category], \"Value\", '{table.Name}'[Value], \"Status\", '{table.Name}'[Status], \"SourceReference\", '{table.Name}'[SourceReference], \"Unit\", '{table.Name}'[Unit])";
        int count = 0;
        using (var reader = command.ExecuteReader())
        {
            while (reader.Read())
            {
                var key = (reader.GetString(0), reader.GetString(1));
                if (!rows.Remove(key, out var reference)) throw new InvalidOperationException($"Unexpected duplicate or key in {table.Name}: {key}");
                if (reference[2].ValueKind == JsonValueKind.Null)
                {
                    if (!reader.IsDBNull(2)) throw new InvalidOperationException($"Expected blank in {table.Name}: {key}");
                }
                else if (reader.IsDBNull(2) || !MatchNumber(Convert.ToDouble(reader.GetValue(2)), reference[2].GetDouble()))
                    throw new InvalidOperationException($"Value differs in {table.Name}: {key}");
                for (int i = 3; i < 6; i++)
                {
                    if (reader.IsDBNull(i) || reader.GetString(i) != reference[i].GetString()) throw new InvalidOperationException($"Source metadata differs in {table.Name}: {key}");
                }
                count++;
            }
        }
        if (rows.Count > 0) throw new InvalidOperationException($"{table.Name} has {rows.Count} missing model rows.");
        // Check a published latest-period result through the exact measure used by the chart.
        var published = modelTable.GetProperty("rows").EnumerateArray().Where(r => r[2].ValueKind == JsonValueKind.Number).OrderByDescending(r => r[0].GetString(), StringComparer.Ordinal).First();
        string Escape(string s) => s.Replace("\"", "\"\"");
        var period = Escape(published[0].GetString()!);
        var category = Escape(published[1].GetString()!);
        var measure = modelTable.GetProperty("measure").GetString();
        command.CommandText = $"EVALUATE ROW(\"Latest\", CALCULATE([{measure}], '{table.Name}'[Period] = \"{period}\", '{table.Name}'[Category] = \"{category}\"))";
        using (var reader = command.ExecuteReader())
        {
            if (!reader.Read() || reader.IsDBNull(0) || !MatchNumber(Convert.ToDouble(reader.GetValue(0)), published[2].GetDouble())) throw new InvalidOperationException($"Measure did not match {table.Name}: {measure}");
            result[table.Name] = new { rows = count, measure, selected_period=published[0].GetString(), selected_category=published[1].GetString(), value=Convert.ToDouble(reader.GetValue(0)) };
        }
        Console.WriteLine($"PASS {table.Name}: {count} rows, source metadata and chart measure verified");
    }
    return result;
}
Dictionary<string, object>? results = null;
try { results = VerifyData(); }
catch (Exception ex)
{
    Console.WriteLine($"Initial native model check: {ex.Message}");
    database.Model.RequestRefresh(RefreshType.Full);
    database.Model.SaveChanges();
    Console.WriteLine("Native Analysis Services model refresh finished");
    results = VerifyData();
}
File.WriteAllText(Path.Combine(evidence, "native-dax-results.json"), System.Text.Json.JsonSerializer.Serialize(results, new JsonSerializerOptions { WriteIndented=true }));
Console.WriteLine("PASS: All six native model tables and six chart measures verified.");
server.Disconnect();
