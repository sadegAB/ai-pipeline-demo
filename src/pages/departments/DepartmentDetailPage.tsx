import { useApi } from '../../hooks/useApi'
import { useParams } from 'react-router-dom'
import { getDepartment } from '../../api/departments'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function DepartmentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data: department, loading, error } = useApi(() => getDepartment(id!), [id])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error || 'An error occurred'} />

  return (
    <div>
      <PageHeader title={department?.name || 'Department'} subtitle="Department details" />
      <div className="bg-white rounded-xl border border-gray-200 p-6 mt-6">
        {department?.description && (
          <p className="text-gray-600 mb-4">{department.description}</p>
        )}
        <p className="text-sm text-gray-500">Hospital ID: {department?.hospital_id}</p>
      </div>
    </div>
  )
}
