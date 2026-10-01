using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace BloodConnect.Migrations
{
    /// <inheritdoc />
    public partial class AddBloodRequestOwner : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "UserId",
                table: "BloodRequests",
                type: "nvarchar(450)",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_BloodRequests_UserId",
                table: "BloodRequests",
                column: "UserId");

            // ✅ Raw SQL — EF Core ka onDelete bug avoid karne ke liye
            migrationBuilder.Sql(@"
                ALTER TABLE [BloodRequests]
                ADD CONSTRAINT [FK_BloodRequests_AspNetUsers_UserId]
                FOREIGN KEY ([UserId]) REFERENCES [AspNetUsers] ([Id])
                ON DELETE SET NULL;
            ");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_BloodRequests_AspNetUsers_UserId",
                table: "BloodRequests");

            migrationBuilder.DropIndex(
                name: "IX_BloodRequests_UserId",
                table: "BloodRequests");

            migrationBuilder.DropColumn(
                name: "UserId",
                table: "BloodRequests");
        }
    }
}