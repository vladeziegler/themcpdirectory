export interface ServerData {
  id: string
  name: string
  provider: string
  description: string
  logoUrl?: string
  tags: string[]
  category: "file-management" | "web-browsing" | "communication" | "development"
}

export interface CategoryData {
  id: string
  title: string
  servers: ServerData[]
}


// export interface ServerData {
//   id: string
//   name: string
//   provider: string
//   description: string
//   logoUrl?: string
//   tags: string[]
//   category: "file-management" | "web-browsing" | "communication" | "development"
// }

// export interface CategoryData {
//   id: string
//   title: string
//   servers: ServerData[]
// }
