using BloodConnect.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;

namespace BloodConnect.Services
{
    /// <summary>
    /// Cached access to unread ContactMessage count.
    /// Non-admins never hit this. Admins hit DB max once per 60s.
    /// Invalidated explicitly on write operations.
    /// </summary>
    public class MessageCache
    {
        private const string UnreadCountKey = "BloodConnect_ContactMessages_UnreadCount";
        private static readonly TimeSpan CacheDuration = TimeSpan.FromSeconds(60);

        private readonly IMemoryCache _cache;

        public MessageCache(IMemoryCache cache)
        {
            _cache = cache;
        }

        public async Task<int> GetUnreadCountAsync(ApplicationDbContext context)
        {
            if (_cache.TryGetValue(UnreadCountKey, out int cached))
                return cached;

            int count = await context.ContactMessages.CountAsync(m => !m.IsRead);
            _cache.Set(UnreadCountKey, count, CacheDuration);
            return count;
        }

        public void Invalidate()
        {
            _cache.Remove(UnreadCountKey);
        }
    }
}