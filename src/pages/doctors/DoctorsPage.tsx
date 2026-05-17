import { getHospitals } from '../../api/hospitals'
import { getDepartments } from '../../api/departments'
import { useApi } from '../../hooks/useApi'
import { getDoctors } from '../../api/doctors'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'
import { useState } from 'react'

export default function DoctorsPage() {
  const { data: doctors, loading, error } = useApi(getDoctors, [])
  const { data: hospitals } = useApi(getHospitals, [])
  const { data: departments } = useApi(getDepartments, [])
  const [hospitalFilter, setHospitalFilter] = useState<string | null>(null)
  const [departmentFilter, setDepartmentFilter] = useState<string | null>(null)

  const filteredDoctors = doctors?.filter(doctor => {
    if (hospitalFilter && doctor.hospital_id !== hospitalFilter) return false
    if (departmentFilter && doctor.department_id !== departmentFilter) return false
    return true
  })

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title="Doctors" subtitle="Manage doctors" />
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Filter by Hospital</label>
        <select
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          value={hospitalFilter || ''}
          onChange={(e) => setHospitalFilter(e.target.value || null)}
        >
          <option value="">All Hospitals</option>
          {hospitals?.map(hospital => (
            <option key={hospital.id} value={hospital.id}>{hospital.name}</option>
          ))}
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Filter by Department</label>
        <select
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          value={departmentFilter || ''}
          onChange={(e) => setDepartmentFilter(e.target.value || null)}
        >
          <option value="">All Departments</option>
          {departments?.map(department => (
            <option key={department.id} value={department.id}>{department.name}</option>
          ))}
        </select>
      </div>
      <div className="bg-white rounded-xl border border-gray-200">
        {filteredDoctors?.map(doctor => (
          <div key={doctor.id} className="px-6 py-4 border-b border-gray-100 last:border-0">
            <p className="font-medium text-gray-900">{doctor.name}</p>
            <p className="text-sm text-gray-500">{doctor.specialty}</p>
            <p className="text-sm text-gray-500">Available Days: {doctor.available_days.join(', ')}</p>
            <p className="text-sm text-gray-500">Available From: {doctor.available_from}</p>
            <p className="text-sm text-gray-500">Available To: {doctor.available_to}</p>
          </div>
        ))}
      </div>
    </div>
  )
}