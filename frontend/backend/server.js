const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Helper to read data
const readData = (filename) => {
  const filePath = path.join(__dirname, 'data', filename);
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
};

// Endpoints
app.get('/api/settings', (req, res) => {
  const settings = readData('settings.json');
  res.json(settings);
});

app.post('/api/settings', (req, res) => {
  const newSettings = req.body;
  fs.writeFileSync(path.join(__dirname, 'data', 'settings.json'), JSON.stringify(newSettings, null, 2));
  res.json({ success: true, message: 'Settings updated' });
});

app.get('/api/search', (req, res) => {
  const query = req.query.q?.toLowerCase() || '';
  const components = readData('mockComponents.json');
  
  const results = components.filter(c => 
    c.name.toLowerCase().includes(query) || 
    c.id.toLowerCase().includes(query)
  );
  
  res.json(results);
});

// AI Analysis Endpoint (Mock for now, will connect to Gemini/OpenAI)
app.post('/api/analyze', async (req, res) => {
  const { componentData } = req.body;
  
  // Simulation of AI processing
  setTimeout(() => {
    const analysis = {
      recommendation: componentData.sources.sort((a, b) => a.price - b.price)[0],
      summary: `AI Analizi: ${componentData.name} için en iyi seçenek ${componentData.sources[0].site}. Fiyat/Performans skoru %96.`,
      charts: [
        { name: 'Fiyat', data: componentData.sources.map(s => ({ site: s.site, value: s.price })) },
        { name: 'Stok', data: componentData.sources.map(s => ({ site: s.site, value: s.stock })) }
      ]
    };
    res.json(analysis);
  }, 1500);
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
