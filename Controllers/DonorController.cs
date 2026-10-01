using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    public class DonorController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<AppUser> _userManager;

        public DonorController(
            ApplicationDbContext context,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        // ----- Helpers -----
        private string? CurrentUserId => _userManager.GetUserId(User);
        private bool IsAdmin => User.IsInRole(DbSeeder.AdminRole) || User.IsInRole(DbSeeder.SuperAdminRole);

        private bool CanEditDonor(Donor donor)
        {
            if (string.IsNullOrEmpty(CurrentUserId)) return false;
            return donor.UserId == CurrentUserId;
        }

        private bool CanDeleteDonor(Donor donor)
        {
            if (IsAdmin) return true;
            return CanEditDonor(donor);
        }

        // ----- Public: List & Search -----
        public async Task<IActionResult> Index()
        {
            var userId = CurrentUserId;

            var myDonorId = string.IsNullOrEmpty(userId)
                ? (int?)null
                : await _context.Donors
                    .Where(d => d.UserId == userId)
                    .Select(d => (int?)d.DonorId)
                    .FirstOrDefaultAsync();

            ViewBag.UserDonorId = myDonorId;

            var donors = await _context.Donors
                .AsNoTracking()
                .OrderByDescending(d => d.DonorId)
                .ToListAsync();

            return View(donors);
        }

        [HttpGet]
        public async Task<IActionResult> Search(
            string? bloodGroup,
            string? location,
            bool exactMatch = false)
        {
            var query = _context.Donors
                .AsNoTracking()
                .Where(d => d.IsAvailable);

            // ✅ Blood group compatibility filter
            var compatibleGroups = new List<string>();

            if (!string.IsNullOrWhiteSpace(bloodGroup) && BloodCompatibility.IsValid(bloodGroup))
            {
                if (exactMatch)
                {
                    // Exact match — only same blood group
                    query = query.Where(d => d.BloodGroup == bloodGroup);
                    compatibleGroups.Add(bloodGroup);
                }
                else
                {
                    // Compatible match — all groups that can donate to this patient
                    var groups = BloodCompatibility.CompatibleDonorsFor(bloodGroup).ToList();
                    query = query.Where(d => groups.Contains(d.BloodGroup));
                    compatibleGroups = groups;
                }
            }

            if (!string.IsNullOrWhiteSpace(location))
                query = query.Where(d => d.Location.Contains(location));

            // ViewBag for UI
            ViewBag.SelectedBloodGroup = bloodGroup;
            ViewBag.SelectedLocation = location;
            ViewBag.ExactMatch = exactMatch;
            ViewBag.CompatibleGroups = compatibleGroups;
            ViewBag.IsCompatibleSearch = !exactMatch
                                        && !string.IsNullOrWhiteSpace(bloodGroup)
                                        && BloodCompatibility.IsValid(bloodGroup);

            var userId = CurrentUserId;
            ViewBag.UserDonorId = string.IsNullOrEmpty(userId)
                ? (int?)null
                : await _context.Donors
                    .Where(d => d.UserId == userId)
                    .Select(d => (int?)d.DonorId)
                    .FirstOrDefaultAsync();

            // Ordering: in compatibility mode, show exact matches first, then by donor id
            var results = await query
                .OrderByDescending(d => d.BloodGroup == bloodGroup)
                .ThenByDescending(d => d.DonorId)
                .ToListAsync();

            return View("Index", results);
        }

        // ----- Create (1 per user) -----
        [HttpGet]
        [Authorize]
        public async Task<IActionResult> Create()
        {
            var userId = CurrentUserId!;

            var existing = await _context.Donors
                .FirstOrDefaultAsync(d => d.UserId == userId);

            if (existing != null)
            {
                TempData["Error"] = "You already have a donor profile.";
                return RedirectToAction(nameof(Edit), new { id = existing.DonorId });
            }

            return View();
        }

        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Donor donor)
        {
            var userId = CurrentUserId!;

            if (await _context.Donors.AnyAsync(d => d.UserId == userId))
            {
                TempData["Error"] = "You already have a donor profile.";
                return RedirectToAction(nameof(Index));
            }

            ModelState.Remove(nameof(Donor.UserId));
            ModelState.Remove(nameof(Donor.User));

            if (!ModelState.IsValid)
                return View(donor);

            try
            {
                donor.UserId = userId;
                _context.Donors.Add(donor);
                await _context.SaveChangesAsync();

                TempData["Success"] = $"{donor.Name}, you're registered as a donor. Thank you!";
                return RedirectToAction(nameof(Index));
            }
            catch (DbUpdateException)
            {
                ModelState.AddModelError("", "Could not save donor. Please try again.");
                return View(donor);
            }
        }

        // ----- Edit (OWNER ONLY) -----
        [HttpGet]
        [Authorize]
        public async Task<IActionResult> Edit(int id)
        {
            var donor = await _context.Donors.FindAsync(id);
            if (donor == null) return NotFound();
            if (!CanEditDonor(donor)) return Forbid();
            return View(donor);
        }

        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, Donor donor)
        {
            if (id != donor.DonorId) return BadRequest();

            var existing = await _context.Donors.FindAsync(id);
            if (existing == null) return NotFound();
            if (!CanEditDonor(existing)) return Forbid();

            ModelState.Remove(nameof(Donor.UserId));
            ModelState.Remove(nameof(Donor.User));

            if (!ModelState.IsValid)
                return View(donor);

            try
            {
                existing.Name = donor.Name;
                existing.BloodGroup = donor.BloodGroup;
                existing.Location = donor.Location;
                existing.ContactNumber = donor.ContactNumber;
                existing.IsAvailable = donor.IsAvailable;

                await _context.SaveChangesAsync();
                TempData["Success"] = "Profile updated.";
                return RedirectToAction(nameof(Index));
            }
            catch (DbUpdateConcurrencyException)
            {
                ModelState.AddModelError("", "Modified by someone else. Reload and try again.");
                return View(donor);
            }
            catch (DbUpdateException)
            {
                ModelState.AddModelError("", "Could not update. Try again.");
                return View(donor);
            }
        }

        // ----- Delete (owner OR admin) -----
        [HttpGet]
        [Authorize]
        public async Task<IActionResult> Delete(int id)
        {
            var donor = await _context.Donors
                .AsNoTracking()
                .FirstOrDefaultAsync(d => d.DonorId == id);

            if (donor == null) return NotFound();
            if (!CanDeleteDonor(donor)) return Forbid();
            return View(donor);
        }

        [HttpPost, ActionName("Delete")]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var donor = await _context.Donors.FindAsync(id);
            if (donor == null) return NotFound();
            if (!CanDeleteDonor(donor)) return Forbid();

            try
            {
                _context.Donors.Remove(donor);
                await _context.SaveChangesAsync();
                TempData["Success"] = "Donor profile deleted.";
            }
            catch (DbUpdateException)
            {
                TempData["Error"] = "Cannot delete — linked to a blood request.";
            }

            return RedirectToAction(nameof(Index));
        }
    }
}