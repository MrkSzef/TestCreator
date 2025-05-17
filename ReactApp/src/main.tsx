import { createRoot } from 'react-dom/client'
import './index.css'
import { BrowserRouter, Route, Routes } from "react-router";
import App from './App.tsx'
import CreatorPage from '../pages/creator_page/CreatorPage.tsx'


createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/creator/:id" element={<CreatorPage />} />
    </Routes>
  </BrowserRouter>,
)
