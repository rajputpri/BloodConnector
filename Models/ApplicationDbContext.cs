using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Models
{
    public class ApplicationDbContext : IdentityDbContext<AppUser>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Donor> Donors => Set<Donor>();
        public DbSet<BloodRequest> BloodRequests => Set<BloodRequest>();
        public DbSet<DonationOffer> DonationOffers => Set<DonationOffer>();
        public DbSet<ContactMessage> ContactMessages => Set<ContactMessage>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // ----- Donor Configuration -----
            modelBuilder.Entity<Donor>(entity =>
            {
                entity.HasKey(d => d.DonorId);

                entity.Property(d => d.Name).IsRequired().HasMaxLength(100);
                entity.Property(d => d.BloodGroup).IsRequired().HasMaxLength(3);

                // ✅ FIXED — C# me [Required] hai (form validation), but EF ke liye nullable
                // (legacy data me NULL hai, warna crash)
                entity.Property(d => d.State).IsRequired(false).HasMaxLength(100);
                entity.Property(d => d.City).HasMaxLength(50);

                entity.Property(d => d.Location).IsRequired().HasMaxLength(100);
                entity.Property(d => d.ContactNumber).IsRequired().HasMaxLength(10);

                entity.HasOne(d => d.User)
                    .WithMany()
                    .HasForeignKey(d => d.UserId)
                    .OnDelete(DeleteBehavior.SetNull);

                entity.HasIndex(d => d.BloodGroup);
                entity.HasIndex(d => d.State);
                entity.HasIndex(d => d.Location);
                entity.HasIndex(d => new { d.BloodGroup, d.IsAvailable });
                entity.HasIndex(d => d.UserId);
            });

            // ----- BloodRequest Configuration -----
            modelBuilder.Entity<BloodRequest>(entity =>
            {
                entity.HasKey(r => r.RequestId);

                entity.Property(r => r.RequesterName).IsRequired().HasMaxLength(100);
                entity.Property(r => r.BloodGroupNeeded).IsRequired().HasMaxLength(3);

                // ✅ FIXED — same treatment (form validation [Required], EF nullable)
                entity.Property(r => r.State).IsRequired(false).HasMaxLength(100);
                entity.Property(r => r.City).HasMaxLength(50);

                entity.Property(r => r.Location).IsRequired().HasMaxLength(100);
                entity.Property(r => r.ContactNumber).IsRequired().HasMaxLength(10);
                entity.Property(r => r.UrgencyLevel).IsRequired().HasMaxLength(20);
                entity.Property(r => r.Status).IsRequired().HasMaxLength(20)
                    .HasDefaultValue(DomainValues.Open);
                entity.Property(r => r.RequestDate).HasDefaultValueSql("GETUTCDATE()");

                entity.HasOne(r => r.FulfilledByDonor)
                    .WithMany()
                    .HasForeignKey(r => r.FulfilledByDonorId)
                    .OnDelete(DeleteBehavior.SetNull);

                entity.HasOne(r => r.User)
                    .WithMany()
                    .HasForeignKey(r => r.UserId)
                    .OnDelete(DeleteBehavior.SetNull);

                entity.HasIndex(r => r.UserId);
                entity.HasIndex(r => r.BloodGroupNeeded);
                entity.HasIndex(r => r.Status);
                entity.HasIndex(r => r.RequestDate);
                entity.HasIndex(r => new { r.Status, r.BloodGroupNeeded });
            });

            // ✅ DonationOffer Configuration
            modelBuilder.Entity<DonationOffer>(entity =>
            {
                entity.HasKey(o => o.Id);

                entity.Property(o => o.Status)
                    .IsRequired()
                    .HasMaxLength(20)
                    .HasDefaultValue(DomainValues.Pledged);

                entity.Property(o => o.CreatedAt)
                    .HasDefaultValueSql("GETUTCDATE()");

                entity.HasOne(o => o.Request)
                    .WithMany(r => r.Offers)
                    .HasForeignKey(o => o.RequestId)
                    .OnDelete(DeleteBehavior.Cascade);

                entity.HasOne(o => o.Donor)
                    .WithMany()
                    .HasForeignKey(o => o.DonorId)
                    .OnDelete(DeleteBehavior.Cascade);

                entity.HasIndex(o => new { o.RequestId, o.DonorId }).IsUnique();
                entity.HasIndex(o => o.Status);
                entity.HasIndex(o => o.DonorId);
            });

            // ✅ ContactMessage Configuration
            modelBuilder.Entity<ContactMessage>(entity =>
            {
                entity.HasKey(c => c.Id);

                entity.Property(c => c.Name).IsRequired().HasMaxLength(100);
                entity.Property(c => c.Email).IsRequired().HasMaxLength(150);
                entity.Property(c => c.Subject).IsRequired().HasMaxLength(150);
                entity.Property(c => c.Message).IsRequired().HasMaxLength(2000);

                entity.Property(c => c.CreatedAt)
                    .HasDefaultValueSql("GETUTCDATE()");

                entity.Property(c => c.IsRead)
                    .HasDefaultValue(false);

                entity.HasIndex(c => c.IsRead);
                entity.HasIndex(c => c.CreatedAt);
            });
        }
    }
}