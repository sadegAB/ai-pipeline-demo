# React Vite Template — Handoff Document

## Overview
Clean reusable React + Vite + TypeScript + TailwindCSS frontend template.
Connects to a FastAPI backend via axios. No UI library — pure Tailwind.

## File Structure
src/
├── api/
│   ├── client.ts        # axios instance, base URL from .env
│   └── index.ts         # exports all api modules
├── types/
│   └── index.ts         # shared TypeScript interfaces
├── components/
│   ├── LoadingSpinner.tsx
│   ├── ErrorMessage.tsx
│   └── PageHeader.tsx
├── layouts/
│   ├── MainLayout.tsx   # Sidebar + Navbar + Outlet
│   ├── Sidebar.tsx      # nav items list
│   └── Navbar.tsx       # top bar
├── pages/
│   └── Home.tsx         # example page
├── hooks/
│   └── useApi.ts        # generic data fetching hook
└── App.tsx              # router + routes

## Conventions
- API base URL: from VITE_API_URL in .env
- All API calls: use client from src/api/client.ts
- All fetch logic: use useApi() hook from src/hooks/useApi.ts
- All types: define in src/types/index.ts or src/types/{feature}.ts
- All pages: one file per feature in src/pages/{feature}/
- All API functions: one file per feature in src/api/{feature}.ts
- Shared components: src/components/
- No inline styles — Tailwind classes only

## How to Add a New Feature (e.g. "doctors")

### Step 1 — Add types in src/types/doctors.ts
export interface Doctor {
  id: string
  name: string
  specialty: string
  created_at?: string
}

export interface DoctorCreate {
  name: string
  specialty: string
}

### Step 2 — Add API functions in src/api/doctors.ts
import client from './client'
import { Doctor, DoctorCreate } from '../types/doctors'

export const getDoctors = () =>
  client.get<Doctor[]>('/doctors').then(r => r.data)

export const getDoctor = (id: string) =>
  client.get<Doctor>(`/doctors/${id}`).then(r => r.data)

export const createDoctor = (data: DoctorCreate) =>
  client.post<Doctor>('/doctors', data).then(r => r.data)

export const updateDoctor = (id: string, data: DoctorCreate) =>
  client.patch<Doctor>(`/doctors/${id}`, data).then(r => r.data)

export const deleteDoctor = (id: string) =>
  client.delete(`/doctors/${id}`).then(r => r.data)

### Step 3 — Export from src/api/index.ts
export * from './doctors'

### Step 4 — Create page src/pages/doctors/DoctorsPage.tsx
import { useApi } from '../../hooks/useApi'
import { getDoctors } from '../../api/doctors'
import PageHeader from '../../components/PageHeader'
import LoadingSpinner from '../../components/LoadingSpinner'
import ErrorMessage from '../../components/ErrorMessage'

export default function DoctorsPage() {
  const { data, loading, error } = useApi(getDoctors, [])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />

  return (
    <div>
      <PageHeader title="Doctors" subtitle="Manage doctors" />
      <div className="bg-white rounded-xl border border-gray-200">
        {data?.map(doctor => (
          <div key={doctor.id} className="px-6 py-4 border-b border-gray-100 last:border-0">
            <p className="font-medium text-gray-900">{doctor.name}</p>
            <p className="text-sm text-gray-500">{doctor.specialty}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

### Step 5 — Add route in App.tsx
import DoctorsPage from './pages/doctors/DoctorsPage'
<Route path="doctors" element={<DoctorsPage />} />

### Step 6 — Add nav item in src/layouts/Sidebar.tsx
{ label: 'Doctors', path: '/doctors', icon: '👨‍⚕️' }

### Step 7 — Done