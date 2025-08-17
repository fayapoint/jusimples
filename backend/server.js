const express = require('express');
const app = express();
const port = 3001;

app.get('/', (req, res) => {
  res.send('Backend do JuSimples está funcionando!');
});

app.listen(port, () => {
  console.log(`Backend do JuSimples rodando em http://localhost:${port}`);
});


