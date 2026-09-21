using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    public class DonorController : Controller
    {
        private readonly ApplicationDbContext _context;

        public DonorController(ApplicationDbContext context)
        {
            _context = context;

            if (!_context.Donors.Any())
            {
                _context.Donors.Add(new Donor { Name = "Pawan", BloodGroup = "AB-", Location = "Bihar", ContactNumber = "1234567890", IsAvailable = true });
                _context.Donors.Add(new Donor { Name = "Ravi Kumar", BloodGroup = "O+", Location = "Gujarat", ContactNumber = "4535393458", IsAvailable = true });
                _context.Donors.Add(new Donor { Name = "Ramesh", BloodGroup = "B+", Location = "Maharashtra", ContactNumber = "9876543210", IsAvailable = true });
                _context.SaveChanges();
            }
        }

        public IActionResult Index()

        {
            var donors = _context.Donors.ToList();
            return View(donors);
        }
        
        [HttpGet]
        public IActionResult Search(string bloodGroup, string location)
        {
            var donors = _context.Donors.Where(d => d.IsAvailable).AsQueryable();

            if (!string.IsNullOrEmpty(bloodGroup))
            {
                donors = donors.Where(d => d.BloodGroup == bloodGroup);
            }

            if (!string.IsNullOrEmpty(location))
            {
                donors = donors.Where(d => d.Location.Contains(location));
            }

            return View("Index", donors.ToList());
        }
        [HttpGet]
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Create(Donor donor)
        {
            if (ModelState.IsValid)
            {
                _context.Donors.Add(donor);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(donor);
        }

        [HttpGet]
        public IActionResult Edit(int id)
        {
            var donor = _context.Donors.Find(id);
            if (donor == null)
            {
                return NotFound();
            }
            return View(donor);
        }

        [HttpPost]
        public IActionResult Edit(Donor donor)
        {
            if (ModelState.IsValid)
            {
                _context.Donors.Update(donor);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(donor);
        }

        [HttpGet]
        public IActionResult Delete(int id)
        {
            var donor = _context.Donors.Find(id);
            if (donor == null)
            {
                return NotFound();
            }
            return View(donor);
        }

        [HttpPost]
        public IActionResult DeleteConfirmed(int id)
        {
            var donor = _context.Donors.Find(id);
            if (donor != null)
            {
                _context.Donors.Remove(donor);
                _context.SaveChanges();
            }
            return RedirectToAction("Index");
        }
    }
}