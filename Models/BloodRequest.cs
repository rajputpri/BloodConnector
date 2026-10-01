using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BloodConnect.Models;

public class BloodRequest
{
    [Key]
    public int RequestId { get; set; }

    // Owner
    public string? UserId { get; set; }

    [ForeignKey(nameof(UserId))]
    public AppUser? User { get; set; }

    [Required(ErrorMessage = "Requester name is required")]
    [StringLength(100)]
    public string RequesterName { get; set; } = "";

    [Required(ErrorMessage = "Blood group needed is required")]
    [RegularExpression(DomainValues.BloodGroupPattern,
        ErrorMessage = "Select a valid blood group.")]
    public string BloodGroupNeeded { get; set; } = "";

    [Required(ErrorMessage = "Location is required")]
    [StringLength(100)]
    public string Location { get; set; } = "";

    [Required(ErrorMessage = "Contact number is required")]
    [RegularExpression(@"^[0-9]{10}$",
        ErrorMessage = "Enter a valid 10-digit number")]
    public string ContactNumber { get; set; } = "";

    [Required(ErrorMessage = "Urgency level is required")]
    [RegularExpression(DomainValues.UrgencyPattern,
        ErrorMessage = "Select a valid urgency level.")]
    public string UrgencyLevel { get; set; } = "";

    [RegularExpression(DomainValues.StatusPattern,
        ErrorMessage = "Status must be Open or Fulfilled.")]
    public string Status { get; set; } = DomainValues.Open;

    public DateTime RequestDate { get; set; } = DateTime.UtcNow;

    // Fulfilled info
    public int? FulfilledByDonorId { get; set; }
    public Donor? FulfilledByDonor { get; set; }

    // ✅ NEW — offers on this request
    public ICollection<DonationOffer> Offers { get; set; } = new List<DonationOffer>();
}