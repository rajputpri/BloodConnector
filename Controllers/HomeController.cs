using System.Diagnostics;
using BloodConnect.Models;
using BloodConnect.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    public class HomeController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly MessageCache _messageCache;

        public HomeController(ApplicationDbContext context, MessageCache messageCache)
        {
            _context = context;
            _messageCache = messageCache;
        }

        public async Task<IActionResult> Index()
        {
            ViewBag.TotalDonors = await _context.Donors.CountAsync();
            ViewBag.AvailableDonors = await _context.Donors.CountAsync(d => d.IsAvailable);
            ViewBag.TotalRequests = await _context.BloodRequests.CountAsync();
            ViewBag.OpenRequests = await _context.BloodRequests.CountAsync(r => r.Status == "Open");
            ViewBag.FulfilledRequests = await _context.BloodRequests.CountAsync(r => r.Status == "Fulfilled");
            ViewBag.LivesTouched = (await _context.BloodRequests
                .CountAsync(r => r.Status == "Fulfilled")) * 2;

            ViewBag.CriticalRequests = await _context.BloodRequests
                .AsNoTracking()
                .Where(r => r.Status == "Open")
                .OrderByDescending(r => r.UrgencyLevel == "Critical")
                .ThenByDescending(r => r.RequestDate)
                .Take(3)
                .ToListAsync();

            return View();
        }

        public async Task<IActionResult> About()
        {
            ViewBag.TotalDonors = await _context.Donors.CountAsync();
            ViewBag.FulfilledRequests = await _context.BloodRequests.CountAsync(r => r.Status == "Fulfilled");
            ViewBag.LivesTouched = ViewBag.FulfilledRequests * 2;
            ViewBag.TotalUsers = await _context.Users.CountAsync();
            return View();
        }

        public IActionResult Faq() => View();

        [HttpGet]
        public IActionResult Contact() => View();

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Contact(ContactViewModel model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var message = new ContactMessage
            {
                Name = model.Name.Trim(),
                Email = model.Email.Trim(),
                Subject = model.Subject.Trim(),
                Message = model.Message.Trim(),
                CreatedAt = DateTime.UtcNow,
                IsRead = false
            };

            _context.ContactMessages.Add(message);
            await _context.SaveChangesAsync();

            // ✅ Invalidate admin badge cache — naya message aaya
            _messageCache.Invalidate();

            TempData["Success"] = "Thank you! Your message has been received. We'll get back within 24 hours.";
            return RedirectToAction(nameof(Contact));
        }

        public IActionResult Privacy() => View();

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error(int? code = null)
        {
            ViewBag.StatusCode = code;
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}