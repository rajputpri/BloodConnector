namespace BloodConnect.Models;

public static class DomainValues
{
    public static readonly IReadOnlyList<string> BloodGroups =
        new[] { "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-" };

    public static readonly IReadOnlyList<string> UrgencyLevels =
        new[] { "Low", "Medium", "High", "Critical" };

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