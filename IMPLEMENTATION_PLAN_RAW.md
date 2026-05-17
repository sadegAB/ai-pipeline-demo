# Raw Planner Output – Phases

{
  "phases": [
    {
      "id": "phase_0",
      "title": "Types",
      "scope": "Define TypeScript interfaces for Hospitals, Departments, Doctors, and Appointments"
    },
    {
      "id": "phase_1",
      "title": "API Functions",
      "scope": "Create API functions for Hospitals, Departments, Doctors, and Appointments"
    },
    {
      "id": "phase_2",
      "title": "Hospital Pages",
      "scope": "Build pages for listing, creating, and viewing hospital details"
    },
    {
      "id": "phase_3",
      "title": "Department Pages",
      "scope": "Build pages for listing, creating, and viewing department details"
    },
    {
      "id": "phase_4",
      "title": "Doctor Pages",
      "scope": "Build pages for listing, creating, and viewing doctor details"
    },
    {
      "id": "phase_5",
      "title": "Appointment Pages",
      "scope": "Build pages for listing, creating, and viewing appointment details"
    },
    {
      "id": "phase_6",
      "title": "Routes and Nav Registration",
      "scope": "Register routes and add navigation items for Hospitals, Departments, Doctors, and Appointments"
    }
  ]
}


# Raw Planner Output – Tasks for phase_0

{
  "tasks": [
    {
      "id": "phase_0_task_0",
      "title": "Create hospital types",
      "type": "code",
      "target_file": "src/types/hospitals.ts",
      "instructions": "Define Hospital, HospitalCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_0_task_1",
      "title": "Create department types",
      "type": "code",
      "target_file": "src/types/departments.ts",
      "instructions": "Define Department, DepartmentCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_0_task_2",
      "title": "Create doctor types",
      "type": "code",
      "target_file": "src/types/doctors.ts",
      "instructions": "Define Doctor, DoctorCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_0_task_3",
      "title": "Create appointment types",
      "type": "code",
      "target_file": "src/types/appointments.ts",
      "instructions": "Define Appointment, AppointmentCreate interfaces according to TASK.md."
    }
  ]
}


# Raw Planner Output – Tasks for phase_1

{
  "tasks": [
    {
      "id": "phase_1_task_0",
      "title": "Create hospital types",
      "type": "code",
      "target_file": "src/types/hospital.ts",
      "instructions": "Define Hospital, HospitalCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_1_task_1",
      "title": "Create hospital API functions",
      "type": "code",
      "target_file": "src/api/hospital.ts",
      "instructions": "Import client from ./client, import types from ../types/hospital, export getHospitals, getHospital, createHospital functions."
    },
    {
      "id": "phase_1_task_2",
      "title": "Export hospital API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add export * from './hospital'."
    },
    {
      "id": "phase_1_task_3",
      "title": "Create department types",
      "type": "code",
      "target_file": "src/types/department.ts",
      "instructions": "Define Department, DepartmentCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_1_task_4",
      "title": "Create department API functions",
      "type": "code",
      "target_file": "src/api/department.ts",
      "instructions": "Import client from ./client, import types from ../types/department, export getDepartments, getDepartment, createDepartment, getDepartmentsByHospital functions."
    },
    {
      "id": "phase_1_task_5",
      "title": "Export department API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add export * from './department'."
    },
    {
      "id": "phase_1_task_6",
      "title": "Create doctor types",
      "type": "code",
      "target_file": "src/types/doctor.ts",
      "instructions": "Define Doctor, DoctorCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_1_task_7",
      "title": "Create doctor API functions",
      "type": "code",
      "target_file": "src/api/doctor.ts",
      "instructions": "Import client from ./client, import types from ../types/doctor, export getDoctors, getDoctor, createDoctor, getDoctorsByDepartment, getDoctorsByHospital functions."
    },
    {
      "id": "phase_1_task_8",
      "title": "Export doctor API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add export * from './doctor'."
    },
    {
      "id": "phase_1_task_9",
      "title": "Create appointment types",
      "type": "code",
      "target_file": "src/types/appointment.ts",
      "instructions": "Define Appointment, AppointmentCreate, AppointmentUpdate interfaces according to TASK.md."
    },
    {
      "id": "phase_1_task_10",
      "title": "Create appointment API functions",
      "type": "code",
      "target_file": "src/api/appointment.ts",
      "instructions": "Import client from ./client, import types from ../types/appointment, export getAppointments, getAppointment, createAppointment, updateAppointmentStatus functions."
    },
    {
      "id": "phase_1_task_11",
      "title": "Export appointment API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add export * from './appointment'."
    }
  ]
}


# Raw Planner Output – Tasks for phase_2

{
  "tasks": [
    {
      "id": "phase_2_task_0",
      "title": "Create hospital types",
      "type": "code",
      "target_file": "src/types/hospital.ts",
      "instructions": "Define Hospital, HospitalCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_2_task_1",
      "title": "Create hospital API functions",
      "type": "code",
      "target_file": "src/api/hospital.ts",
      "instructions": "Import client from ./client, import types from ../types/hospital, export getHospitals, getHospital, createHospital."
    },
    {
      "id": "phase_2_task_2",
      "title": "Export hospital API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add export * from './hospital'."
    },
    {
      "id": "phase_2_task_3",
      "title": "Create HospitalsList page",
      "type": "code",
      "target_file": "src/pages/hospitals/HospitalsListPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import getHospitals from ../../api/hospital, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, data state."
    },
    {
      "id": "phase_2_task_4",
      "title": "Create HospitalDetail page",
      "type": "code",
      "target_file": "src/pages/hospitals/HospitalDetailPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import getHospital from ../../api/hospital, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, data state."
    },
    {
      "id": "phase_2_task_5",
      "title": "Create HospitalCreate page",
      "type": "code",
      "target_file": "src/pages/hospitals/HospitalCreatePage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import createHospital from ../../api/hospital, import PageHeader from ../../components/, create form for HospitalCreate."
    },
    {
      "id": "phase_2_task_6",
      "title": "Add HospitalsList route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import HospitalsListPage from './pages/hospitals/HospitalsListPage', add Route path='hospitals' element={<HospitalsListPage />}."
    },
    {
      "id": "phase_2_task_7",
      "title": "Add HospitalDetail route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import HospitalDetailPage from './pages/hospitals/HospitalDetailPage', add Route path='hospitals/:id' element={<HospitalDetailPage />}."
    },
    {
      "id": "phase_2_task_8",
      "title": "Add HospitalCreate route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import HospitalCreatePage from './pages/hospitals/HospitalCreatePage', add Route path='hospitals/new' element={<HospitalCreatePage />}."
    },
    {
      "id": "phase_2_task_9",
      "title": "Add Hospitals nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item to navItems array: { label: 'Hospitals', path: '/hospitals', icon: '🏥' }."
    }
  ]
}


# Raw Planner Output – Tasks for phase_3

{
  "tasks": [
    {
      "id": "phase_3_task_0",
      "title": "Create department types",
      "type": "code",
      "target_file": "src/types/department.ts",
      "instructions": "Define Department, DepartmentCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_3_task_1",
      "title": "Create department API functions",
      "type": "code",
      "target_file": "src/api/department.ts",
      "instructions": "Import client from ./client, import types from ../types/department, export: getDepartments, getDepartment, createDepartment, updateDepartment, deleteDepartment."
    },
    {
      "id": "phase_3_task_2",
      "title": "Export department API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add: export * from './department'"
    },
    {
      "id": "phase_3_task_3",
      "title": "Create departments listing page",
      "type": "code",
      "target_file": "src/pages/departments/DepartmentsPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import api functions from ../../api/department, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, data state."
    },
    {
      "id": "phase_3_task_4",
      "title": "Create department creation page",
      "type": "code",
      "target_file": "src/pages/departments/CreateDepartmentPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import createDepartment from ../../api/department, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, handle form submission, show loading state, error state, success state."
    },
    {
      "id": "phase_3_task_5",
      "title": "Create department detail page",
      "type": "code",
      "target_file": "src/pages/departments/DepartmentDetailPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import getDepartment from ../../api/department, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, department details, list of doctors."
    },
    {
      "id": "phase_3_task_6",
      "title": "Add departments route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import DepartmentsPage, CreateDepartmentPage, DepartmentDetailPage from ./pages/departments/, add routes: /departments, /departments/new, /departments/:id"
    },
    {
      "id": "phase_3_task_7",
      "title": "Add departments nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item to navItems array: { label: 'Departments', path: '/departments', icon: '🚪' }"
    }
  ]
}


# Raw Planner Output – Tasks for phase_4

{
  "tasks": [
    {
      "id": "phase_4_task_0",
      "title": "Create doctor types",
      "type": "code",
      "target_file": "src/types/doctors.ts",
      "instructions": "Define Doctor, DoctorCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_4_task_1",
      "title": "Create doctor API functions",
      "type": "code",
      "target_file": "src/api/doctors.ts",
      "instructions": "Implement getDoctors, getDoctor, createDoctor, updateDoctor, deleteDoctor functions according to HANDOFF.md."
    },
    {
      "id": "phase_4_task_2",
      "title": "Export doctor API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add export * from './doctors'."
    },
    {
      "id": "phase_4_task_3",
      "title": "Create DoctorsPage",
      "type": "code",
      "target_file": "src/pages/doctors/DoctorsPage.tsx",
      "instructions": "Build page to list all doctors with filters by hospital/department."
    },
    {
      "id": "phase_4_task_4",
      "title": "Create DoctorFormPage",
      "type": "code",
      "target_file": "src/pages/doctors/DoctorFormPage.tsx",
      "instructions": "Build page to create a new doctor form (select hospital, department, available days)."
    },
    {
      "id": "phase_4_task_5",
      "title": "Create DoctorDetailPage",
      "type": "code",
      "target_file": "src/pages/doctors/DoctorDetailPage.tsx",
      "instructions": "Build page to view doctor details with appointments list."
    },
    {
      "id": "phase_4_task_6",
      "title": "Add DoctorsPage route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Add route for DoctorsPage."
    },
    {
      "id": "phase_4_task_7",
      "title": "Add DoctorFormPage route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Add route for DoctorFormPage."
    },
    {
      "id": "phase_4_task_8",
      "title": "Add DoctorDetailPage route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Add route for DoctorDetailPage."
    },
    {
      "id": "phase_4_task_9",
      "title": "Add Doctors nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item for Doctors."
    }
  ]
}


# Raw Planner Output – Tasks for phase_5

{
  "tasks": [
    {
      "id": "phase_5_task_0",
      "title": "Create appointment types",
      "type": "code",
      "target_file": "src/types/appointment.ts",
      "instructions": "Define Appointment, AppointmentCreate interfaces according to TASK.md."
    },
    {
      "id": "phase_5_task_1",
      "title": "Create appointment API functions",
      "type": "code",
      "target_file": "src/api/appointments.ts",
      "instructions": "Import client from ./client, import types from ../types/appointment, export: getAppointments, getAppointment, createAppointment, updateAppointmentStatus"
    },
    {
      "id": "phase_5_task_2",
      "title": "Export appointment API functions",
      "type": "code",
      "target_file": "src/api/index.ts",
      "instructions": "Add: export * from './appointments'"
    },
    {
      "id": "phase_5_task_3",
      "title": "Create appointments list page",
      "type": "code",
      "target_file": "src/pages/appointments/AppointmentsPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import api functions from ../../api/appointments, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, data state"
    },
    {
      "id": "phase_5_task_4",
      "title": "Create appointment creation page",
      "type": "code",
      "target_file": "src/pages/appointments/NewAppointmentPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import api functions from ../../api/appointments, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, form for creating appointment"
    },
    {
      "id": "phase_5_task_5",
      "title": "Create appointment detail page",
      "type": "code",
      "target_file": "src/pages/appointments/AppointmentDetailPage.tsx",
      "instructions": "Import useApi from ../../hooks/useApi, import api functions from ../../api/appointments, import PageHeader, LoadingSpinner, ErrorMessage from ../../components/, show loading state, error state, appointment details, status update button"
    },
    {
      "id": "phase_5_task_6",
      "title": "Add appointments route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import AppointmentsPage, NewAppointmentPage, AppointmentDetailPage from ./pages/appointments/, add routes for /appointments, /appointments/new, /appointments/:id"
    },
    {
      "id": "phase_5_task_7",
      "title": "Add appointments nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item to navItems array for Appointments"
    }
  ]
}


# Raw Planner Output – Tasks for phase_6

{
  "tasks": [
    {
      "id": "phase_6_task_0",
      "title": "Add Hospitals route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import HospitalsPage and add Route for path 'hospitals'."
    },
    {
      "id": "phase_6_task_1",
      "title": "Add Departments route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import DepartmentsPage and add Route for path 'departments'."
    },
    {
      "id": "phase_6_task_2",
      "title": "Add Doctors route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import DoctorsPage and add Route for path 'doctors'."
    },
    {
      "id": "phase_6_task_3",
      "title": "Add Appointments route",
      "type": "code",
      "target_file": "src/App.tsx",
      "instructions": "Import AppointmentsPage and add Route for path 'appointments'."
    },
    {
      "id": "phase_6_task_4",
      "title": "Register Hospitals nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item for Hospitals with path '/hospitals' and appropriate icon."
    },
    {
      "id": "phase_6_task_5",
      "title": "Register Departments nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item for Departments with path '/departments' and appropriate icon."
    },
    {
      "id": "phase_6_task_6",
      "title": "Register Doctors nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item for Doctors with path '/doctors' and appropriate icon."
    },
    {
      "id": "phase_6_task_7",
      "title": "Register Appointments nav item",
      "type": "code",
      "target_file": "src/layouts/Sidebar.tsx",
      "instructions": "Add nav item for Appointments with path '/appointments' and appropriate icon."
    }
  ]
}
