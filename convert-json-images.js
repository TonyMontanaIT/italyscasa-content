const fs = require("fs-extra");
const path = require("path");

const filePath = path.join(__dirname, "anunci", "index2.json");

(async () => {
  try {
    const data = await fs.readJson(filePath);

    const updated = data.map(item => {
      if (
        Array.isArray(item.images) &&
        item.images.length &&
        typeof item.images[0] === "string"
      ) {
        return {
          ...item,
          images: item.images.map(src => ({
            src,
            alt: ""
          }))
        };
      }
      return item;
    });

    await fs.writeJson(filePath, updated, { spaces: 2, encoding: "utf-8" });
    console.log("✅ index2.json успешно обновлён!");
  } catch (err) {
    console.error("❌ Ошибка при обновлении index2.json:", err);
  }
})();
