using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BloodConnect.Models;

public class Donor
{
    [Key]
    public int DonorId { get; set; }

    public string? UserId { get; set; }

    [ForeignKey(nameof(UserId))]
    public AppUser? User { get; set; }

    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 2,
        ErrorMessage = "Name must be 2-100 characters")]
    public string Name { get; set; } = "";

    // ✅ Nullable — purane donors NULL allowed, naye donors ke liye controller me mandatory check
    [Range(18, 65, ErrorMessage = "Donor age must be between 18 and 65 years")]
    public int? Age { get; set; }

    [Required(ErrorMessage = "Blood group is required")]
    [RegularExpression(DomainValues.BloodGroupPattern,
        ErrorMessage = "Select a valid blood group")]
    public string BloodGroup { get; set; } = "";

    // Location ab AUTO-BANTA hai ("City, State") controller me — form me input nahi hai.
    // Purane pages/API isi column ko padhte hain, isliye isko rakha hai.
    [Required(ErrorMessage = "Location is required")]
    [StringLength(100, MinimumLength = 2,
        ErrorMessage = "Location must be 2-100 characters")]
    public string Location { get; set; } = "";

    // ✅ NEW — dropdown se aata hai. Nullable: purane donors ke liye (controller me mandatory check)
    [StringLength(50)]
    public string? State { get; set; }

    // ✅ NEW — free text city
    [StringLength(50, MinimumLength = 2,
        ErrorMessage = "City must be 2-50 characters")]
    public string? City { get; set; }

    [Required(ErrorMessage = "Contact number is required")]
    [RegularExpression(@"^[0-9]{10}$",
        ErrorMessage = "Enter a valid 10-digit number")]
    public string ContactNumber { get; set; } = "";

    public bool IsAvailable { get; set; } = true;

    // ✅ FIXED — non-nullable (SQL Server rowversion always NOT NULL)
    [Timestamp]
    public byte[] RowVersion { get; set; } = Array.Empty<byte>();
}