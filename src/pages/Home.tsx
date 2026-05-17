import PageHeader from '../components/PageHeader'

export default function Home() {
  return (
    <div>
      <PageHeader
        title="Welcome"
        subtitle="Select a section from the sidebar to get started."
      />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-1">Feature 1</h3>
          <p className="text-gray-500 text-sm">Add your first feature here.</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-1">Feature 2</h3>
          <p className="text-gray-500 text-sm">Add your second feature here.</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-1">Feature 3</h3>
          <p className="text-gray-500 text-sm">Add your third feature here.</p>
        </div>
      </div>
    </div>
  )
}