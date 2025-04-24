const fs = require("fs");
const path = require("path");

const inputPath = path.join(__dirname, "blog/index.json");
const outputPath = path.join(__dirname, "blog/structured-blog.json");

const authorName = "Antonio Montano";
const authorUrl = "https://www.instagram.com/tony_montana_it/profilecard/?igsh=eWU3MzBha2swMWVj";

const raw = fs.readFileSync(inputPath, "utf-8");
const blogs = JSON.parse(raw);

const now = new Date().toISOString();

const graph = blogs.map(blog => {
  const imageObj = blog.images?.[0] || { src: "uploads/default.jpg", alt: "" };
  return {
    "@type": "BlogPosting",
    "headline": blog.title || blog.h1 || "",
    "datePublished": now,
    "author": {
      "@type": "Person",
      "name": authorName,
      "url": authorUrl
    },
    "image": `https://tonymontanait.github.io/italyscasa-content/${imageObj.src}`,
    "description": blog.text1 || ""
  };
});

const structuredData = {
  "@context": "https://schema.org",
  "@graph": graph
};

fs.writeFileSync(outputPath, JSON.stringify(structuredData, null, 2), "utf-8");
console.log("✅ structured-blog.json сгенерирован!");
