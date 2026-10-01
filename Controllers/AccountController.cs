using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;

namespace BloodConnect.Controllers
{
    public class AccountController : Controller
    {
        private readonly UserManager<AppUser> _userManager;
        private readonly SignInManager<AppUser> _signInManager;

        public AccountController(
            UserManager<AppUser> userManager,
            SignInManager<AppUser> signInManager)
        {
            _userManager = userManager;
            _signInManager = signInManager;
        }

        [HttpGet]
        public IActionResult Register()
        {
            if (_signInManager.IsSignedIn(User))
                return RedirectToAction("Index", "Home");

            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Register(RegisterViewModel model)
        {
            if (!ModelState.IsValid)
                return View(model);

            var user = new AppUser
            {
                UserName = model.Email,
                Email = model.Email,
                FullName = model.FullName,
                EmailConfirmed = true,
                CreatedAt = DateTime.UtcNow
            };

            var result = await _userManager.CreateAsync(user, model.Password);

            if (result.Succeeded)
            {
                await _userManager.AddToRoleAsync(user, DbSeeder.UserRole);
                await _signInManager.SignInAsync(user, isPersistent: false);

                // ✅ Welcome splash on registration
                TempData["WelcomeSplash"] = user.FullName;
                return RedirectToAction("Index", "Home");
            }

            foreach (var error in result.Errors)
            {
                ModelState.AddModelError("", error.Description);
            }

            return View(model);
        }

        [HttpGet]
        public IActionResult Login(string? returnUrl = null)
        {
            if (_signInManager.IsSignedIn(User))
                return RedirectToAction("Index", "Home");

            ViewData["ReturnUrl"] = returnUrl;
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Login(LoginViewModel model, string? returnUrl = null)
        {
            if (!ModelState.IsValid)
                return View(model);

            var existingUser = await _userManager.FindByEmailAsync(model.Email);
            if (existingUser != null && existingUser.IsBanned)
            {
                ModelState.AddModelError("",
                    "Your account has been suspended. Please contact support.");
                return View(model);
            }

            var result = await _signInManager.PasswordSignInAsync(
                model.Email, model.Password, model.RememberMe, lockoutOnFailure: true);

            if (result.Succeeded)
            {
                // ✅ Welcome splash
                var user = await _userManager.FindByEmailAsync(model.Email);
                TempData["WelcomeSplash"] = user?.FullName ?? "there";

                return RedirectToLocal(returnUrl);
            }

            if (result.IsLockedOut)
            {
                ModelState.AddModelError("",
                    "Account locked due to multiple failed attempts. Try again in 5 minutes.");
                return View(model);
            }

            ModelState.AddModelError("", "Invalid email or password.");
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Logout()
        {
            await _signInManager.SignOutAsync();
            TempData["Success"] = "You have been logged out.";
            return RedirectToAction("Index", "Home");
        }

        [HttpGet]
        public IActionResult AccessDenied() => View();

        private IActionResult RedirectToLocal(string? returnUrl)
        {
            if (!string.IsNullOrEmpty(returnUrl) && Url.IsLocalUrl(returnUrl))
                return Redirect(returnUrl);

            return RedirectToAction("Index", "Home");
        }
    }
}