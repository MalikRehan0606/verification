const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(express.static('public'));

app.get('/verify', async (req, res) => {
  try {
    
    const response = await axios.post('https://api.github.com/repos/MalikRehan0606/verify-button/actions/workflows/verify.yml/dispatches', {
      ref: 'main'
    }, {
      headers: {
        'Authorization': `Bearer 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`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    res.status(200).send('Workflow dispatched successfully.');
  } catch (error) {
    console.error(error);
    res.status(500).send('Error dispatching workflow.');
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
