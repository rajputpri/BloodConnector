using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace BloodConnect.Models;

public class DonationOffer
{
    [Key]
    public int Id { get; set; }

    // ----- Request (kis request pe offer) -----
    public int RequestId { get; set; }

    [ForeignKey(nameof(RequestId))]
    public BloodRequest Request { get; set; } = null!;

    // ----- Donor (kisne offer kiya) -----
    public int DonorId { get; set; }

    [ForeignKey(nameof(DonorId))]
    public Donor Donor { get; set; } = null!;

    // ----- State -----
    [Required]
    [RegularExpression(DomainValues.OfferStatusPattern,
        ErrorMessage = "Invalid offer status.")]
    public string Status { get; set; } = DomainValues.Pledged;

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? RespondedAt { get; set; }   // accepted/rejected kab hua
    public DateTime? CompletedAt { get; set; }   // donation complete kab hua
}