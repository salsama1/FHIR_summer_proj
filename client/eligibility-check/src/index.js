import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { prefixer } from 'stylis';
import { BrowserRouter } from 'react-router-dom';

// f

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
 
      <BrowserRouter>
      <App />
      </BrowserRouter>
 
);