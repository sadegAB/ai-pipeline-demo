import client from './client'
import type { Doctor, DoctorCreate } from '../types/doctors'

export const getDoctors = () =>
  client.get<Doctor[]>('/doctors').then(r => r.data)

export const getDoctor = (id: string) =>
  client.get<Doctor>(`/doctors/${id}`).then(r => r.data)

export const createDoctor = (data: DoctorCreate) =>
  client.post<Doctor>('/doctors', data).then(r => r.data)

export const getDoctorAppointments = (doctorId: string) =>
  client.get(`/doctors/${doctorId}/appointments`).then(r => r.data)
