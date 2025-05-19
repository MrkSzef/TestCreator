import { createRoot } from 'react-dom/client'
import './index.css'
import { BrowserRouter, Route, Routes } from "react-router";
import App from './App.tsx'
import CreatorPage from '../pages/creator_page/CreatorPage.tsx'
import TestPage from '../pages/test_page/TestPage.tsx'
import { Toaster } from "../components/ui/sonner.tsx";
const root = window.document.documentElement
root.classList.add('dark')

createRoot(document.getElementById('root')!).render(

  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/creator/:id" element={<CreatorPage />} />
      <Route path="/test/:id" element={<TestPage />}></Route>
    </Routes>
      <Toaster/>
  </BrowserRouter>,

)
