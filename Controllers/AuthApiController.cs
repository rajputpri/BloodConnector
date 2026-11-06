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
        // POST /api/auth/register   ← 🆕 NAYA ENDPOINT
        // =========================================================
        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterApiDto dto)
        {
            if (!ModelState.IsValid)
                return BadRequest(new { error = "Invalid data.", details = ModelState });

            var existing = await _userManager.FindByEmailAsync(dto.Email);
            if (existing != null)
                return Conflict(new { error = "Email already registered." });

            var user = new AppUser
            {
                UserName = dto.Email,
                Email = dto.Email,
                FullName = string.IsNullOrWhiteSpace(dto.FullName)
                            ? dto.Email.Split('@')[0]
                            : dto.FullName,
                EmailConfirmed = true,
                CreatedAt = DateTime.UtcNow
            };

            var result = await _userManager.CreateAsync(user, dto.Password);

            if (!result.Succeeded)
                return BadRequest(new
                {
                    error = "Registration failed.",
                    details = result.Errors.Select(e => e.Description)
                });

            await _userManager.AddToRoleAsync(user, DbSeeder.UserRole);

            return Ok(new
            {
                message = "User registered successfully.",
                userId = user.Id,
                email = user.Email,
                fullName = user.FullName
            });
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

    // =========================================================
    // DTOs
    // =========================================================
    public class LoginApiDto
    {
        [Required(ErrorMessage = "Email is required.")]
        [EmailAddress(ErrorMessage = "Invalid email format.")]
        public string Email { get; set; } = "";

        [Required(ErrorMessage = "Password is required.")]
        public string Password { get; set; } = "";
    }

    // 🆕 Register DTO
    public class RegisterApiDto
    {
        [Required(ErrorMessage = "Email is required.")]
        [EmailAddress(ErrorMessage = "Invalid email format.")]
        public string Email { get; set; } = "";

        [Required(ErrorMessage = "Password is required.")]
        [MinLength(6, ErrorMessage = "Password must be at least 6 characters.")]
        public string Password { get; set; } = "";

        public string? FullName { get; set; }
    }
}