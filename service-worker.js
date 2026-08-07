/* ==============================================
   BLACK ARROW VENTURE — SERVICE WORKER (RETIREMENT SHIM)
   ==============================================

   This file used to be a cache-first service worker. It had two faults that
   made it actively harmful:

   1. It precached '/assets/images/logo.png', which does not exist. cache.addAll()
      rejects atomically, so the precache never ran. But skipWaiting() sat
      OUTSIDE waitUntil(), so the worker activated anyway with an empty cache.

   2. It then served CSS, JS and images cache-first with no revalidation and
      no cache-busting. Returning visitors were pinned to whatever assets they
      first downloaded, permanently, and Vercel's own cache headers were
      bypassed entirely.

   For a static brochure site on Vercel's CDN a service worker buys very little
   and costs a whole class of "why is the site stale" bugs. So it is retired.

   IMPORTANT: deleting this file would NOT retire it. Browsers that already
   registered the old worker keep running it. This shim replaces the old
   worker, clears every cache it created, unregisters itself, and reloads open
   tabs so they pick up the real network responses. The registration call in
   index.html stays for one release so existing clients actually receive this.
   ============================================== */

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    // Drop every cache this origin created, including the old 'eightstar-v2'.
    const keys = await caches.keys();
    await Promise.all(keys.map((k) => caches.delete(k)));

    await self.registration.unregister();

    // Reload open tabs so they stop being controlled by a dead worker.
    const clients = await self.clients.matchAll({ type: 'window' });
    for (const client of clients) {
      client.navigate(client.url);
    }
  })());
});

// No fetch handler at all — every request passes straight through to the
// network and to Vercel's cache headers.
