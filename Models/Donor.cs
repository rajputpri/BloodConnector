using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BloodConnect.Models;

public class Donor
{
    [Key]
    public int DonorId { get; set; }

    // ✅ NEW: Link to Identity user (nullable — purane donors ke liye)
    public string? UserId { get; set; }

    [ForeignKey(nameof(UserId))]
    public AppUser? User { get; set; }

    [Required, StringLength(100)]
    public string Name { get; set; } = "";

    [Required, StringLength(3), Display(Name = "Blood group")]
    [RegularExpression(DomainValues.BloodGroupPattern,
        ErrorMessage = "Select a valid blood group.")]
    public string BloodGroup { get; set; } = "";

    [Required, StringLength(100)]
    public string Location { get; set; } = "";

    [Required, StringLength(10), Display(Name = "Contact number")]
    [RegularExpression(@"^[0-9]{10}$",
        ErrorMessage = "Enter a valid 10-digit number.")]
    public string ContactNumber { get; set; } = "";

    [Display(Name = "Available to donate")]
    public bool IsAvailable { get; set; } = true;

    [Timestamp]
    public byte[] RowVersion { get; set; } = [];
}