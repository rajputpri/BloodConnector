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

            migrationBuilder.AddForeignKey(
                name: "FK_BloodRequests_AspNetUsers_UserId",
                table: "BloodRequests",
                column: "UserId",
                principalTable: "AspNetUsers",
                principalColumn: "Id",
                onDelete: ReferentialAction.SetNull);   // ✅ YEH LINE ADD HUI
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
