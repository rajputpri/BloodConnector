using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    public class BloodRequestController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<AppUser> _userManager;

        public BloodRequestController(
            ApplicationDbContext context,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        // ----- Helpers -----
        private bool IsSuperAdmin => User.IsInRole(DbSeeder.SuperAdminRole);
        private bool IsAdmin => User.IsInRole(DbSeeder.AdminRole) || IsSuperAdmin;

        private bool CanEditRequest(BloodRequest request)
        {
            if (User.Identity?.IsAuthenticated != true) return false;
            var currentUserId = _userManager.GetUserId(User);
            return !string.IsNullOrEmpty(currentUserId) && request.UserId == currentUserId;
        }

        private bool CanDeleteRequest(BloodRequest request)
        {
            if (IsAdmin) return true;
            return CanEditRequest(request);
        }

        // ----- Index -----
        public async Task<IActionResult> Index(
            string? bloodGroup,
            string? urgency,
            string? status)
        {
            var query = _context.BloodRequests.AsNoTracking().AsQueryable();

            if (!string.IsNullOrWhiteSpace(bloodGroup))
                query = query.Where(r => r.BloodGroupNeeded == bloodGroup);
            if (!string.IsNullOrWhiteSpace(urgency))
                query = query.Where(r => r.UrgencyLevel == urgency);
            if (!string.IsNullOrWhiteSpace(status))
                query = query.Where(r => r.Status == status);

            var requests = await query
                .OrderByDescending(r => r.RequestDate)
                .ToListAsync();

            // ---- Viewer context (donor info, offers) ----
            var currentUserId = _userManager.GetUserId(User);
            int? myDonorId = null;
            string? myBloodGroup = null;
            var myOfferRequestIds = new HashSet<int>();

            if (!string.IsNullOrEmpty(currentUserId))
            {
                var myDonor = await _context.Donors.AsNoTracking()
                    .FirstOrDefaultAsync(d => d.UserId == currentUserId);

                if (myDonor != null)
                {
                    myDonorId = myDonor.DonorId;
                    myBloodGroup = myDonor.BloodGroup;

                    myOfferRequestIds = (await _context.DonationOffers.AsNoTracking()
                        .Where(o => o.DonorId == myDonor.DonorId
                            && (o.Status == DomainValues.Pledged
                                || o.Status == DomainValues.Accepted))
                        .Select(o => o.RequestId)
                        .ToListAsync()).ToHashSet();
                }
            }

            ViewBag.FilterBloodGroup = bloodGroup;
            ViewBag.FilterUrgency = urgency;
            ViewBag.FilterStatus = status;
            ViewBag.MyDonorId = myDonorId;
            ViewBag.MyBloodGroup = myBloodGroup;
            ViewBag.MyOfferRequestIds = myOfferRequestIds;

            return View(requests);
        }

        // ----- Create -----
        [HttpGet]
        public IActionResult Create() => View();

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(BloodRequest request)
        {
            ModelState.Remove(nameof(BloodRequest.UserId));
            ModelState.Remove(nameof(BloodRequest.User));
            ValidateLocation(request.State, request.City);
            ModelState.Remove(nameof(BloodRequest.Location));
            request.Location = BuildLocation(request.City, request.State);

            if (!ModelState.IsValid) return View(request);

            try
            {
                request.Status = DomainValues.Open;
                request.RequestDate = DateTime.UtcNow;

                if (User.Identity?.IsAuthenticated == true)
                    request.UserId = _userManager.GetUserId(User);

                _context.BloodRequests.Add(request);
                await _context.SaveChangesAsync();
                TempData["Success"] = "Blood request created successfully.";
                return RedirectToAction(nameof(Index));
            }
            catch (DbUpdateException)
            {
                ModelState.AddModelError("", "Could not create request. Please try again.");
                return View(request);
            }
        }

        // ----- Edit (OWNER ONLY) -----
        [HttpGet]
        [Authorize]
        public async Task<IActionResult> Edit(int id)
        {
            var request = await _context.BloodRequests.FindAsync(id);
            if (request == null) return NotFound();
            if (!CanEditRequest(request)) return Forbid();
            return View(request);
        }

        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, BloodRequest request)
        {
            if (id != request.RequestId) return BadRequest();
            var existing = await _context.BloodRequests.FindAsync(id);
            if (existing == null) return NotFound();
            if (!CanEditRequest(existing)) return Forbid();

            ModelState.Remove(nameof(BloodRequest.UserId));
            ModelState.Remove(nameof(BloodRequest.User));
            ValidateLocation(request.State, request.City);
            ModelState.Remove(nameof(BloodRequest.Location));
            request.Location = BuildLocation(request.City, request.State);

            if (!ModelState.IsValid) return View(request);

            try
            {
                existing.RequesterName = request.RequesterName;
                existing.BloodGroupNeeded = request.BloodGroupNeeded;
                existing.State = request.State;
                existing.City = request.City;
                existing.Location = request.Location;
                existing.ContactNumber = request.ContactNumber;
                existing.UrgencyLevel = request.UrgencyLevel;

                await _context.SaveChangesAsync();
                TempData["Success"] = "Blood request updated.";
                return RedirectToAction(nameof(Index));
            }
            catch (DbUpdateException)
            {
                ModelState.AddModelError("", "Could not update. Try again.");
                return View(request);
            }
        }

        // ✅ FIXED — state nullable accept karta hai (purane rows ke liye safety)
        private void ValidateLocation(string? state, string? city)
        {
            if (!DomainValues.IsValidState(state))
                ModelState.AddModelError(nameof(BloodRequest.State),
                    "Select a valid Indian state or union territory.");

            if (!string.IsNullOrWhiteSpace(city) && city.Length > 50)
                ModelState.AddModelError(nameof(BloodRequest.City),
                    "City cannot exceed 50 characters.");
        }

        // ✅ FIXED — state nullable handle karta hai ("" return ho sakta hai but validation already rokega)
        private static string BuildLocation(string? city, string? state)
        {
            if (string.IsNullOrWhiteSpace(state))
                return city?.Trim() ?? "";
            return string.IsNullOrWhiteSpace(city) ? state : $"{city.Trim()}, {state}";
        }

        // ----- Delete (owner OR admin) -----
        [HttpGet]
        [Authorize]
        public async Task<IActionResult> Delete(int id)
        {
            var request = await _context.BloodRequests.AsNoTracking()
                .FirstOrDefaultAsync(r => r.RequestId == id);
            if (request == null) return NotFound();
            if (!CanDeleteRequest(request)) return Forbid();
            return View(request);
        }

        [HttpPost, ActionName("Delete")]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var request = await _context.BloodRequests.FindAsync(id);
            if (request == null) return NotFound();
            if (!CanDeleteRequest(request)) return Forbid();

            try
            {
                _context.BloodRequests.Remove(request);
                await _context.SaveChangesAsync();
                TempData["Success"] = "Request deleted.";
            }
            catch (DbUpdateException)
            {
                TempData["Error"] = "Could not delete request.";
            }

            return RedirectToAction(nameof(Index));
        }

        // ==================================================
        // ============ DONATION OFFER WORKFLOW ============
        // ==================================================

        // ----- Offers list (owner / admin) -----
        [HttpGet]
        [Authorize]
        public async Task<IActionResult> Offers(int id)
        {
            var request = await _context.BloodRequests
                .AsNoTracking()
                .Include(r => r.User)
                .Include(r => r.FulfilledByDonor)
                .FirstOrDefaultAsync(r => r.RequestId == id);

            if (request == null) return NotFound();

            var currentUserId = _userManager.GetUserId(User);
            var isOwner = request.UserId == currentUserId;

            if (!isOwner && !IsAdmin)
                return Forbid();

            var offers = await _context.DonationOffers
                .AsNoTracking()
                .Include(o => o.Donor)
                .Where(o => o.RequestId == id)
                .OrderByDescending(o => o.CreatedAt)
                .ToListAsync();

            int? myDonorId = null;
            if (!string.IsNullOrEmpty(currentUserId))
            {
                myDonorId = await _context.Donors
                    .Where(d => d.UserId == currentUserId)
                    .Select(d => (int?)d.DonorId)
                    .FirstOrDefaultAsync();
            }

            var vm = new OffersViewModel
            {
                Request = request,
                Offers = offers,
                MyDonorId = myDonorId
            };

            return View(vm);
        }

        // ----- Donor creates offer -----
        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Offer(int requestId)
        {
            var request = await _context.BloodRequests.FindAsync(requestId);
            if (request == null) return NotFound();

            if (request.Status != DomainValues.Open)
            {
                TempData["Error"] = "This request is no longer open.";
                return RedirectToAction(nameof(Index));
            }

            var currentUserId = _userManager.GetUserId(User);
            if (string.IsNullOrEmpty(currentUserId))
                return Challenge();

            if (request.UserId == currentUserId)
            {
                TempData["Error"] = "You cannot offer on your own request.";
                return RedirectToAction(nameof(Index));
            }

            var myDonor = await _context.Donors
                .FirstOrDefaultAsync(d => d.UserId == currentUserId);

            if (myDonor == null)
            {
                TempData["Error"] = "Please create a donor profile first.";
                return RedirectToAction(nameof(Index));
            }

            if (myDonor.BloodGroup != request.BloodGroupNeeded)
            {
                TempData["Error"] = "Your blood group doesn't match this request.";
                return RedirectToAction(nameof(Index));
            }

            var existing = await _context.DonationOffers
                .FirstOrDefaultAsync(o => o.RequestId == requestId && o.DonorId == myDonor.DonorId);

            if (existing != null)
            {
                if (existing.Status == DomainValues.Pledged || existing.Status == DomainValues.Accepted)
                {
                    TempData["Error"] = "You have already offered for this request.";
                    return RedirectToAction(nameof(Index));
                }

                // Rejected/Cancelled/Completed — reuse record, reset to Pledged
                existing.Status = DomainValues.Pledged;
                existing.CreatedAt = DateTime.UtcNow;
                existing.RespondedAt = null;
                existing.CompletedAt = null;
                await _context.SaveChangesAsync();

                TempData["Success"] = "Your offer has been renewed.";
                return RedirectToAction(nameof(Index));
            }

            var offer = new DonationOffer
            {
                RequestId = requestId,
                DonorId = myDonor.DonorId,
                Status = DomainValues.Pledged,
                CreatedAt = DateTime.UtcNow
            };

            _context.DonationOffers.Add(offer);
            await _context.SaveChangesAsync();
            TempData["Success"] = "Your offer has been sent to the requester.";
            return RedirectToAction(nameof(Index));
        }

        // ----- Donor cancels own offer -----
        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> CancelOffer(int id)
        {
            var offer = await _context.DonationOffers
                .Include(o => o.Donor)
                .FirstOrDefaultAsync(o => o.Id == id);

            if (offer == null) return NotFound();

            var currentUserId = _userManager.GetUserId(User);
            if (offer.Donor.UserId != currentUserId)
                return Forbid();

            if (offer.Status != DomainValues.Pledged)
            {
                TempData["Error"] = "Only pending offers can be cancelled.";
                return RedirectToAction(nameof(Index));
            }

            offer.Status = DomainValues.Cancelled;
            offer.RespondedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            TempData["Success"] = "Your offer has been cancelled.";
            return RedirectToAction(nameof(Index));
        }

        // ----- Owner/Admin accepts offer -----
        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> AcceptOffer(int id)
        {
            var offer = await _context.DonationOffers
                .Include(o => o.Request)
                .Include(o => o.Donor)
                .FirstOrDefaultAsync(o => o.Id == id);

            if (offer == null) return NotFound();

            var currentUserId = _userManager.GetUserId(User);
            var isOwner = offer.Request.UserId == currentUserId;
            if (!isOwner && !IsAdmin) return Forbid();

            if (offer.Request.Status != DomainValues.Open)
            {
                TempData["Error"] = "This request is no longer open.";
                return RedirectToAction(nameof(Offers), new { id = offer.RequestId });
            }

            if (offer.Status != DomainValues.Pledged)
            {
                TempData["Error"] = "Only pending offers can be accepted.";
                return RedirectToAction(nameof(Offers), new { id = offer.RequestId });
            }

            // Auto-reject all other Pledged offers
            var otherPledged = await _context.DonationOffers
                .Where(o => o.RequestId == offer.RequestId
                    && o.Id != offer.Id
                    && o.Status == DomainValues.Pledged)
                .ToListAsync();

            foreach (var o in otherPledged)
            {
                o.Status = DomainValues.Rejected;
                o.RespondedAt = DateTime.UtcNow;
            }

            offer.Status = DomainValues.Accepted;
            offer.RespondedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();

            TempData["Success"] = $"You accepted {offer.Donor.Name}'s offer. Contact: {offer.Donor.ContactNumber}";
            return RedirectToAction(nameof(Offers), new { id = offer.RequestId });
        }

        // ----- Owner/Admin rejects offer -----
        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> RejectOffer(int id)
        {
            var offer = await _context.DonationOffers
                .Include(o => o.Request)
                .FirstOrDefaultAsync(o => o.Id == id);

            if (offer == null) return NotFound();

            var currentUserId = _userManager.GetUserId(User);
            var isOwner = offer.Request.UserId == currentUserId;
            if (!isOwner && !IsAdmin) return Forbid();

            if (offer.Status != DomainValues.Pledged && offer.Status != DomainValues.Accepted)
            {
                TempData["Error"] = "This offer cannot be rejected at this stage.";
                return RedirectToAction(nameof(Offers), new { id = offer.RequestId });
            }

            offer.Status = DomainValues.Rejected;
            offer.RespondedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            TempData["Success"] = "Offer rejected.";
            return RedirectToAction(nameof(Offers), new { id = offer.RequestId });
        }

        // ----- Complete donation (owner / admin / accepted donor) -----
        [HttpPost]
        [Authorize]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> CompleteDonation(int id)
        {
            var offer = await _context.DonationOffers
                .Include(o => o.Request)
                .Include(o => o.Donor)
                .FirstOrDefaultAsync(o => o.Id == id);

            if (offer == null) return NotFound();

            var currentUserId = _userManager.GetUserId(User);
            var isOwner = offer.Request.UserId == currentUserId;
            var isAcceptedDonor = offer.Donor.UserId == currentUserId;

            if (!isOwner && !IsAdmin && !isAcceptedDonor)
                return Forbid();

            if (offer.Status != DomainValues.Accepted)
            {
                TempData["Error"] = "Only accepted offers can be marked complete.";
                return RedirectToAction(nameof(Offers), new { id = offer.RequestId });
            }

            // Mark offer completed
            offer.Status = DomainValues.Completed;
            offer.CompletedAt = DateTime.UtcNow;

            // Mark request fulfilled
            offer.Request.Status = DomainValues.Fulfilled;
            offer.Request.FulfilledByDonorId = offer.DonorId;

            // Any remaining Pledged offers → rejected
            var remaining = await _context.DonationOffers
                .Where(o => o.RequestId == offer.RequestId
                    && o.Id != offer.Id
                    && o.Status == DomainValues.Pledged)
                .ToListAsync();

            foreach (var o in remaining)
            {
                o.Status = DomainValues.Rejected;
                o.RespondedAt = DateTime.UtcNow;
            }

            await _context.SaveChangesAsync();

            TempData["Success"] = "Donation marked as completed. Request fulfilled!";
            return RedirectToAction(nameof(Index));
        }
    }
}