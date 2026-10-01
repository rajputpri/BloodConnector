using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace BloodConnect.Migrations
{
    /// <inheritdoc />
    public partial class AddDonationOfferWorkflow : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_BloodRequests_AspNetUsers_UserId",
                table: "BloodRequests");

            migrationBuilder.CreateTable(
                name: "DonationOffers",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    RequestId = table.Column<int>(type: "int", nullable: false),
                    DonorId = table.Column<int>(type: "int", nullable: false),
                    Status = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false, defaultValue: "Pledged"),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false, defaultValueSql: "GETUTCDATE()"),
                    RespondedAt = table.Column<DateTime>(type: "datetime2", nullable: true),
                    CompletedAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DonationOffers", x => x.Id);
                    table.ForeignKey(
                        name: "FK_DonationOffers_BloodRequests_RequestId",
                        column: x => x.RequestId,
                        principalTable: "BloodRequests",
                        principalColumn: "RequestId",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_DonationOffers_Donors_DonorId",
                        column: x => x.DonorId,
                        principalTable: "Donors",
                        principalColumn: "DonorId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_DonationOffers_DonorId",
                table: "DonationOffers",
                column: "DonorId");

            migrationBuilder.CreateIndex(
                name: "IX_DonationOffers_RequestId_DonorId",
                table: "DonationOffers",
                columns: new[] { "RequestId", "DonorId" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_DonationOffers_Status",
                table: "DonationOffers",
                column: "Status");

            migrationBuilder.AddForeignKey(
                name: "FK_BloodRequests_AspNetUsers_UserId",
                table: "BloodRequests",
                column: "UserId",
                principalTable: "AspNetUsers",
                principalColumn: "Id",
                onDelete: ReferentialAction.SetNull);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_BloodRequests_AspNetUsers_UserId",
                table: "BloodRequests");

            migrationBuilder.DropTable(
                name: "DonationOffers");

            migrationBuilder.AddForeignKey(
                name: "FK_BloodRequests_AspNetUsers_UserId",
                table: "BloodRequests",
                column: "UserId",
                principalTable: "AspNetUsers",
                principalColumn: "Id");
        }
    }
}
