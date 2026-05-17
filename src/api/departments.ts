import client from './client'
import type { Department, DepartmentCreate } from '../types/departments'

export const getDepartments = () =>
  client.get<Department[]>('/departments').then(r => r.data)

export const getDepartment = (id: string) =>
  client.get<Department>(`/departments/${id}`).then(r => r.data)

export const createDepartment = (data: DepartmentCreate) =>
  client.post<Department>('/departments', data).then(r => r.data)

export const getDepartmentsByHospitalId = (hospitalId: string) =>
  client.get<Department[]>(`/hospitals/${hospitalId}/departments`).then(r => r.data)
