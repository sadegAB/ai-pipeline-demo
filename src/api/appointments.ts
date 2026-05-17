import client from './client'
import type { Appointment, AppointmentCreate } from '../types/appointments'

export const getAppointments = () =>
  client.get<Appointment[]>('/appointments').then(r => r.data)

export const getAppointment = (id: string) =>
  client.get<Appointment>(`/appointments/${id}`).then(r => r.data)

export const createAppointment = (data: AppointmentCreate) =>
  client.post<Appointment>('/appointments', data).then(r => r.data)

export const updateAppointmentStatus = (id: string, status: string) =>
  client.patch<Appointment>(`/appointments/${id}/status`, { status }).then(r => r.data)
