import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createHospital } from '../../api/hospitals'
import PageHeader from '../../components/PageHeader'

export default function HospitalCreatePage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [address, setAddress] = useState('')
  const [phone, setPhone] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await createHospital({ name, address, phone })
      navigate('/hospitals')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to create hospital')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <PageHeader title="Create Hospital" subtitle="Add a new hospital" />
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
          <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="address" className="block text-sm font-medium text-gray-700">Address</label>
          <input type="text" id="address" value={address} onChange={(e) => setAddress(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700">Phone</label>
          <input type="tel" id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <button type="submit" disabled={loading}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50">
          {loading ? 'Creating...' : 'Create Hospital'}
        </button>
      </form>
    </div>
  )
}
