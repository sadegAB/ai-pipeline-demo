export interface DoctorCreate {
  hospital_id: string
  department_id: string
  name: string
  specialty: string
  available_days: string[]
  available_from: string
  available_to: string
}

export interface Doctor extends DoctorCreate {
  id: string
  created_at?: string
  updated_at?: string
}