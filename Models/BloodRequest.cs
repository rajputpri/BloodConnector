using System.ComponentModel.DataAnnotations;

namespace BloodConnect.Models
{
    public class BloodRequest
    {
        [Key]
        public int RequestId { get; set; }

        [Required(ErrorMessage = "Requester name is required")]
        public string RequesterName { get; set; } = "";

        [Required(ErrorMessage = "Blood group needed is required")]
        public string BloodGroupNeeded { get; set; } = "";

        [Required(ErrorMessage = "Location is required")]
        public string Location { get; set; } = "";

        [Required(ErrorMessage = "Contact number is required")]
        [RegularExpression(@"^[0-9]{10}$", ErrorMessage = "Enter a valid 10-digit number")]
        public string ContactNumber { get; set; } = "";

        [Required(ErrorMessage = "Urgency level is required")]
        public string UrgencyLevel { get; set; } = "";

        public string Status { get; set; } = "Open";

        public DateTime RequestDate { get; set; } = DateTime.Now;

        public int? FulfilledByDonorId { get; set; }
    }
}