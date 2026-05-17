import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createDepartment } from '../../api/departments'
import PageHeader from '../../components/PageHeader'

export default function CreateDepartmentPage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [hospitalId, setHospitalId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await createDepartment({ name, description, hospital_id: hospitalId })
      navigate('/departments')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to create department')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <PageHeader title="Create Department" subtitle="Add a new department" />
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <input type="text" value={description} onChange={(e) => setDescription(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Hospital ID</label>
          <input type="text" value={hospitalId} onChange={(e) => setHospitalId(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <button type="submit" disabled={loading}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50">
          {loading ? 'Creating...' : 'Create Department'}
        </button>
      </form>
    </div>
  )
}
