import { BrowserRouter, Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Home from './pages/Home'
import HospitalsListPage from './pages/hospitals/HospitalsListPage'
import HospitalDetailPage from './pages/hospitals/HospitalDetailPage'
import HospitalCreatePage from './pages/hospitals/HospitalCreatePage'
import DepartmentsPage from './pages/departments/DepartmentsPage'
import CreateDepartmentPage from './pages/departments/CreateDepartmentPage'
import DepartmentDetailPage from './pages/departments/DepartmentDetailPage'
import DoctorsPage from './pages/doctors/DoctorsPage'
import DoctorFormPage from './pages/doctors/DoctorFormPage'
import DoctorDetailPage from './pages/doctors/DoctorDetailPage'
import AppointmentsPage from './pages/appointments/AppointmentsPage'
import NewAppointmentPage from './pages/appointments/NewAppointmentPage'
import AppointmentDetailPage from './pages/appointments/AppointmentDetailPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="hospitals" element={<HospitalsListPage />} />
          <Route path="hospitals/:id" element={<HospitalDetailPage />} />
          <Route path="hospitals/new" element={<HospitalCreatePage />} />
          <Route path="departments" element={<DepartmentsPage />} />
          <Route path="departments/new" element={<CreateDepartmentPage />} />
          <Route path="departments/:id" element={<DepartmentDetailPage />} />
          <Route path="doctors" element={<DoctorsPage />} />
          <Route path="doctors/new" element={<DoctorFormPage />} />
          <Route path="doctors/:id" element={<DoctorDetailPage />} />
          <Route path="appointments" element={<AppointmentsPage />} />
          <Route path="appointments/new" element={<NewAppointmentPage />} />
          <Route path="appointments/:id" element={<AppointmentDetailPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App