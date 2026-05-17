import { useParams } from 'react-router-dom'
import { useApi } from '../../hooks/useApi'
import { getDoctor, getDoctorAppointments } from '../../api/doctors'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function DoctorDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data: doctor, loading: doctorLoading, error: doctorError } = useApi(() => getDoctor(id!), [])
  const { data: appointments, loading: appointmentsLoading, error: appointmentsError } = useApi(() => getDoctorAppointments(id!), [id])

  if (doctorLoading || appointmentsLoading) return <LoadingSpinner />
  if (doctorError || appointmentsError) return <ErrorMessage message={(doctorError || appointmentsError) || 'An error occurred'} />

  return (
    <div>
      <PageHeader title={`${doctor?.name}`} subtitle={`Specialty: ${doctor?.specialty}`} />
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <p className="font-medium text-gray-900">Available Days: {doctor?.available_days.map(day => <span key={day} className="inline-block bg-blue-100 text-blue-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full">{day}</span>)}</p>
        <p className="text-sm text-gray-500">Available From: {doctor?.available_from}</p>
        <p className="text-sm text-gray-500">Available To: {doctor?.available_to}</p>
      </div>
      <PageHeader title="Appointments" />
      <div className="bg-white rounded-xl border border-gray-200">
        {(appointments as any[])?.map((appointment: any) => (
          <div key={appointment.id} className="px-6 py-4 border-b border-gray-100 last:border-0">
            <p className="font-medium text-gray-900">{appointment.patient_name}</p>
            <p className="text-sm text-gray-500">Date: {appointment.date}, Time: {appointment.time}</p>
            <p className="text-sm text-gray-500">Status: <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${appointment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{appointment.status}</span></p>
          </div>
        ))}
      </div>
    </div>
  )
}