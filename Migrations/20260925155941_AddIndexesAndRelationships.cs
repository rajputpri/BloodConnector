using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace BloodConnect.Migrations
{
    /// <inheritdoc />
    public partial class AddIndexesAndRelationships : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterColumn<string>(
                name: "Name",
                table: "Donors",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "Location",
                table: "Donors",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "ContactNumber",
                table: "Donors",
                type: "nvarchar(10)",
                maxLength: 10,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "BloodGroup",
                table: "Donors",
                type: "nvarchar(3)",
                maxLength: 3,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AddColumn<byte[]>(
                name: "RowVersion",
                table: "Donors",
                type: "rowversion",
                rowVersion: true,
                nullable: false,
                defaultValue: new byte[0]);

            migrationBuilder.AlterColumn<string>(
                name: "UrgencyLevel",
                table: "BloodRequests",
                type: "nvarchar(20)",
                maxLength: 20,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "Status",
                table: "BloodRequests",
                type: "nvarchar(20)",
                maxLength: 20,
                nullable: false,
                defaultValue: "Open",
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "RequesterName",
                table: "BloodRequests",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<DateTime>(
                name: "RequestDate",
                table: "BloodRequests",
                type: "datetime2",
                nullable: false,
                defaultValueSql: "GETUTCDATE()",
                oldClrType: typeof(DateTime),
                oldType: "datetime2");

            migrationBuilder.AlterColumn<string>(
                name: "Location",
                table: "BloodRequests",
                type: "nvarchar(100)",
                maxLength: 100,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "ContactNumber",
                table: "BloodRequests",
                type: "nvarchar(10)",
                maxLength: 10,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AlterColumn<string>(
                name: "BloodGroupNeeded",
                table: "BloodRequests",
                type: "nvarchar(3)",
                maxLength: 3,
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.CreateIndex(
                name: "IX_Donors_BloodGroup",
                table: "Donors",
                column: "BloodGroup");

            migrationBuilder.CreateIndex(
                name: "IX_Donors_BloodGroup_IsAvailable",
                table: "Donors",
                columns: new[] { "BloodGroup", "IsAvailable" });

            migrationBuilder.CreateIndex(
                name: "IX_Donors_Location",
                table: "Donors",
                column: "Location");

            migrationBuilder.CreateIndex(
                name: "IX_BloodRequests_BloodGroupNeeded",
                table: "BloodRequests",
                column: "BloodGroupNeeded");

            migrationBuilder.CreateIndex(
                name: "IX_BloodRequests_FulfilledByDonorId",
                table: "BloodRequests",
                column: "FulfilledByDonorId");

            migrationBuilder.CreateIndex(
                name: "IX_BloodRequests_RequestDate",
                table: "BloodRequests",
                column: "RequestDate");

            migrationBuilder.CreateIndex(
                name: "IX_BloodRequests_Status",
                table: "BloodRequests",
                column: "Status");

            migrationBuilder.CreateIndex(
                name: "IX_BloodRequests_Status_BloodGroupNeeded",
                table: "BloodRequests",
                columns: new[] { "Status", "BloodGroupNeeded" });

            migrationBuilder.AddForeignKey(
                name: "FK_BloodRequests_Donors_FulfilledByDonorId",
                table: "BloodRequests",
                column: "FulfilledByDonorId",
                principalTable: "Donors",
                principalColumn: "DonorId",
                onDelete: ReferentialAction.SetNull);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_BloodRequests_Donors_FulfilledByDonorId",
                table: "BloodRequests");

            migrationBuilder.DropIndex(
                name: "IX_Donors_BloodGroup",
                table: "Donors");

            migrationBuilder.DropIndex(
                name: "IX_Donors_BloodGroup_IsAvailable",
                table: "Donors");

            migrationBuilder.DropIndex(
                name: "IX_Donors_Location",
                table: "Donors");

            migrationBuilder.DropIndex(
                name: "IX_BloodRequests_BloodGroupNeeded",
                table: "BloodRequests");

            migrationBuilder.DropIndex(
                name: "IX_BloodRequests_FulfilledByDonorId",
                table: "BloodRequests");

            migrationBuilder.DropIndex(
                name: "IX_BloodRequests_RequestDate",
                table: "BloodRequests");

            migrationBuilder.DropIndex(
                name: "IX_BloodRequests_Status",
                table: "BloodRequests");

            migrationBuilder.DropIndex(
                name: "IX_BloodRequests_Status_BloodGroupNeeded",
                table: "BloodRequests");

            migrationBuilder.DropColumn(
                name: "RowVersion",
                table: "Donors");

            migrationBuilder.AlterColumn<string>(
                name: "Name",
                table: "Donors",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(100)",
                oldMaxLength: 100);

            migrationBuilder.AlterColumn<string>(
                name: "Location",
                table: "Donors",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(100)",
                oldMaxLength: 100);

            migrationBuilder.AlterColumn<string>(
                name: "ContactNumber",
                table: "Donors",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(10)",
                oldMaxLength: 10);

            migrationBuilder.AlterColumn<string>(
                name: "BloodGroup",
                table: "Donors",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(3)",
                oldMaxLength: 3);

            migrationBuilder.AlterColumn<string>(
                name: "UrgencyLevel",
                table: "BloodRequests",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(20)",
                oldMaxLength: 20);

            migrationBuilder.AlterColumn<string>(
                name: "Status",
                table: "BloodRequests",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(20)",
                oldMaxLength: 20,
                oldDefaultValue: "Open");

            migrationBuilder.AlterColumn<string>(
                name: "RequesterName",
                table: "BloodRequests",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(100)",
                oldMaxLength: 100);

            migrationBuilder.AlterColumn<DateTime>(
                name: "RequestDate",
                table: "BloodRequests",
                type: "datetime2",
                nullable: false,
                oldClrType: typeof(DateTime),
                oldType: "datetime2",
                oldDefaultValueSql: "GETUTCDATE()");

            migrationBuilder.AlterColumn<string>(
                name: "Location",
                table: "BloodRequests",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(100)",
                oldMaxLength: 100);

            migrationBuilder.AlterColumn<string>(
                name: "ContactNumber",
                table: "BloodRequests",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(10)",
                oldMaxLength: 10);

            migrationBuilder.AlterColumn<string>(
                name: "BloodGroupNeeded",
                table: "BloodRequests",
                type: "nvarchar(max)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "nvarchar(3)",
                oldMaxLength: 3);
        }
    }
}
