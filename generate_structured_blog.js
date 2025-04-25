const fs = require("fs");
const path = require("path");

const inputPath = path.join(__dirname, "blog/index.json");
const outputPath = path.join(__dirname, "blog/structured-blog.json");

const authorName = "Antonio Montano";
const authorUrl = "https://www.instagram.com/italyscasa?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==";
const logoUrl = "https://tonymontanait.github.io/italyscasa-content/uploads/logo.webp";
const sameAs = [
  "https://www.instagram.com/italyscasa?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==",
  "https://www.facebook.com/profile.php?id=61551668563870",
  "https://www.tiktok.com/@italyscasa1?is_from_webapp=1&sender_device=pc"
];

const raw = fs.readFileSync(inputPath, "utf-8");
const blogs = JSON.parse(raw);
const now = new Date().toISOString();

function extractKeywords(blog) {
  const pool = [
    blog.title, blog.tipo, blog.slug,
    blog.h1, blog.h2t1, blog.h2t2, blog.h2t3,
    blog.h2t4, blog.h2t5, blog.h2t6,
    blog.text1, blog.text2
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

function countWords(blog) {
  let total = 0;
  for (let i = 1; i <= 6; i++) {
    total += (blog[`text${i}`] || "").split(/\s+/).length;
  }
  return total;
}

const graph = blogs.map(blog => {
  const imageObj = blog.images?.[0] || { src: "uploads/default.jpg", alt: "" };
  return {
    "@type": "BlogPosting",
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": `https://italyscasa.com/blogpage/?slug=${blog.slug}`
    },
    "headline": blog.title || blog.h1 || "",
    "datePublished": now,
    "author": {
      "@type": "Person",
      "name": authorName,
      "url": authorUrl
    },
    "publisher": {
      "@type": "Organization",
      "name": "ItalysCasa",
      "logo": {
        "@type": "ImageObject",
        "url": logoUrl
      }
    },
    "image": `https://tonymontanait.github.io/italyscasa-content/${imageObj.src}`,
    "description": blog.text1 || "",
    "articleBody": [
      blog.text1, blog.text2, blog.text3,
      blog.text4, blog.text5, blog.text6
    ].filter(Boolean).join("\n"),
    "inLanguage": "it",
    "isAccessibleForFree": true,
    "wordCount": countWords(blog),
    "keywords": extractKeywords(blog),
    "sameAs": sameAs
  };
});

const structuredData = {
  "@context": "https://schema.org",
  "@graph": graph
};

fs.writeFileSync(outputPath, JSON.stringify(structuredData, null, 2), "utf-8");
console.log("✅ structured-blog.json сгенерирован!");
