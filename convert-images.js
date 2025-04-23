const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");

const folder = path.join(__dirname, "blog");

fs.readdirSync(folder).forEach(file => {
  if (!file.endsWith(".md")) return;

  const filePath = path.join(folder, file);
  const content = fs.readFileSync(filePath, "utf8");
  const parsed = matter(content);

  const images = parsed.data.images;

  if (Array.isArray(images) && images.every(img => typeof img === "string")) {
    parsed.data.images = images.map(src => ({ src, alt: "" }));

    const updatedContent = matter.stringify(parsed.content, parsed.data);
    fs.writeFileSync(filePath, updatedContent, "utf8");
    console.log(`✅ Aggiornato: ${file}`);
  }
});
