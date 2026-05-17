import { useApi } from '../../hooks/useApi'
import { getDepartments } from '../../api/departments'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function DepartmentsPage() {
  const { data, loading, error } = useApi(getDepartments, [])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title="Departments" subtitle="Manage departments" />
      <div className="bg-white rounded-xl border border-gray-200">
        {data?.map(department => (
          <div key={department.id} className="px-6 py-4 border-b border-gray-100 last:border-0">
            <p className="font-medium text-gray-900">{department.name}</p>
            <p className="text-sm text-gray-500">{department.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}