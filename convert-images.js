const fs = require("fs-extra");
const path = require("path");
const matter = require("gray-matter");

const dir = path.join(__dirname, "anunci");

(async () => {
  const files = await fs.readdir(dir);
  const mdFiles = files.filter(file => file.endsWith(".md"));

  for (const file of mdFiles) {
    const filePath = path.join(dir, file);
    const content = await fs.readFile(filePath, "utf-8");
    const parsed = matter(content);

    const { data, content: body } = parsed;

    // Преобразуем только если старый формат
    if (
      Array.isArray(data.images) &&
      data.images.length &&
      typeof data.images[0] === "string"
    ) {
      data.images = data.images.map(src => ({ src, alt: "" }));

      const newFile = matter.stringify(body, data);
      await fs.writeFile(filePath, newFile, "utf-8");
      console.log(`✅ Обновлён: ${file}`);
    } else {
      console.log(`⏩ Пропущен (уже в новом формате или пусто): ${file}`);
    }
  }

  console.log("🎉 Все подходящие файлы обновлены!");
})();
