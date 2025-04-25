const fs = require("fs");
const path = require("path");

const inputPath = path.join(__dirname, "anunci/index2.json");
const outputPath = path.join(__dirname, "anunci/structured-annunci.json");

const raw = fs.readFileSync(inputPath, "utf-8");
const listings = JSON.parse(raw);
const now = new Date().toISOString();

function extractKeywords(annuncio) {
  const pool = [
    annuncio.nomeAnunci, annuncio.city1, annuncio.street1,
    annuncio.descrizione, annuncio.text1, annuncio.text2,
    annuncio.text3, annuncio.text4
  ].join(" ").toLowerCase();

  const words = pool.match(/[a-zà-ú]+/gi) || [];
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
    "@type": "Offer",
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": `https://italyscasa.com/anunci/?slug=${item.slug}`
    },
    "name": item.nomeAnunci || "",
    "description": item.descrizione || item.text1 || "",
    "price": item.prezzo || item.prezzo1 || "",
    "image": image,
    "inLanguage": "it",
    "isAccessibleForFree": true,
    "wordCount": wordCount,
    "keywords": extractKeywords(item),
    "address": {
      "@type": "PostalAddress",
      "addressLocality": item.city1 || "",
      "streetAddress": item.street1 || ""
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": parseFloat(item.latitude),
      "longitude": parseFloat(item.longitude)
    },
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
});

fs.writeFileSync(outputPath, JSON.stringify(structured, null, 2), "utf-8");
console.log("✅ structured-annunci.json сгенерирован!");
