// generate-json.mjs
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const blogDir = './blog';
const outputPath = path.join(blogDir, 'index.json');

const posts = [];

fs.readdirSync(blogDir).forEach((file) => {
  if (file.endsWith('.md')) {
    const filePath = path.join(blogDir, file);
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const { data } = matter(fileContents);

    data.slug = file.replace('.md', '');
    posts.push(data);
  }
});

fs.writeFileSync(outputPath, JSON.stringify(posts, null, 2), 'utf8');
console.log(`✅ index.json создан. Всего постов: ${posts.length}`);
