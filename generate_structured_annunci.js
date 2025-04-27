// 📦 generate_structured_annunci.js - новая правильная версия!

const fs = require("fs");
const path = require("path");

const inputPath = path.join(__dirname, "anunci/index2.json");
const outputPath = path.join(__dirname, "anunci/structured-annunci.json");

const raw = fs.readFileSync(inputPath, "utf-8");
const listings = JSON.parse(raw);

function extractKeywords(annuncio) {
  const pool = [
    annuncio.nomeAnunci, annuncio.city1, annuncio.street1,
    annuncio.descrizione, annuncio.text1, annuncio.text2,
    annuncio.text3, annuncio.text4
  ].join(" ").toLowerCase();

  const words = pool.match(/[a-zÀ-ſ]+/gi) || [];
  const freq = {};
  words.forEach(w => {
    if (w.length > 3) freq[w] = (freq[w] || 0) + 1;
  });

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(entry => entry[0])
    .join(", ");
}

const structured = listings.map(item => {
  const image = item.images?.[0]?.src
    ? `https://tonymontanait.github.io/italyscasa-content/${item.images[0].src}`
    : "https://tonymontanait.github.io/italyscasa-content/uploads/default.jpg";

  const wordCount = [item.descrizione, item.text1, item.text2, item.text3, item.text4]
    .filter(Boolean)
    .join(" ")
    .split(/\s+/).length;

  return {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": item.nomeAnunci || "",
    "description": item.descrizione || item.text1 || "",
    "image": image,
    "offers": {
      "@type": "Offer",
      "url": `https://italyscasa.com/anunci/dynamic/?rif=${encodeURIComponent(item.riferimento || item.slug || '')}`,
      "price": parseFloat((item.prezzo || item.prezzo1 || "0").replace(/[^0-9.]/g, "")) || 0,
      "priceCurrency": "EUR",
      "availability": "https://schema.org/InStock"
    },
    "inLanguage": "it",
    "isAccessibleForFree": true,
    "wordCount": wordCount,
    "keywords": extractKeywords(item),
    "address": {
      "@type": "PostalAddress",
      "addressLocality": item.city1 || "",
      "streetAddress": item.street1 || ""
    },
    "geo": item.latitude && item.longitude ? {
      "@type": "GeoCoordinates",
      "latitude": parseFloat(item.latitude),
      "longitude": parseFloat(item.longitude)
    } : undefined,
    "publisher": {
      "@type": "Organization",
      "name": "ItalysCasa",
      "logo": {
        "@type": "ImageObject",
        "url": "https://tonymontanait.github.io/italyscasa-content/uploads/logo.webp"
      }
    },
    "sameAs": [
      "https://www.instagram.com/italyscasa?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==",
      "https://www.facebook.com/profile.php?id=61551668563870",
      "https://www.tiktok.com/@italyscasa1?is_from_webapp=1&sender_device=pc"
    ]
  };
}).map(obj => {
  // Чистим пустые ключи (например если нет координат)
  Object.keys(obj).forEach(key => {
    if (obj[key] === undefined) delete obj[key];
  });
  return obj;
});

fs.writeFileSync(outputPath, JSON.stringify(structured, null, 2), "utf-8");
console.log("\u2705 structured-annunci.json успешно сгенерирован по правильной схеме!");
