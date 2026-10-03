using System.ComponentModel.DataAnnotations;

namespace BloodConnect.Models
{
    /// <summary>
    /// Custom validation attribute — value must be true.
    /// Used for terms acceptance, consent checkboxes, etc.
    /// </summary>
    public class MustBeTrueAttribute : ValidationAttribute
    {
        public MustBeTrueAttribute()
        {
            ErrorMessage = "This field must be checked.";
        }

        protected override ValidationResult? IsValid(object? value, ValidationContext validationContext)
        {
            if (value is bool boolValue && boolValue)
                return ValidationResult.Success;

            return new ValidationResult(ErrorMessage ?? "This field must be checked.");
        }
    }
}