import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createAppointment } from '../../api/appointments'
import PageHeader from '../../components/PageHeader'

export default function NewAppointmentPage() {
  const navigate = useNavigate()
  const [doctorId, setDoctorId] = useState('')
  const [patientName, setPatientName] = useState('')
  const [patientPhone, setPatientPhone] = useState('')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [notes, setNotes] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      await createAppointment({ doctor_id: doctorId, patient_name: patientName, patient_phone: patientPhone, date, time, notes })
      navigate('/appointments')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to book appointment')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <PageHeader title="Book Appointment" subtitle="Schedule a new appointment" />
      {error && <p className="text-red-600 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Doctor ID</label>
          <input type="text" value={doctorId} onChange={(e) => setDoctorId(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Patient Name</label>
          <input type="text" value={patientName} onChange={(e) => setPatientName(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Patient Phone</label>
          <input type="tel" value={patientPhone} onChange={(e) => setPatientPhone(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Date</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Time</label>
          <input type="time" value={time} onChange={(e) => setTime(e.target.value)} required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Notes</label>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
        </div>
        <button type="submit" disabled={loading}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50">
          {loading ? 'Booking...' : 'Book Appointment'}
        </button>
      </form>
    </div>
  )
}
