using System.ComponentModel.DataAnnotations;

namespace BloodConnect.Models;

// ==================================================
// ==================== DONOR DTOs ==================
// ==================================================

public class DonorDto
{
    public int DonorId { get; set; }
    public string Name { get; set; } = "";
    public string BloodGroup { get; set; } = "";
    public int? Age { get; set; }
    public string? State { get; set; }
    public string? City { get; set; }
    public string Location { get; set; } = "";
    public bool IsAvailable { get; set; }
    public string? ContactNumber { get; set; }  // null in list, value in detail
}

public class CreateDonorDto
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 2)]
    public string Name { get; set; } = "";

    [Required]
    [Range(18, 65, ErrorMessage = "Age must be between 18 and 65")]
    public int Age { get; set; }

    [Required]
    [RegularExpression(DomainValues.BloodGroupPattern,
        ErrorMessage = "Invalid blood group")]
    public string BloodGroup { get; set; } = "";

    [Required]
    [StringLength(100)]
    public string State { get; set; } = "";

    [StringLength(50)]
    public string? City { get; set; }

    [Required]
    [RegularExpression(@"^[0-9]{10}$", ErrorMessage = "Enter 10-digit mobile number")]
    public string ContactNumber { get; set; } = "";

    public bool IsAvailable { get; set; } = true;
}

public class UpdateDonorDto
{
    [Required]
    [StringLength(100, MinimumLength = 2)]
    public string Name { get; set; } = "";

    [Required]
    [Range(18, 65)]
    public int Age { get; set; }

    [Required]
    [RegularExpression(DomainValues.BloodGroupPattern)]
    public string BloodGroup { get; set; } = "";

    [Required]
    [StringLength(100)]
    public string State { get; set; } = "";

    [StringLength(50)]
    public string? City { get; set; }

    [Required]
    [RegularExpression(@"^[0-9]{10}$")]
    public string ContactNumber { get; set; } = "";

    public bool IsAvailable { get; set; } = true;
}

// ==================================================
// ============== BLOOD REQUEST DTOs ================
// ==================================================

public class BloodRequestDto
{
    public int RequestId { get; set; }
    public string RequesterName { get; set; } = "";
    public string BloodGroupNeeded { get; set; } = "";
    public string? State { get; set; }
    public string? City { get; set; }
    public string Location { get; set; } = "";
    public string? ContactNumber { get; set; }
    public string UrgencyLevel { get; set; } = "";
    public string Status { get; set; } = "";
    public DateTime RequestDate { get; set; }
}

public class CreateBloodRequestDto
{
    [Required]
    [StringLength(100)]
    public string RequesterName { get; set; } = "";

    [Required]
    [RegularExpression(DomainValues.BloodGroupPattern)]
    public string BloodGroupNeeded { get; set; } = "";

    [Required]
    [StringLength(100)]
    public string State { get; set; } = "";

    [StringLength(50)]
    public string? City { get; set; }

    [Required]
    [RegularExpression(@"^[0-9]{10}$")]
    public string ContactNumber { get; set; } = "";

    [Required]
    [RegularExpression(DomainValues.UrgencyPattern)]
    public string UrgencyLevel { get; set; } = "";
}

public class UpdateBloodRequestDto
{
    [Required]
    [StringLength(100)]
    public string RequesterName { get; set; } = "";

    [Required]
    [RegularExpression(DomainValues.BloodGroupPattern)]
    public string BloodGroupNeeded { get; set; } = "";

    [Required]
    [StringLength(100)]
    public string State { get; set; } = "";

    [StringLength(50)]
    public string? City { get; set; }

    [Required]
    [RegularExpression(@"^[0-9]{10}$")]
    public string ContactNumber { get; set; } = "";

    [Required]
    [RegularExpression(DomainValues.UrgencyPattern)]
    public string UrgencyLevel { get; set; } = "";
}