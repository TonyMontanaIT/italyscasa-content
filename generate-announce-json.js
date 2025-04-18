const fs = require("fs-extra");
const path = require("path");
const matter = require("gray-matter");

const mdFolder = path.join(__dirname, "anunci");
const outputPath = path.join(mdFolder, "index2.json");

(async () => {
  const files = await fs.readdir(mdFolder);
  const mdFiles = files.filter(file => file.endsWith(".md"));

  const data = [];

  for (const file of mdFiles) {
    const filePath = path.join(mdFolder, file);
    const content = await fs.readFile(filePath, "utf-8");
    const { data: meta } = matter(content);

    data.push({
      slug: meta.slug || path.basename(file, ".md"),
      rif1: meta.RIF1 || "",
      nomeAnunci: meta.nomeAnunci || "",
      nomeZona: meta.nomeZona || "",
      city1: meta.city1 || "",
      street1: meta.street1 || "",
      prezzo1: meta.prezzo1 || "",
      tipo: meta.tipo || "",
      totalrooms: meta.totalrooms || "",
      rooms: meta.rooms || "",
      bagni: meta.bagni || "",
      zonam2: meta.zonam2 || "",
      floor: meta.floor || "",
      elevator: meta.elevator || "",
      terrazzo: meta.terrazzo || "",
      prezzo: meta.prezzo || "",
      giardino: meta.giardino || "",
      garage: meta.garage || "",
      arredamenti: meta.arredamenti || "",
      patio: meta.patio || "",
      corte: meta.corte || "",
      descrizione: meta.descrizione || "",
      h2t1: meta.h2t1 || "",
      text1: meta.text1 || "",
      h2t2: meta.h2t2 || "",
      text2: meta.text2 || "",
      h2t3: meta.h2t3 || "",
      text3: meta.text3 || "",
      h2t4: meta.h2t4 || "",
      text4: meta.text4 || "",
      h2t5: meta.h2t5 || "",
      text5: meta.text5 || "",
      h2t6: meta.h2t6 || "",
      text6: meta.text6 || "",
      video: meta.video || "",
      video360: meta.video360 || "",
      images: meta.images || [],
      latitude: meta.latitude || "",
      longitude: meta.longitude || ""
    });
  }

  await fs.writeJson(outputPath, data, { spaces: 2, encoding: "utf-8" });
  console.log(`✅ index2.json created with ${data.length} announcements`);
})();
