using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    [Authorize]
    public class DashboardController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<AppUser> _userManager;

        public DashboardController(
            ApplicationDbContext context,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        public async Task<IActionResult> Index()
        {
            var userId = _userManager.GetUserId(User);
            if (string.IsNullOrEmpty(userId)) return Challenge();

            var user = await _userManager.FindByIdAsync(userId);
            if (user == null) return NotFound();

            var roles = await _userManager.GetRolesAsync(user);

            var myDonor = await _context.Donors.AsNoTracking()
                .FirstOrDefaultAsync(d => d.UserId == userId);

            var myRequests = await _context.BloodRequests.AsNoTracking()
                .Where(r => r.UserId == userId)
                .OrderByDescending(r => r.RequestDate)
                .ToListAsync();

            var myDonations = myDonor == null
                ? new List<BloodRequest>()
                : await _context.BloodRequests.AsNoTracking()
                    .Where(r => r.FulfilledByDonorId == myDonor.DonorId)
                    .OrderByDescending(r => r.RequestDate)
                    .ToListAsync();

            var myOffers = myDonor == null
                ? new List<DonationOffer>()
                : await _context.DonationOffers.AsNoTracking()
                    .Include(o => o.Request)
                    .Where(o => o.DonorId == myDonor.DonorId)
                    .OrderByDescending(o => o.CreatedAt)
                    .Take(10)
                    .ToListAsync();

            var vm = new UserDashboardViewModel
            {
                FullName = user.FullName ?? "",
                Email = user.Email ?? "",
                MemberSince = user.CreatedAt,
                Roles = roles.ToList(),
                IsBanned = user.IsBanned,
                MyDonorProfile = myDonor,
                MyRequests = myRequests,
                MyDonations = myDonations,
                MyOffers = myOffers,
                TotalRequestsPosted = myRequests.Count,
                ActiveRequestsCount = myRequests.Count(r => r.Status == DomainValues.Open),
                TotalDonationsMade = myDonations.Count,
                PendingOffersCount = myOffers.Count(o => o.Status == DomainValues.Pledged)
            };

            return View(vm);
        }
    }
}