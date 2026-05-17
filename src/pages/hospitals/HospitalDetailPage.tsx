import { useApi } from '../../hooks/useApi'
import { getHospital } from '../../api/hospitals'
import { useParams } from 'react-router-dom'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function HospitalDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data: hospital, loading, error } = useApi(() => getHospital(id!), [id])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title={hospital?.name || 'Hospital'} subtitle="Hospital details" />
      <div className="bg-white rounded-xl border border-gray-200 p-6 mt-6">
        <p className="text-gray-700"><span className="font-medium">Address:</span> {hospital?.address}</p>
        <p className="text-gray-700 mt-2"><span className="font-medium">Phone:</span> {hospital?.phone}</p>
        {hospital?.created_at && <p className="text-gray-500 text-sm mt-4">Created: {new Date(hospital.created_at).toLocaleDateString()}</p>}
      </div>
    </div>
  )
}
