import { NavLink } from 'react-router-dom'

interface NavItem {
  label: string
  path: string
  icon?: string
}

const navItems: NavItem[] = [
  { label: 'Home', path: '/', icon: '🏠' },
  // Add items here as you create pages
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4">
      <div className="mb-8">
        <h2 className="text-xl font-bold text-white">AppName</h2>
      </div>
      <nav className="space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            {item.icon && <span>{item.icon}</span>}
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}