import { useState } from 'react'
import { useApi } from '../../hooks/useApi'
import { getHospitals } from '../../api/hospitals'
import { getDepartmentsByHospitalId } from '../../api/departments'
import { createDoctor } from '../../api/doctors'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'
import type { Hospital, DoctorCreate } from '../../types'

export default function DoctorFormPage() {
  const { data: hospitals, loading: hospitalsLoading, error: hospitalsError } = useApi(getHospitals, [])
  const [selectedHospital, setSelectedHospital] = useState<Hospital | null>(null)
  const { data: departments, loading: departmentsLoading, error: departmentsError } = useApi(() => selectedHospital ? getDepartmentsByHospitalId(selectedHospital.id) : Promise.resolve([]), [selectedHospital])
  const [formData, setFormData] = useState<DoctorCreate>({
    name: '',
    specialty: '',
    hospital_id: '',
    department_id: '',
    available_days: [],
    available_from: '',
    available_to: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value
    })
  }

  const handleDaysChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const options = e.target.options
    const value = []
    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        value.push(options[i].value)
      }
    }
    setFormData({
      ...formData,
      available_days: value
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await createDoctor(formData)
      alert('Doctor created successfully')
    } catch (err) {
      setError('Failed to create doctor')
    } finally {
      setLoading(false)
    }
  }

  if (hospitalsLoading || departmentsLoading) return <LoadingSpinner />
  if (hospitalsError || departmentsError) return <ErrorMessage message={(hospitalsError || departmentsError) || "An error occurred"} />

  return (
    <div>
      <PageHeader title="Create Doctor" subtitle="Add a new doctor" />
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
          <input type="text" id="name" name="name" value={formData.name} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="specialty" className="block text-sm font-medium text-gray-700">Specialty</label>
          <input type="text" id="specialty" name="specialty" value={formData.specialty} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="hospital_id" className="block text-sm font-medium text-gray-700">Hospital</label>
          <select id="hospital_id" name="hospital_id" value={formData.hospital_id} onChange={(e) => {
            handleInputChange(e)
            setSelectedHospital(hospitals?.find(hospital => hospital.id === e.target.value) || null)
          }} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="">Select a hospital</option>
            {hospitals?.map(hospital => (
              <option key={hospital.id} value={hospital.id}>{hospital.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="department_id" className="block text-sm font-medium text-gray-700">Department</label>
          <select id="department_id" name="department_id" value={formData.department_id} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="">Select a department</option>
            {(departments as any[])?.map((department: any) => (
              <option key={department.id} value={department.id}>{department.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="available_days" className="block text-sm font-medium text-gray-700">Available Days</label>
          <select id="available_days" name="available_days" multiple value={formData.available_days} onChange={handleDaysChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            <option value="Monday">Monday</option>
            <option value="Tuesday">Tuesday</option>
            <option value="Wednesday">Wednesday</option>
            <option value="Thursday">Thursday</option>
            <option value="Friday">Friday</option>
            <option value="Saturday">Saturday</option>
            <option value="Sunday">Sunday</option>
          </select>
        </div>
        <div>
          <label htmlFor="available_from" className="block text-sm font-medium text-gray-700">Available From</label>
          <input type="time" id="available_from" name="available_from" value={formData.available_from} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <label htmlFor="available_to" className="block text-sm font-medium text-gray-700">Available To</label>
          <input type="time" id="available_to" name="available_to" value={formData.available_to} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <button type="submit" disabled={loading} className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          {loading ? 'Creating...' : 'Create Doctor'}
        </button>
        {error && <ErrorMessage message={error} />}
      </form>
    </div>
  )
}