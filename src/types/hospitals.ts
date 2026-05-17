export interface HospitalCreate {
  name: string
  address: string
  phone: string
}

export interface Hospital extends HospitalCreate {
  id: string
  created_at?: string
}