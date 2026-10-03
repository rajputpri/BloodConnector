using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    [ApiController]
    [Route("api/bloodrequest")]
    [IgnoreAntiforgeryToken]
    public class BloodRequestApiController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<AppUser> _userManager;

        public BloodRequestApiController(
            ApplicationDbContext context,
            UserManager<AppUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        private static BloodRequestDto ToDto(BloodRequest r, bool includeContact = false) => new()
        {
            RequestId = r.RequestId,
            RequesterName = r.RequesterName,
            BloodGroupNeeded = r.BloodGroupNeeded,
            State = r.State,
            City = r.City,
            Location = r.Location,
            ContactNumber = includeContact ? r.ContactNumber : null,
            UrgencyLevel = r.UrgencyLevel,
            Status = r.Status,
            RequestDate = r.RequestDate
        };

        private static string BuildLocation(string? city, string state) =>
            string.IsNullOrWhiteSpace(city) ? state : $"{city.Trim()}, {state}";

        // =========================================================
        // GET /api/bloodrequest?bloodGroup=A%2B&urgency=Critical&status=Open
        // =========================================================
        [HttpGet]
        public async Task<IActionResult> GetAll(
            [FromQuery] string? bloodGroup,
            [FromQuery] string? urgency,
            [FromQuery] string? status,
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 20)
        {
            page = page < 1 ? 1 : page;
            pageSize = pageSize is < 1 or > 100 ? 20 : pageSize;

            var query = _context.BloodRequests.AsNoTracking().AsQueryable();

            if (!string.IsNullOrWhiteSpace(bloodGroup))
                query = query.Where(r => r.BloodGroupNeeded == bloodGroup);
            if (!string.IsNullOrWhiteSpace(urgency))
                query = query.Where(r => r.UrgencyLevel == urgency);
            if (!string.IsNullOrWhiteSpace(status))
                query = query.Where(r => r.Status == status);

            var total = await query.CountAsync();

            var items = await query
                .OrderByDescending(r => r.RequestDate)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .Select(r => new BloodRequestDto
                {
                    RequestId = r.RequestId,
                    RequesterName = r.RequesterName,
                    BloodGroupNeeded = r.BloodGroupNeeded,
                    State = r.State,
                    City = r.City,
                    Location = r.Location,
                    ContactNumber = null,
                    UrgencyLevel = r.UrgencyLevel,
                    Status = r.Status,
                    RequestDate = r.RequestDate
                })
                .ToListAsync();

            return Ok(new { total, page, pageSize, items });
        }

        // =========================================================
        // GET /api/bloodrequest/3
        // =========================================================
        [HttpGet("{id:int}")]
        public async Task<IActionResult> GetById(int id)
        {
            var r = await _context.BloodRequests.AsNoTracking()
                .FirstOrDefaultAsync(x => x.RequestId == id);

            if (r == null)
                return NotFound(new { error = "Blood request not found." });

            bool includeContact = User.Identity?.IsAuthenticated == true;
            return Ok(ToDto(r, includeContact));
        }

        // =========================================================
        // POST /api/bloodrequest
        // =========================================================
        [HttpPost]
        [Authorize]
        public async Task<IActionResult> Create([FromBody] CreateBloodRequestDto dto)
        {
            if (!DomainValues.IsValidState(dto.State))
                return BadRequest(new { error = "Invalid Indian state or union territory." });

            var userId = _userManager.GetUserId(User);

            var request = new BloodRequest
            {
                RequesterName = dto.RequesterName.Trim(),
                BloodGroupNeeded = dto.BloodGroupNeeded,
                State = dto.State.Trim(),
                City = string.IsNullOrWhiteSpace(dto.City) ? null : dto.City.Trim(),
                Location = BuildLocation(dto.City, dto.State),
                ContactNumber = dto.ContactNumber.Trim(),
                UrgencyLevel = dto.UrgencyLevel,
                Status = DomainValues.Open,
                RequestDate = DateTime.UtcNow,
                UserId = userId
            };

            _context.BloodRequests.Add(request);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById),
                new { id = request.RequestId }, ToDto(request, true));
        }

        // =========================================================
        // PUT /api/bloodrequest/3
        // =========================================================
        [HttpPut("{id:int}")]
        [Authorize]
        public async Task<IActionResult> Update(int id, [FromBody] UpdateBloodRequestDto dto)
        {
            var r = await _context.BloodRequests.FindAsync(id);
            if (r == null)
                return NotFound(new { error = "Blood request not found." });

            if (!DomainValues.IsValidState(dto.State))
                return BadRequest(new { error = "Invalid Indian state or union territory." });

            var userId = _userManager.GetUserId(User);
            bool isAdmin = User.IsInRole(DbSeeder.AdminRole)
                        || User.IsInRole(DbSeeder.SuperAdminRole);
            bool isOwner = !string.IsNullOrEmpty(userId) && r.UserId == userId;

            if (!isAdmin && !isOwner)
                return Forbid();

            if (r.Status == DomainValues.Fulfilled)
                return BadRequest(new { error = "Fulfilled requests cannot be edited." });

            r.RequesterName = dto.RequesterName.Trim();
            r.BloodGroupNeeded = dto.BloodGroupNeeded;
            r.State = dto.State.Trim();
            r.City = string.IsNullOrWhiteSpace(dto.City) ? null : dto.City.Trim();
            r.Location = BuildLocation(dto.City, dto.State);
            r.ContactNumber = dto.ContactNumber.Trim();
            r.UrgencyLevel = dto.UrgencyLevel;

            await _context.SaveChangesAsync();
            return Ok(ToDto(r, true));
        }

        // =========================================================
        // DELETE /api/bloodrequest/3
        // =========================================================
        [HttpDelete("{id:int}")]
        [Authorize]
        public async Task<IActionResult> Delete(int id)
        {
            var r = await _context.BloodRequests.FindAsync(id);
            if (r == null)
                return NotFound(new { error = "Blood request not found." });

            var userId = _userManager.GetUserId(User);
            bool isAdmin = User.IsInRole(DbSeeder.AdminRole)
                        || User.IsInRole(DbSeeder.SuperAdminRole);
            bool isOwner = !string.IsNullOrEmpty(userId) && r.UserId == userId;

            if (!isAdmin && !isOwner)
                return Forbid();

            _context.BloodRequests.Remove(r);
            await _context.SaveChangesAsync();
            return NoContent();
        }
    }
}