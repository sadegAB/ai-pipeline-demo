export interface AppointmentCreate {
  doctor_id: string
  patient_name: string
  patient_phone: string
  date: string
  time: string
  notes?: string
}

export interface Appointment extends AppointmentCreate {
  id: string
  status: string
  created_at?: string
  updated_at?: string
}