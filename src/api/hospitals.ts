import client from './client'
import type { Hospital, HospitalCreate } from '../types/hospitals'

export const getHospitals = () =>
  client.get<Hospital[]>('/hospitals').then(r => r.data)

export const getHospital = (id: string) =>
  client.get<Hospital>(`/hospitals/${id}`).then(r => r.data)

export const createHospital = (data: HospitalCreate) =>
  client.post<Hospital>('/hospitals', data).then(r => r.data)
