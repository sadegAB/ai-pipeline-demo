export interface DepartmentCreate {
  hospital_id: string
  name: string
  description?: string
}

export interface Department extends DepartmentCreate {
  id: string
  created_at?: string
  updated_at?: string
}