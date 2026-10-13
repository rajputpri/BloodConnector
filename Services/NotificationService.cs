using BloodConnect.Hubs;
using BloodConnect.Models;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;

namespace BloodConnect.Services
{
    /// <summary>
    /// Notification service — hybrid approach:
    /// • Cache: for initial page load (60s expiry)
    /// • SignalR: for real-time push on write operations
    /// • Explicit invalidation on every write
    /// </summary>
    public class NotificationService
    {
        private const int CacheDurationSeconds = 60;
        private const string AdminCacheKey = "BC_AdminNotifications";

        private readonly IMemoryCache _cache;
        private readonly ApplicationDbContext _context;
        private readonly IHubContext<NotificationHub> _hub;

        public NotificationService(
            IMemoryCache cache,
            ApplicationDbContext context,
            IHubContext<NotificationHub> hub)
        {
            _cache = cache;
            _context = context;
            _hub = hub;
        }

        // =============================================================
        // READ METHODS — for initial page load (bell dropdown content)
        // =============================================================

        public async Task<AdminNotification> GetAdminNotificationsAsync()
        {
            if (_cache.TryGetValue(AdminCacheKey, out AdminNotification? cached) && cached != null)
                return cached;

            var result = await BuildAdminNotificationAsync();
            _cache.Set(AdminCacheKey, result, TimeSpan.FromSeconds(CacheDurationSeconds));
            return result;
        }

        public async Task<UserNotification> GetUserNotificationsAsync(string userId)
        {
            if (string.IsNullOrEmpty(userId))
                return new UserNotification();

            string key = $"BC_UserNotif_{userId}";
            if (_cache.TryGetValue(key, out UserNotification? cached) && cached != null)
                return cached;

            var result = await BuildUserNotificationAsync(userId);
            _cache.Set(key, result, TimeSpan.FromSeconds(CacheDurationSeconds));
            return result;
        }

        // =============================================================
        // BUILDERS
        // =============================================================

        private async Task<AdminNotification> BuildAdminNotificationAsync()
        {
            var since = DateTime.UtcNow.AddDays(-3);

            var recentRequests = await _context.BloodRequests.AsNoTracking()
                .Where(r => r.Status == DomainValues.Open && r.RequestDate >= since)
                .OrderByDescending(r => r.RequestDate)
                .Take(4)
                .Select(r => new NotificationItem
                {
                    Type = "request",
                    Text = $"New {r.BloodGroupNeeded} request",
                    SubText = $"{r.RequesterName} · {r.Location}",
                    Timestamp = r.RequestDate,
                    Url = "/BloodRequest/Index"
                })
                .ToListAsync();

            var unreadMessages = await _context.ContactMessages.AsNoTracking()
                .Where(m => !m.IsRead)
                .OrderByDescending(m => m.CreatedAt)
                .Take(4)
                .Select(m => new NotificationItem
                {
                    Type = "message",
                    Text = $"Message from {m.Name}",
                    SubText = m.Subject,
                    Timestamp = m.CreatedAt,
                    Url = "/Admin/Messages"
                })
                .ToListAsync();

            int totalUnread = await _context.ContactMessages.CountAsync(m => !m.IsRead);
            int totalOpen = await _context.BloodRequests.CountAsync(r => r.Status == DomainValues.Open);

            return new AdminNotification
            {
                UnreadMessages = totalUnread,
                OpenRequests = totalOpen,
                TotalCount = totalUnread + totalOpen,
                Items = recentRequests.Concat(unreadMessages)
                    .OrderByDescending(x => x.Timestamp)
                    .Take(8)
                    .ToList()
            };
        }

        private async Task<UserNotification> BuildUserNotificationAsync(string userId)
        {
            var myRequestIds = await _context.BloodRequests.AsNoTracking()
                .Where(r => r.UserId == userId)
                .Select(r => r.RequestId)
                .ToListAsync();

            var pendingOffers = await _context.DonationOffers.AsNoTracking()
                .Include(o => o.Donor)
                .Include(o => o.Request)
                .Where(o => myRequestIds.Contains(o.RequestId) && o.Status == DomainValues.Pledged)
                .OrderByDescending(o => o.CreatedAt)
                .Take(8)
                .Select(o => new NotificationItem
                {
                    Type = "offer",
                    Text = $"{o.Donor.Name} ({o.Donor.BloodGroup}) wants to donate",
                    SubText = $"For request #{o.RequestId} — {o.Request.BloodGroupNeeded}",
                    Timestamp = o.CreatedAt,
                    Url = $"/BloodRequest/Offers/{o.RequestId}"
                })
                .ToListAsync();

            return new UserNotification
            {
                PendingOffers = pendingOffers.Count,
                TotalCount = pendingOffers.Count,
                Items = pendingOffers
            };
        }

        // =============================================================
        // PUSH METHODS — real-time via SignalR
        // =============================================================

        public async Task PushNewRequestToAdminsAsync(BloodRequest request)
        {
            _cache.Remove(AdminCacheKey);

            var payload = new
            {
                type = "request",
                title = $"New {request.BloodGroupNeeded} request",
                message = $"{request.RequesterName} · {request.Location}",
                url = "/BloodRequest/Index",
                timestamp = DateTime.UtcNow.ToString("o")
            };

            await _hub.Clients.Group("admins").SendAsync("ReceiveNotification", payload);
        }

        public async Task PushNewMessageToAdminsAsync(ContactMessage msg)
        {
            _cache.Remove(AdminCacheKey);

            var payload = new
            {
                type = "message",
                title = $"Message from {msg.Name}",
                message = msg.Subject,
                url = "/Admin/Messages",
                timestamp = DateTime.UtcNow.ToString("o")
            };

            await _hub.Clients.Group("admins").SendAsync("ReceiveNotification", payload);
        }

        public async Task PushNewOfferToOwnerAsync(BloodRequest request, DonationOffer offer)
        {
            if (string.IsNullOrEmpty(request.UserId)) return;

            _cache.Remove($"BC_UserNotif_{request.UserId}");

            var payload = new
            {
                type = "offer",
                title = $"{offer.Donor.Name} wants to donate!",
                message = $"Blood group {offer.Donor.BloodGroup} for request #{request.RequestId}",
                url = $"/BloodRequest/Offers/{request.RequestId}",
                timestamp = DateTime.UtcNow.ToString("o")
            };

            await _hub.Clients.Group($"user_{request.UserId}")
                .SendAsync("ReceiveNotification", payload);
        }

        public async Task PushOfferStatusToDonorAsync(string donorUserId, string status, int requestId)
        {
            if (string.IsNullOrEmpty(donorUserId)) return;

            var payload = new
            {
                type = "offer-status",
                title = status == DomainValues.Accepted
                    ? "Your offer was accepted!"
                    : $"Offer {status}",
                message = $"Request #{requestId} — {status}",
                url = "/Dashboard/Index",
                timestamp = DateTime.UtcNow.ToString("o")
            };

            await _hub.Clients.Group($"user_{donorUserId}")
                .SendAsync("ReceiveNotification", payload);
        }

        // =============================================================
        // INVALIDATION
        // =============================================================

        public void InvalidateAdmin() => _cache.Remove(AdminCacheKey);

        public void InvalidateUser(string userId)
        {
            if (!string.IsNullOrEmpty(userId))
                _cache.Remove($"BC_UserNotif_{userId}");
        }
    }

    // ============ DTOs ============
    public class NotificationItem
    {
        public string Type { get; set; } = "";
        public string Text { get; set; } = "";
        public string SubText { get; set; } = "";
        public DateTime Timestamp { get; set; }
        public string Url { get; set; } = "";
    }

    public class AdminNotification
    {
        public int UnreadMessages { get; set; }
        public int OpenRequests { get; set; }
        public int TotalCount { get; set; }
        public List<NotificationItem> Items { get; set; } = new();
    }

    public class UserNotification
    {
        public int PendingOffers { get; set; }
        public int TotalCount { get; set; }
        public List<NotificationItem> Items { get; set; } = new();
    }
}