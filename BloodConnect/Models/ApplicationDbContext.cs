using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Models
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        public DbSet<Donor> Donors { get; set; }
        public DbSet<BloodRequest> BloodRequests { get; set; }
    }
}