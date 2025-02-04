import './App.css'
import { Chat } from './pages/chat/chat'
import { Landing } from './pages/landing/landing'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <Router>
        <div className="w-full h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App