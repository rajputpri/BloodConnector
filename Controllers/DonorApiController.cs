using Microsoft.AspNetCore.Mvc;
using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class DonorApiController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public DonorApiController(ApplicationDbContext context)
        {
            _context = context;
        }

        [HttpGet("search")]
        public async Task<IActionResult> Search(
            [FromQuery] string? bloodGroup,
            [FromQuery] string? location,
            [FromQuery] bool exactMatch = false,
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 20)
        {
            // Input sanitize
            page = page < 1 ? 1 : page;
            pageSize = pageSize is < 1 or > 100 ? 20 : pageSize;

            var query = _context.Donors
                .AsNoTracking()
                .Where(d => d.IsAvailable);

            // ✅ Blood group compatibility filter
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

            if (!string.IsNullOrWhiteSpace(location))
            {
                query = query.Where(d => d.Location.Contains(location));
            }

            var total = await query.CountAsync();

            // DTO projection — ContactNumber BAHAR
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
                    d.Location,
                    IsExactMatch = !string.IsNullOrEmpty(bloodGroup) && d.BloodGroup == bloodGroup
                    // ContactNumber jaan-boojh kar nahi bhej rahe
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
    }
}