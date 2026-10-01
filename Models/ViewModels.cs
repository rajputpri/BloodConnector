namespace BloodConnect.Models;

public class AdminDashboardViewModel
{
    public int TotalUsers { get; set; }
    public int TotalDonors { get; set; }
    public int AvailableDonors { get; set; }
    public int TotalRequests { get; set; }
    public int OpenRequests { get; set; }
    public int FulfilledRequests { get; set; }

    public List<Donor> RecentDonors { get; set; } = new();
    public List<BloodRequest> RecentRequests { get; set; } = new();
}

public class UserWithRoleViewModel
{
    public string Id { get; set; } = "";
    public string Email { get; set; } = "";
    public string FullName { get; set; } = "";
    public bool IsBanned { get; set; }
    public DateTime CreatedAt { get; set; }
    public List<string> Roles { get; set; } = new();
}

public class UserDashboardViewModel
{
    public string FullName { get; set; } = "";
    public string Email { get; set; } = "";
    public DateTime MemberSince { get; set; }
    public List<string> Roles { get; set; } = new();
    public bool IsBanned { get; set; }

    public Donor? MyDonorProfile { get; set; }

    public List<BloodRequest> MyRequests { get; set; } = new();
    public List<BloodRequest> MyDonations { get; set; } = new();
    public List<DonationOffer> MyOffers { get; set; } = new();   // ✅ offers I made as donor

    public int TotalRequestsPosted { get; set; }
    public int ActiveRequestsCount { get; set; }
    public int TotalDonationsMade { get; set; }
    public int PendingOffersCount { get; set; }                   // ✅ my pending offers
}

// ✅ NEW — Offers page
public class OffersViewModel
{
    public BloodRequest Request { get; set; } = null!;
    public List<DonationOffer> Offers { get; set; } = new();
    public int? MyDonorId { get; set; }
}
// ✅ Contact page view model
public class ContactViewModel
{
    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "Your name is required")]
    [System.ComponentModel.DataAnnotations.StringLength(100)]
    public string Name { get; set; } = "";

    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "Email is required")]
    [System.ComponentModel.DataAnnotations.EmailAddress(ErrorMessage = "Enter a valid email")]
    [System.ComponentModel.DataAnnotations.StringLength(150)]
    public string Email { get; set; } = "";

    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "Subject is required")]
    [System.ComponentModel.DataAnnotations.StringLength(150)]
    public string Subject { get; set; } = "";

    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "Message is required")]
    [System.ComponentModel.DataAnnotations.StringLength(2000, MinimumLength = 10,
        ErrorMessage = "Message must be 10-2000 characters")]
    public string Message { get; set; } = "";
}