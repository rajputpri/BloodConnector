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

        [HttpGet]
        public IActionResult Edit(int id)
        {
            var request = _context.BloodRequests.Find(id);
            if (request == null)
            {
                return NotFound();
            }
            return View(request);
        }

        [HttpPost]
        public IActionResult Edit(BloodRequest request)
        {
            if (ModelState.IsValid)
            {
                _context.BloodRequests.Update(request);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(request);
        }

        [HttpGet]
        public IActionResult Delete(int id)
        {
            var request = _context.BloodRequests.Find(id);
            if (request == null)
            {
                return NotFound();
            }
            return View(request);
        }

        [HttpPost]
        public IActionResult DeleteConfirmed(int id)
        {
            var request = _context.BloodRequests.Find(id);
            if (request != null)
            {
                _context.BloodRequests.Remove(request);
                _context.SaveChanges();
            }
            return RedirectToAction("Index");
        }

        [HttpGet]
        public IActionResult MarkFulfilled(int id)
        {
            var request = _context.BloodRequests.Find(id);
            if (request == null)
            {
                return NotFound();
            }

            ViewBag.Donors = _context.Donors.Where(d => d.BloodGroup == request.BloodGroupNeeded).ToList();
            return View(request);
        }

        [HttpPost]
        public IActionResult MarkFulfilled(int id, int donorId)
        {
            var request = _context.BloodRequests.Find(id);
            if (request != null)
            {
                request.FulfilledByDonorId = donorId;
                request.Status = "Fulfilled";
                _context.SaveChanges();
            }
            return RedirectToAction("Index");
        }
    }
}