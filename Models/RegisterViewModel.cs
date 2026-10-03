using System.ComponentModel.DataAnnotations;

namespace BloodConnect.Models;

public class RegisterViewModel
{
    [Required(ErrorMessage = "Full name is required")]
    [StringLength(100, MinimumLength = 2,
        ErrorMessage = "Name must be 2-100 characters")]
    [Display(Name = "Full Name")]
    public string FullName { get; set; } = "";

    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Enter a valid email address")]
    [StringLength(150)]
    [Display(Name = "Email Address")]
    public string Email { get; set; } = "";

    [Required(ErrorMessage = "Password is required")]
    [StringLength(100, MinimumLength = 6,
        ErrorMessage = "Password must be at least 6 characters")]
    [DataType(DataType.Password)]
    public string Password { get; set; } = "";

    [Required(ErrorMessage = "Please confirm your password")]
    [DataType(DataType.Password)]
    [Display(Name = "Confirm Password")]
    [Compare(nameof(Password), ErrorMessage = "Passwords do not match")]
    public string ConfirmPassword { get; set; } = "";

    [MustBeTrue(ErrorMessage = "You must accept the terms and privacy policy to register")]
    [Display(Name = "I agree to the Terms of Service and Privacy Policy")]
    public bool AcceptTerms { get; set; }
}