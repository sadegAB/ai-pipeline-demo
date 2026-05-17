import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <Link to="/" className="text-xl font-bold text-blue-600">
        AppName
      </Link>
      <div className="flex items-center gap-4">
        <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors">
          Home
        </Link>
      </div>
    </nav>
  )
}