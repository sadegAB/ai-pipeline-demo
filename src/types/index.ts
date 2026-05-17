export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface ApiError {
  detail: string
  status: number
}

export interface BaseEntity {
  id: string
  created_at?: string
  updated_at?: string
}
export * from './hospitals'
export * from './departments'
export * from './doctors'
export * from './appointments'
