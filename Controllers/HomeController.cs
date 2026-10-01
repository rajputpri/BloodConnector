using System.Diagnostics;
using BloodConnect.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    public class HomeController : Controller
    {
        private readonly ApplicationDbContext _context;

        public HomeController(ApplicationDbContext context)
        {
            _context = context;
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
        public IActionResult Contact(ContactViewModel model)
        {
            if (!ModelState.IsValid)
                return View(model);

            // In production: integrate email service (SendGrid, SMTP, etc.)
            // For now: log and show success
            // var body = $"From: {model.Name} <{model.Email}>\nSubject: {model.Subject}\n\n{model.Message}";

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