namespace BloodConnect.Models;

/// <summary>
/// Blood group compatibility logic.
/// Based on universal donor/receiver rules and antigen compatibility.
/// </summary>
public static class BloodCompatibility
{
    /// <summary>
    /// Given a patient's blood group (the one needed), returns the list of
    /// donor blood groups that can safely donate to that patient.
    /// Example: Patient A+ → donors [O-, O+, A-, A+]
    /// </summary>
    public static IReadOnlyList<string> CompatibleDonorsFor(string patientBloodGroup) =>
        patientBloodGroup switch
        {
            "O-"  => new[] { "O-" },
            "O+"  => new[] { "O-", "O+" },
            "A-"  => new[] { "O-", "A-" },
            "A+"  => new[] { "O-", "O+", "A-", "A+" },
            "B-"  => new[] { "O-", "B-" },
            "B+"  => new[] { "O-", "O+", "B-", "B+" },
            "AB-" => new[] { "O-", "A-", "B-", "AB-" },
            "AB+" => new[] { "O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+" },
            _     => Array.Empty<string>()
        };

    /// <summary>
    /// Given a donor's blood group, returns the list of patient blood groups
    /// that this donor can safely donate to.
    /// Example: Donor O- → patients [all 8 groups]
    /// </summary>
    public static IReadOnlyList<string> CompatiblePatientsFor(string donorBloodGroup) =>
        donorBloodGroup switch
        {
            "O-"  => new[] { "O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+" },
            "O+"  => new[] { "O+", "A+", "B+", "AB+" },
            "A-"  => new[] { "A-", "A+", "AB-", "AB+" },
            "A+"  => new[] { "A+", "AB+" },
            "B-"  => new[] { "B-", "B+", "AB-", "AB+" },
            "B+"  => new[] { "B+", "AB+" },
            "AB-" => new[] { "AB-", "AB+" },
            "AB+" => new[] { "AB+" },
            _     => Array.Empty<string>()
        };

    public static bool IsUniversalDonor(string bloodGroup) => bloodGroup == "O-";
    public static bool IsUniversalReceiver(string bloodGroup) => bloodGroup == "AB+";

    public static bool IsValid(string bloodGroup) =>
        !string.IsNullOrWhiteSpace(bloodGroup) &&
        Array.IndexOf(DomainValues.BloodGroups.ToArray(), bloodGroup) >= 0;

    /// <summary>
    /// Short human-readable description of compatibility for UI display.
    /// </summary>
    public static string DescribeDonorReach(string donorBloodGroup) =>
        donorBloodGroup switch
        {
            "O-"  => "Can donate to all 8 blood groups (Universal Donor)",
            "O+"  => "Can donate to O+, A+, B+, AB+",
            "A-"  => "Can donate to A-, A+, AB-, AB+",
            "A+"  => "Can donate to A+ and AB+",
            "B-"  => "Can donate to B-, B+, AB-, AB+",
            "B+"  => "Can donate to B+ and AB+",
            "AB-" => "Can donate to AB- and AB+",
            "AB+" => "Can donate to AB+ only (Universal Receiver)",
            _     => ""
        };
}