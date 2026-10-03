using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace BloodConnect.Migrations
{
    /// <inheritdoc />
    public partial class AddStateCityToDonorAndRequest : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "City",
                table: "Donors",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "State",
                table: "Donors",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "City",
                table: "BloodRequests",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "State",
                table: "BloodRequests",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_Donors_State",
                table: "Donors",
                column: "State");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_Donors_State",
                table: "Donors");

            migrationBuilder.DropColumn(
                name: "City",
                table: "Donors");

            migrationBuilder.DropColumn(
                name: "State",
                table: "Donors");

            migrationBuilder.DropColumn(
                name: "City",
                table: "BloodRequests");

            migrationBuilder.DropColumn(
                name: "State",
                table: "BloodRequests");
        }
    }
}
