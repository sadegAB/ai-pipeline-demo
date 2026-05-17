import { useApi } from '../../hooks/useApi'
import { getHospitals } from '../../api/hospitals'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function HospitalsListPage() {
  const { data, loading, error } = useApi(getHospitals, [])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title="Hospitals" subtitle="List of all hospitals" />
      <div className="bg-white rounded-xl border border-gray-200">
        {data?.map(hospital => (
          <div key={hospital.id} className="px-6 py-4 border-b border-gray-100 last:border-0">
            <p className="font-medium text-gray-900">{hospital.name}</p>
            <p className="text-sm text-gray-500">{hospital.address}</p>
            <p className="text-sm text-gray-500">{hospital.phone}</p>
          </div>
        ))}
      </div>
    </div>
  )
}