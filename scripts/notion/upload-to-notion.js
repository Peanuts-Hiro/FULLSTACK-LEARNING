const https = require('https');
const fs = require('fs');

// Notion API Configuration
const NOTION_API_KEY = process.env.NOTION_API_KEY;
const NOTION_VERSION = '2022-06-28';

if (!NOTION_API_KEY) {
  console.error('Error: NOTION_API_KEY environment variable is not set');
  console.error('Please set it in your environment or .env file');
  process.exit(1);
}

// Page mappings
const PAGE_MAPPINGS = [
  {
    pageId: '2c7ff8dad4c9816a9962c28f1b8ed5cf',
    file: './projects/week01-portfolio/knowledge/01_requirements-thinking.md'
  },
  {
    pageId: '2c7ff8dad4c98112bf02f9a77fab98e5',
    file: './projects/week01-portfolio/knowledge/02_design-thinking.md'
  },
  {
    pageId: '2c7ff8dad4c9811f9f8febcdf4157432',
    file: './projects/week01-portfolio/knowledge/03_phase1-html-structure.md'
  },
  {
    pageId: '2c7ff8dad4c98133b5aae27a1cb2cd67',
    file: './projects/week01-portfolio/knowledge/04_phase2-basic-styles.md'
  },
  {
    pageId: '2c7ff8dad4c981e3a55cc2ebaf6ab12a',
    file: './projects/week01-portfolio/knowledge/05_phase3-flexbox-layout.md'
  },
  {
    pageId: '2c7ff8dad4c981169b09e7184b8e2c8e',
    file: './projects/week01-portfolio/knowledge/06_phase4-effects-animations.md'
  }
];

// Helper function to make HTTPS requests
function notionRequest(path, method, data) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.notion.com',
      port: 443,
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${NOTION_API_KEY}`,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(responseData));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${responseData}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

// Convert markdown to Notion blocks
function markdownToNotionBlocks(markdown) {
  const lines = markdown.split('\n');
  const blocks = [];
  let currentCodeBlock = null;
  let currentCodeLanguage = '';
  let currentList = [];
  let inTable = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Handle code blocks
    if (line.startsWith('```')) {
      if (currentCodeBlock === null) {
        // Start code block
        currentCodeLanguage = line.substring(3).trim() || 'plain text';
        currentCodeBlock = [];
      } else {
        // End code block
        blocks.push({
          object: 'block',
          type: 'code',
          code: {
            rich_text: [{
              type: 'text',
              text: { content: currentCodeBlock.join('\n') }
            }],
            language: currentCodeLanguage
          }
        });
        currentCodeBlock = null;
        currentCodeLanguage = '';
      }
      continue;
    }

    // Inside code block
    if (currentCodeBlock !== null) {
      currentCodeBlock.push(line);
      continue;
    }

    // Skip table headers and separators (simplified table handling)
    if (line.startsWith('|') && (line.includes('---') || line.includes('|---|'))) {
      inTable = true;
      continue;
    }

    // Convert table rows to bullet points
    if (line.startsWith('|') && !line.includes('---')) {
      const cells = line.split('|').filter(cell => cell.trim()).map(cell => cell.trim());
      if (cells.length > 0) {
        blocks.push({
          object: 'block',
          type: 'bulleted_list_item',
          bulleted_list_item: {
            rich_text: [{
              type: 'text',
              text: { content: cells.join(' | ') }
            }]
          }
        });
      }
      continue;
    }

    // Empty line
    if (line.trim() === '') {
      continue;
    }

    // Heading 1
    if (line.startsWith('# ')) {
      blocks.push({
        object: 'block',
        type: 'heading_1',
        heading_1: {
          rich_text: [{
            type: 'text',
            text: { content: line.substring(2) }
          }]
        }
      });
      continue;
    }

    // Heading 2
    if (line.startsWith('## ')) {
      blocks.push({
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{
            type: 'text',
            text: { content: line.substring(3) }
          }]
        }
      });
      continue;
    }

    // Heading 3
    if (line.startsWith('### ')) {
      blocks.push({
        object: 'block',
        type: 'heading_3',
        heading_3: {
          rich_text: [{
            type: 'text',
            text: { content: line.substring(4) }
          }]
        }
      });
      continue;
    }

    // Heading 4
    if (line.startsWith('#### ')) {
      blocks.push({
        object: 'block',
        type: 'heading_3',
        heading_3: {
          rich_text: [{
            type: 'text',
            text: { content: line.substring(5) }
          }]
        }
      });
      continue;
    }

    // Bullet list
    if (line.startsWith('- ') || line.startsWith('* ')) {
      const content = line.substring(2).trim();
      // Remove markdown formatting from content
      const cleanContent = content
        .replace(/\*\*(.*?)\*\*/g, '$1')  // Remove bold
        .replace(/\*(.*?)\*/g, '$1')       // Remove italic
        .replace(/`(.*?)`/g, '$1')         // Remove inline code
        .replace(/\[(.*?)\]\(.*?\)/g, '$1'); // Remove links

      blocks.push({
        object: 'block',
        type: 'bulleted_list_item',
        bulleted_list_item: {
          rich_text: [{
            type: 'text',
            text: { content: cleanContent.substring(0, 2000) }
          }]
        }
      });
      continue;
    }

    // Checkbox list
    if (line.startsWith('- [ ] ') || line.startsWith('- [x] ')) {
      const checked = line.includes('[x]');
      const content = line.substring(6).trim();
      blocks.push({
        object: 'block',
        type: 'to_do',
        to_do: {
          rich_text: [{
            type: 'text',
            text: { content: content.substring(0, 2000) }
          }],
          checked: checked
        }
      });
      continue;
    }

    // Divider
    if (line.startsWith('---')) {
      blocks.push({
        object: 'block',
        type: 'divider',
        divider: {}
      });
      continue;
    }

    // Callout for emphasized content (lines starting with ** or important keywords)
    if (line.includes('**重要') || line.includes('**学び') || line.includes('**注意') ||
        line.includes('**効果') || line.includes('**理由')) {
      const cleanContent = line
        .replace(/\*\*(.*?)\*\*/g, '$1')
        .replace(/\*(.*?)\*/g, '$1')
        .replace(/`(.*?)`/g, '$1');

      blocks.push({
        object: 'block',
        type: 'callout',
        callout: {
          rich_text: [{
            type: 'text',
            text: { content: cleanContent.substring(0, 2000) }
          }],
          icon: { emoji: '💡' }
        }
      });
      continue;
    }

    // Regular paragraph
    if (line.trim().length > 0) {
      const cleanContent = line
        .replace(/\*\*(.*?)\*\*/g, '$1')
        .replace(/\*(.*?)\*/g, '$1')
        .replace(/`(.*?)`/g, '$1')
        .replace(/\[(.*?)\]\(.*?\)/g, '$1');

      blocks.push({
        object: 'block',
        type: 'paragraph',
        paragraph: {
          rich_text: [{
            type: 'text',
            text: { content: cleanContent.substring(0, 2000) }
          }]
        }
      });
    }
  }

  return blocks;
}

// Upload blocks to Notion in batches (max 100 per request)
async function uploadToNotion(pageId, blocks) {
  const batchSize = 100;
  let uploadedCount = 0;

  for (let i = 0; i < blocks.length; i += batchSize) {
    const batch = blocks.slice(i, i + batchSize);

    try {
      await notionRequest(
        `/v1/blocks/${pageId}/children`,
        'PATCH',
        { children: batch }
      );
      uploadedCount += batch.length;
      console.log(`  Uploaded ${uploadedCount}/${blocks.length} blocks...`);

      // Wait a bit to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error(`  Error uploading batch: ${error.message}`);
      throw error;
    }
  }

  return uploadedCount;
}

// Main function
async function main() {
  console.log('Starting Notion upload process...\n');

  for (const mapping of PAGE_MAPPINGS) {
    try {
      console.log(`Processing: ${mapping.file}`);

      // Read markdown file
      const markdown = fs.readFileSync(mapping.file, 'utf8');

      // Convert to Notion blocks
      console.log('  Converting markdown to Notion blocks...');
      const blocks = markdownToNotionBlocks(markdown);
      console.log(`  Created ${blocks.length} blocks`);

      // Upload to Notion
      console.log('  Uploading to Notion...');
      const uploadedCount = await uploadToNotion(mapping.pageId, blocks);

      console.log(`✓ Successfully uploaded ${uploadedCount} blocks to page ${mapping.pageId}\n`);

    } catch (error) {
      console.error(`✗ Failed to process ${mapping.file}: ${error.message}\n`);
    }
  }

  console.log('Upload process completed!');
}

// Run the script
main().catch(console.error);
