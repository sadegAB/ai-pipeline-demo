import { useApi } from '../../hooks/useApi'
import { useParams } from 'react-router-dom'
import { getAppointment, updateAppointmentStatus } from '../../api/appointments'
import type { Appointment } from '../../types/appointments'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'
import { useState } from 'react'

export default function AppointmentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data, loading, error } = useApi<Appointment>(() => getAppointment(id!), [])
  const [status, setStatus] = useState(data?.status || '')

  const handleStatusUpdate = async (newStatus: string) => {
    try {
      await updateAppointmentStatus(id!, newStatus)
      setStatus(newStatus)
    } catch (err) {
      console.error('Failed to update appointment status', err)
      // Optionally, show an error message to the user
    }
  }

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title={`Appointment with ${data?.patient_name}`} subtitle={`Date: ${data?.date}, Time: ${data?.time}`} />
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="mb-4">
          <p className="font-medium text-gray-900">Patient Name:</p>
          <p className="text-sm text-gray-500">{data?.patient_name}</p>
        </div>
        <div className="mb-4">
          <p className="font-medium text-gray-900">Patient Phone:</p>
          <p className="text-sm text-gray-500">{data?.patient_phone}</p>
        </div>
        <div className="mb-4">
          <p className="font-medium text-gray-900">Notes:</p>
          <p className="text-sm text-gray-500">{data?.notes}</p>
        </div>
        <div className="mb-4">
          <p className="font-medium text-gray-900">Status:</p>
          <button
            onClick={() => handleStatusUpdate(status === 'pending' ? 'confirmed' : 'pending')}
            className={`px-3 py-1 rounded-full text-white ${
              status === 'pending' ? 'bg-yellow-500' : 'bg-green-500'
            }`}
          >
            {status === 'pending' ? 'Confirm' : 'Mark Pending'}
          </button>
          <button
            onClick={() => handleStatusUpdate('cancelled')}
            className="ml-2 px-3 py-1 rounded-full text-white bg-red-500"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}