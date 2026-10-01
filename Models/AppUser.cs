using Microsoft.AspNetCore.Identity;

namespace BloodConnect.Models;

public class AppUser : IdentityUser
{
    public string? FullName { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public bool IsBanned { get; set; } = false;
}