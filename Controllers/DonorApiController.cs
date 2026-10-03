using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    [ApiController]
    [Route("api/donor")]
    [IgnoreAntiforgeryToken]  // REST clients ke liye — Postman CSRF token nahi bhejta
    public class DonorApiController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<AppUser> _userManager;

        public DonorApiController(
            ApplicationDbContext context,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        private static DonorDto ToDto(Donor d, bool includeContact = false) => new()
        {
            DonorId = d.DonorId,
            Name = d.Name,
            BloodGroup = d.BloodGroup,
            Age = d.Age,
            State = d.State,
            City = d.City,
            Location = d.Location,
            IsAvailable = d.IsAvailable,
            ContactNumber = includeContact ? d.ContactNumber : null
        };

        private static string BuildLocation(string? city, string state) =>
            string.IsNullOrWhiteSpace(city) ? state : $"{city.Trim()}, {state}";

        // =========================================================
        // GET /api/donor?bloodGroup=O%2B&state=Gujarat&available=true&page=1&pageSize=20
        // =========================================================
        [HttpGet]
        public async Task<IActionResult> GetAll(
            [FromQuery] string? bloodGroup,
            [FromQuery] string? state,
            [FromQuery] bool? available,
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 20)
        {
            page = page < 1 ? 1 : page;
            pageSize = pageSize is < 1 or > 100 ? 20 : pageSize;

            var query = _context.Donors.AsNoTracking().AsQueryable();

            if (!string.IsNullOrWhiteSpace(bloodGroup))
                query = query.Where(d => d.BloodGroup == bloodGroup);

            if (!string.IsNullOrWhiteSpace(state) && DomainValues.IsValidState(state))
                query = query.Where(d => d.State == state);

            if (available.HasValue)
                query = query.Where(d => d.IsAvailable == available.Value);

            var total = await query.CountAsync();

            var items = await query
                .OrderByDescending(d => d.DonorId)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .Select(d => new DonorDto
                {
                    DonorId = d.DonorId,
                    Name = d.Name,
                    BloodGroup = d.BloodGroup,
                    Age = d.Age,
                    State = d.State,
                    City = d.City,
                    Location = d.Location,
                    IsAvailable = d.IsAvailable,
                    ContactNumber = null
                })
                .ToListAsync();

            return Ok(new { total, page, pageSize, items });
        }

        // =========================================================
        // GET /api/donor/5
        // =========================================================
        [HttpGet("{id:int}")]
        public async Task<IActionResult> GetById(int id)
        {
            var donor = await _context.Donors.AsNoTracking()
                .FirstOrDefaultAsync(d => d.DonorId == id);

            if (donor == null)
                return NotFound(new { error = "Donor not found." });

            // Contact number sensitive — authenticated user ko hi dikhao
            bool includeContact = User.Identity?.IsAuthenticated == true;

            return Ok(ToDto(donor, includeContact));
        }

        // =========================================================
        // GET /api/donor/search?bloodGroup=A%2B&state=Gujarat&exactMatch=false
        // =========================================================
        [HttpGet("search")]
        public async Task<IActionResult> Search(
            [FromQuery] string? bloodGroup,
            [FromQuery] string? location,
            [FromQuery] string? state,
            [FromQuery] bool exactMatch = false,
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 20)
        {
            page = page < 1 ? 1 : page;
            pageSize = pageSize is < 1 or > 100 ? 20 : pageSize;

            var query = _context.Donors.AsNoTracking().Where(d => d.IsAvailable);
            var compatibleGroups = new List<string>();

            if (!string.IsNullOrWhiteSpace(bloodGroup) && BloodCompatibility.IsValid(bloodGroup))
            {
                if (exactMatch)
                {
                    query = query.Where(d => d.BloodGroup == bloodGroup);
                    compatibleGroups.Add(bloodGroup);
                }
                else
                {
                    var groups = BloodCompatibility.CompatibleDonorsFor(bloodGroup).ToList();
                    query = query.Where(d => groups.Contains(d.BloodGroup));
                    compatibleGroups = groups;
                }
            }

            if (!string.IsNullOrWhiteSpace(state) && DomainValues.IsValidState(state))
                query = query.Where(d => d.State == state
                    || (d.State == null && d.Location.Contains(state)));

            if (!string.IsNullOrWhiteSpace(location))
                query = query.Where(d => d.Location.Contains(location));

            var total = await query.CountAsync();

            var results = await query
                .OrderByDescending(d => d.BloodGroup == bloodGroup)
                .ThenBy(d => d.Name)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .Select(d => new
                {
                    d.DonorId,
                    d.Name,
                    d.BloodGroup,
                    d.State,
                    d.City,
                    d.Location,
                    IsExactMatch = !string.IsNullOrEmpty(bloodGroup) && d.BloodGroup == bloodGroup
                })
                .ToListAsync();

            return Ok(new
            {
                total,
                page,
                pageSize,
                searchMode = exactMatch ? "exact" : "compatible",
                requestedBloodGroup = bloodGroup,
                compatibleGroups,
                results
            });
        }

        // =========================================================
        // POST /api/donor
        // =========================================================
        [HttpPost]
        [Authorize]
        public async Task<IActionResult> Create([FromBody] CreateDonorDto dto)
        {
            if (!DomainValues.IsValidState(dto.State))
                return BadRequest(new { error = "Invalid Indian state or union territory." });

            var userId = _userManager.GetUserId(User);

            // Ek user ek hi donor profile bana sakta hai
            if (!string.IsNullOrEmpty(userId) &&
                await _context.Donors.AnyAsync(d => d.UserId == userId))
                return Conflict(new { error = "You already have a donor profile." });

            var donor = new Donor
            {
                Name = dto.Name.Trim(),
                Age = dto.Age,
                BloodGroup = dto.BloodGroup,
                State = dto.State.Trim(),
                City = string.IsNullOrWhiteSpace(dto.City) ? null : dto.City.Trim(),
                Location = BuildLocation(dto.City, dto.State),
                ContactNumber = dto.ContactNumber.Trim(),
                IsAvailable = dto.IsAvailable,
                UserId = userId
            };

            _context.Donors.Add(donor);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById),
                new { id = donor.DonorId }, ToDto(donor, true));
        }

        // =========================================================
        // PUT /api/donor/5
        // =========================================================
        [HttpPut("{id:int}")]
        [Authorize]
        public async Task<IActionResult> Update(int id, [FromBody] UpdateDonorDto dto)
        {
            var donor = await _context.Donors.FindAsync(id);
            if (donor == null)
                return NotFound(new { error = "Donor not found." });

            if (!DomainValues.IsValidState(dto.State))
                return BadRequest(new { error = "Invalid Indian state or union territory." });

            var userId = _userManager.GetUserId(User);
            bool isAdmin = User.IsInRole(DbSeeder.AdminRole)
                        || User.IsInRole(DbSeeder.SuperAdminRole);
            bool isOwner = !string.IsNullOrEmpty(userId) && donor.UserId == userId;

            if (!isAdmin && !isOwner)
                return Forbid();

            donor.Name = dto.Name.Trim();
            donor.Age = dto.Age;
            donor.BloodGroup = dto.BloodGroup;
            donor.State = dto.State.Trim();
            donor.City = string.IsNullOrWhiteSpace(dto.City) ? null : dto.City.Trim();
            donor.Location = BuildLocation(dto.City, dto.State);
            donor.ContactNumber = dto.ContactNumber.Trim();
            donor.IsAvailable = dto.IsAvailable;

            await _context.SaveChangesAsync();
            return Ok(ToDto(donor, true));
        }

        // =========================================================
        // DELETE /api/donor/5
        // =========================================================
        [HttpDelete("{id:int}")]
        [Authorize]
        public async Task<IActionResult> Delete(int id)
        {
            var donor = await _context.Donors.FindAsync(id);
            if (donor == null)
                return NotFound(new { error = "Donor not found." });

            var userId = _userManager.GetUserId(User);
            bool isAdmin = User.IsInRole(DbSeeder.AdminRole)
                        || User.IsInRole(DbSeeder.SuperAdminRole);
            bool isOwner = !string.IsNullOrEmpty(userId) && donor.UserId == userId;

            if (!isAdmin && !isOwner)
                return Forbid();

            _context.Donors.Remove(donor);
            await _context.SaveChangesAsync();
            return NoContent();
        }
    }
}