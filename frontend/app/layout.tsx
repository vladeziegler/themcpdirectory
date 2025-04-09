import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

// Use Inter font which is more minimalistic
const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  display: "swap",
})

export const metadata: Metadata = {
  title: "MCP Directory | Find the best MCP servers for your AI agents",
  description: "Discover and explore the largest collection of MCP Servers to enhance your AI applications",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}

// import './globals.css'
// import type { Metadata } from 'next'

// export const metadata: Metadata = {
//   title: 'Modo Search',
//   description: 'Search MCP descriptions and capabilities',
// }

// export default function RootLayout({
//   children,
// }: {
//   children: React.ReactNode
// }) {
//   return (
//     <html lang="en">
//       <body>{children}</body>
//     </html>
//   )
// }
