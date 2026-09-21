using System.ComponentModel.DataAnnotations;
namespace BloodConnect.Models{




public class Donor
{
public int DonorId { get; set; }
[Required(ErrorMessage = "Name is required")]
public string Name { get; set; } = "";

[Required(ErrorMessage = "Blood group is required")]
public string BloodGroup { get; set; } = "";

[Required(ErrorMessage = "Location is required")]
public string Location { get; set; } = "";

[Required(ErrorMessage = "Contact number is required")]
[RegularExpression(@"^[0-9]{10}$", ErrorMessage = "Enter a valid 10-digit number")]
public string ContactNumber { get; set; } = "";
public bool IsAvailable { get; set; } = true;
}
}