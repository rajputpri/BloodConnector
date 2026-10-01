using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    [Authorize(Roles = "Admin")]
    public class AdminController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<AppUser> _userManager;

        public AdminController(
            ApplicationDbContext context,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        // Helper: current user SuperAdmin hai?
        private bool IsSuperAdmin => User.IsInRole(DbSeeder.SuperAdminRole);

        // ==================== DASHBOARD ====================
        public async Task<IActionResult> Index()
        {
            var vm = new AdminDashboardViewModel
            {
                TotalUsers = await _userManager.Users.CountAsync(),
                TotalDonors = await _context.Donors.CountAsync(),
                AvailableDonors = await _context.Donors.CountAsync(d => d.IsAvailable),
                TotalRequests = await _context.BloodRequests.CountAsync(),
                OpenRequests = await _context.BloodRequests.CountAsync(r => r.Status == "Open"),
                FulfilledRequests = await _context.BloodRequests.CountAsync(r => r.Status == "Fulfilled"),

                RecentDonors = await _context.Donors
                    .AsNoTracking()
                    .OrderByDescending(d => d.DonorId)
                    .Take(5)
                    .ToListAsync(),

                RecentRequests = await _context.BloodRequests
                    .AsNoTracking()
                    .OrderByDescending(r => r.RequestDate)
                    .Take(5)
                    .ToListAsync()
            };

            return View(vm);
        }

        // ==================== DONORS ====================
        public async Task<IActionResult> Donors()
        {
            var donors = await _context.Donors
                .AsNoTracking()
                .OrderByDescending(d => d.DonorId)
                .ToListAsync();

            return View(donors);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteDonor(int id)
        {
            var donor = await _context.Donors.FindAsync(id);
            if (donor == null)
                return NotFound();

            try
            {
                _context.Donors.Remove(donor);
                await _context.SaveChangesAsync();
                TempData["Success"] = $"Donor '{donor.Name}' deleted.";
            }
            catch (DbUpdateException)
            {
                TempData["Error"] = "Cannot delete — linked to a blood request.";
            }

            return RedirectToAction(nameof(Donors));
        }

        // ==================== REQUESTS ====================
        public async Task<IActionResult> Requests()
        {
            var requests = await _context.BloodRequests
                .AsNoTracking()
                .Include(r => r.User)
                .OrderByDescending(r => r.RequestDate)
                .ToListAsync();

            return View(requests);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteRequest(int id)
        {
            var request = await _context.BloodRequests.FindAsync(id);
            if (request == null)
                return NotFound();

            try
            {
                _context.BloodRequests.Remove(request);
                await _context.SaveChangesAsync();
                TempData["Success"] = "Blood request deleted.";
            }
            catch (DbUpdateException)
            {
                TempData["Error"] = "Could not delete request.";
            }

            return RedirectToAction(nameof(Requests));
        }

        // ==================== USERS ====================
        public async Task<IActionResult> UserList()
        {
            var users = await _userManager.Users
                .OrderByDescending(u => u.CreatedAt)
                .ToListAsync();

            var userList = new List<UserWithRoleViewModel>();
            foreach (var user in users)
            {
                var roles = await _userManager.GetRolesAsync(user);
                userList.Add(new UserWithRoleViewModel
                {
                    Id = user.Id,
                    Email = user.Email ?? "",
                    FullName = user.FullName ?? "",
                    IsBanned = user.IsBanned,
                    CreatedAt = user.CreatedAt,
                    Roles = roles.ToList()
                });
            }

            return View(userList);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> ToggleBan(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound();

            // ✅ SuperAdmin ko koi ban nahi kar sakta
            if (await _userManager.IsInRoleAsync(user, DbSeeder.SuperAdminRole))
            {
                TempData["Error"] = "Cannot ban a SuperAdmin.";
                return RedirectToAction(nameof(UserList));
            }

            // ✅ Admin, doosre Admin ko ban nahi kar sakta (sirf SuperAdmin kar sakta)
            if (!IsSuperAdmin && await _userManager.IsInRoleAsync(user, DbSeeder.AdminRole))
            {
                TempData["Error"] = "Only a SuperAdmin can manage other Admins.";
                return RedirectToAction(nameof(UserList));
            }

            // Khud ko ban nahi kar sakta
            var currentUserId = _userManager.GetUserId(User);
            if (user.Id == currentUserId)
            {
                TempData["Error"] = "You cannot ban yourself.";
                return RedirectToAction(nameof(UserList));
            }

            user.IsBanned = !user.IsBanned;
            await _userManager.UpdateAsync(user);

            TempData["Success"] = user.IsBanned
                ? $"User '{user.Email}' banned."
                : $"User '{user.Email}' unbanned.";

            return RedirectToAction(nameof(UserList));
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteUser(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound();

            // ✅ SuperAdmin ko delete nahi kar sakte
            if (await _userManager.IsInRoleAsync(user, DbSeeder.SuperAdminRole))
            {
                TempData["Error"] = "Cannot delete a SuperAdmin.";
                return RedirectToAction(nameof(UserList));
            }

            // ✅ Admin, doosre Admin ko delete nahi kar sakta (sirf SuperAdmin)
            if (!IsSuperAdmin && await _userManager.IsInRoleAsync(user, DbSeeder.AdminRole))
            {
                TempData["Error"] = "Only a SuperAdmin can manage other Admins.";
                return RedirectToAction(nameof(UserList));
            }

            var currentUserId = _userManager.GetUserId(User);
            if (user.Id == currentUserId)
            {
                TempData["Error"] = "You cannot delete yourself.";
                return RedirectToAction(nameof(UserList));
            }

            var result = await _userManager.DeleteAsync(user);
            if (result.Succeeded)
                TempData["Success"] = "User deleted.";
            else
                TempData["Error"] = "Could not delete user.";

            return RedirectToAction(nameof(UserList));
        }

        // ==================== ROLE MANAGEMENT ====================

        // Promote: Admin aur SuperAdmin dono kar sakte hain (regular user ko Admin banao)
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> PromoteToAdmin(string id)
        {
            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound();

            if (await _userManager.IsInRoleAsync(user, DbSeeder.AdminRole))
            {
                TempData["Error"] = "User is already an Admin.";
                return RedirectToAction(nameof(UserList));
            }

            var result = await _userManager.AddToRoleAsync(user, DbSeeder.AdminRole);
            if (result.Succeeded)
                TempData["Success"] = $"'{user.Email}' is now an Admin.";
            else
                TempData["Error"] = "Could not promote user.";

            return RedirectToAction(nameof(UserList));
        }

        // Demote: SIRF SuperAdmin kar sakta hai
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DemoteFromAdmin(string id)
        {
            // ✅ Only SuperAdmin
            if (!IsSuperAdmin)
            {
                TempData["Error"] = "Only a SuperAdmin can remove Admin role.";
                return RedirectToAction(nameof(UserList));
            }

            var user = await _userManager.FindByIdAsync(id);
            if (user == null)
                return NotFound();

            // ✅ Doosre SuperAdmin ko demote nahi kar sakta
            if (await _userManager.IsInRoleAsync(user, DbSeeder.SuperAdminRole))
            {
                TempData["Error"] = "Cannot demote a SuperAdmin.";
                return RedirectToAction(nameof(UserList));
            }

            // ✅ Khud ko demote nahi kar sakta
            var currentUserId = _userManager.GetUserId(User);
            if (user.Id == currentUserId)
            {
                TempData["Error"] = "You cannot demote yourself.";
                return RedirectToAction(nameof(UserList));
            }

            if (!await _userManager.IsInRoleAsync(user, DbSeeder.AdminRole))
            {
                TempData["Error"] = "User is not an Admin.";
                return RedirectToAction(nameof(UserList));
            }

            var result = await _userManager.RemoveFromRoleAsync(user, DbSeeder.AdminRole);
            if (result.Succeeded)
                TempData["Success"] = $"'{user.Email}' is no longer an Admin.";
            else
                TempData["Error"] = "Could not demote user.";

            return RedirectToAction(nameof(UserList));
        }
    }
}