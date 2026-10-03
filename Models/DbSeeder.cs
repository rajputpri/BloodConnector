using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace BloodConnect.Models;

public static class DbSeeder
{
    public const string SuperAdminRole = "SuperAdmin";
    public const string AdminRole = "Admin";
    public const string UserRole = "User";

    public static async Task SeedAsync(
        ApplicationDbContext context,
        UserManager<AppUser> userManager,
        RoleManager<IdentityRole> roleManager)
    {
        // Step 1: Roles banao
        await SeedRolesAsync(roleManager);

        // Step 2: Admin user banao (SuperAdmin + Admin dono roles)
        await SeedAdminUserAsync(userManager);

        // Step 3: Sample donors
        await SeedDonorsAsync(context);
    }

    private static async Task SeedRolesAsync(RoleManager<IdentityRole> roleManager)
    {
        // Order matters: SuperAdmin pehle, phir Admin, phir User
        string[] roles = { SuperAdminRole, AdminRole, UserRole };

        foreach (var role in roles)
        {
            if (!await roleManager.RoleExistsAsync(role))
            {
                await roleManager.CreateAsync(new IdentityRole(role));
            }
        }
    }

    private static async Task SeedAdminUserAsync(UserManager<AppUser> userManager)
    {
        const string adminEmail = "admin@bloodconnect.com";
        const string adminPassword = "Admin@123";

        var admin = await userManager.FindByEmailAsync(adminEmail);

        if (admin == null)
        {
            // Fresh seed — create admin
            admin = new AppUser
            {
                UserName = adminEmail,
                Email = adminEmail,
                EmailConfirmed = true,
                FullName = "Administrator",
                CreatedAt = DateTime.UtcNow
            };

            var result = await userManager.CreateAsync(admin, adminPassword);
            if (!result.Succeeded) return;
        }

        // ✅ Ensure Admin role (existing old admin ke liye bhi)
        if (!await userManager.IsInRoleAsync(admin, AdminRole))
        {
            await userManager.AddToRoleAsync(admin, AdminRole);
        }

        // ✅ Ensure SuperAdmin role (new addition — old admin ko upgrade)
        if (!await userManager.IsInRoleAsync(admin, SuperAdminRole))
        {
            await userManager.AddToRoleAsync(admin, SuperAdminRole);
        }
    }

    private static async Task SeedDonorsAsync(ApplicationDbContext context)
    {
        if (await context.Donors.AnyAsync()) return;

        var donors = new[]
        {
            new Donor { Name = "Pawan",      BloodGroup = "AB-", State = "Bihar",       Location = "Bihar",       ContactNumber = "1234567890", IsAvailable = true },
            new Donor { Name = "Ravi Kumar", BloodGroup = "O+",  State = "Gujarat",     Location = "Gujarat",     ContactNumber = "4535393458", IsAvailable = true },
            new Donor { Name = "Ramesh",     BloodGroup = "B+",  State = "Maharashtra", Location = "Maharashtra", ContactNumber = "9876543210", IsAvailable = true },
        };

        context.Donors.AddRange(donors);
        await context.SaveChangesAsync();
    }
}
