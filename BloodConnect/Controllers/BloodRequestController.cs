using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    public class BloodRequestController : Controller
    {
        private readonly ApplicationDbContext _context;

        public BloodRequestController(ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            var requests = _context.BloodRequests.ToList();
            return View(requests);
        }

        [HttpGet]
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Create(BloodRequest request)
        {
            if (ModelState.IsValid)
            {
                _context.BloodRequests.Add(request);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(request);
        }
    }
}