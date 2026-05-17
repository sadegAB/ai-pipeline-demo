import { useApi } from '../../hooks/useApi'
import { getAppointments } from '../../api/appointments'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function AppointmentsPage() {
  const { data, loading, error } = useApi(getAppointments, [])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title="Appointments" subtitle="Manage appointments" />
      <div className="bg-white rounded-xl border border-gray-200">
        {data?.map(appointment => (
          <div key={appointment.id} className="px-6 py-4 border-b border-gray-100 last:border-0">
            <p className="font-medium text-gray-900">Patient: {appointment.patient_name}</p>
            <p className="text-sm text-gray-500">Date: {appointment.date}, Time: {appointment.time}</p>
            <p className="text-sm text-gray-500">Status: <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${appointment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{appointment.status}</span></p>
          </div>
        ))}
      </div>
    </div>
  )
}