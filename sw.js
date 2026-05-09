const CACHE = "kaoyan-v1";
const ASSETS = [
  "/kaoyan-countdown/",
  "/kaoyan-countdown/index.html",
  "/kaoyan-countdown/manifest.json",
  "/kaoyan-countdown/icon-192.png",
  "/kaoyan-countdown/icon-512.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then(
      (cached) => cached || fetch(e.request)
    )
  );
});
