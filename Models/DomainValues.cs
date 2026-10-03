namespace BloodConnect.Models;

public static class DomainValues
{
    public static readonly IReadOnlyList<string> BloodGroups =
        new[] { "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-" };

    public static readonly IReadOnlyList<string> UrgencyLevels =
        new[] { "Low", "Medium", "High", "Critical" };

    // ✅ NEW — 28 States + 8 Union Territories (alphabetical)
    public static readonly IReadOnlyList<string> IndianStates = new[]
    {
        // States
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal",
        // Union Territories
        "Andaman and Nicobar Islands", "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
        "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    };

    // ✅ NEW — server-side check: dropdown ke bahar ki value (hacker/Postman) reject
    public static bool IsValidState(string? state) =>
        !string.IsNullOrWhiteSpace(state) && IndianStates.Contains(state);

    // ✅ NEW — "Surat, Gujarat" format (purane Location column ke liye)
    public static string BuildLocation(string city, string state) =>
        $"{city.Trim()}, {state}";

    public const string BloodGroupPattern = @"^(A|B|AB|O)[+-]$";
    public const string UrgencyPattern = "^(Low|Medium|High|Critical)$";
    public const string StatusPattern = "^(Open|Fulfilled)$";

    // Request status
    public const string Open = "Open";
    public const string Fulfilled = "Fulfilled";

    // ✅ DonationOffer status
    public const string Pledged = "Pledged";
    public const string Accepted = "Accepted";
    public const string Rejected = "Rejected";
    public const string Completed = "Completed";
    public const string Cancelled = "Cancelled";
    public const string OfferStatusPattern = "^(Pledged|Accepted|Rejected|Completed|Cancelled)$";
}