using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using System.ComponentModel.DataAnnotations;

namespace BloodConnect.Controllers
{
    [ApiController]
    [Route("api/auth")]
    [IgnoreAntiforgeryToken]
    public class AuthApiController : ControllerBase
    {
        private readonly SignInManager<AppUser> _signInManager;
        private readonly UserManager<AppUser> _userManager;

        public AuthApiController(
            SignInManager<AppUser> signInManager,
            UserManager<AppUser> userManager)
        {
            _signInManager = signInManager;
            _userManager = userManager;
        }

        // =========================================================
        // POST /api/auth/login
        // =========================================================
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginApiDto dto)
        {
            if (!ModelState.IsValid)
                return BadRequest(new { error = "Email and password are required." });

            var user = await _userManager.FindByEmailAsync(dto.Email);
            if (user == null)
                return Unauthorized(new { error = "Invalid credentials." });

            if (user.IsBanned)
                return Unauthorized(new { error = "Account is banned." });

            var result = await _signInManager.PasswordSignInAsync(
                user, dto.Password, isPersistent: true, lockoutOnFailure: true);

            if (result.Succeeded)
            {
                return Ok(new
                {
                    message = "Login successful.",
                    email = user.Email,
                    fullName = user.FullName
                });
            }

            if (result.IsLockedOut)
                return StatusCode(423, new { error = "Account locked. Try again in 5 minutes." });

            return Unauthorized(new { error = "Invalid credentials." });
        }

        // =========================================================
        // POST /api/auth/logout
        // =========================================================
        [HttpPost("logout")]
        [Authorize]
        public async Task<IActionResult> Logout()
        {
            await _signInManager.SignOutAsync();
            return Ok(new { message = "Logged out successfully." });
        }

        // =========================================================
        // GET /api/auth/me
        // =========================================================
        [HttpGet("me")]
        [Authorize]
        public async Task<IActionResult> Me()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null)
                return Unauthorized();

            var roles = await _userManager.GetRolesAsync(user);

            return Ok(new
            {
                email = user.Email,
                fullName = user.FullName,
                roles,
                createdAt = user.CreatedAt
            });
        }
    }

    public class LoginApiDto
    {
        [Required(ErrorMessage = "Email is required.")]
        [EmailAddress(ErrorMessage = "Invalid email format.")]
        public string Email { get; set; } = "";

        [Required(ErrorMessage = "Password is required.")]
        public string Password { get; set; } = "";
    }
}