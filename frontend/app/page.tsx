import { ArrowRight } from "lucide-react"
import Link from "next/link"
import { CategorySection } from "@/app/components/category-section"
import { categories } from "@/lib/data"
import { Button } from "@/app/components/ui/button"
import HeroSection from "@/app/components/HeroSection"
import Search from "@/app/components/Search"
import { FAQ } from "@/app/components/ui/faq-section"

export default function Home() {
  return (
    <div className="min-h-screen bg-[#f9f9f9] bg-grid-pattern">
      <header className="container mx-auto px-4 py-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="bg-blue-900 text-white w-10 h-10 flex items-center justify-center rounded-md">
            <span className="font-bold">M</span>
          </div>
          <span className="text-xl font-bold">MCP Directory</span>
        </div>
        <div className="flex items-center gap-4">
          <Button className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors">
            Deploy
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        <HeroSection />
        {/* <Search /> */}
        <FAQ />
      </main>

      <footer className="container mx-auto px-4 py-8 mt-12 border-t border-gray-200">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <div className="bg-blue-900 text-white w-8 h-8 flex items-center justify-center rounded-md">
              <span className="font-bold">M</span>
            </div>
            <span className="text-lg font-bold">MCP Directory</span>
          </div>
          <div className="flex gap-6">
            <Link href="#" className="text-gray-600 hover:text-gray-900">
              GitHub
            </Link>
            <Link href="#" className="text-gray-600 hover:text-gray-900">
              Documentation
            </Link>
            <Link href="#" className="text-gray-600 hover:text-gray-900">
              Submit Server
            </Link>
            <Link href="#" className="text-gray-600 hover:text-gray-900">
              Contact
            </Link>
          </div>
        </div>
        <p className="text-center text-gray-500 text-sm mt-6">
          © {new Date().getFullYear()} MCP Directory - The community-driven MCP Server directory
        </p>
      </footer>
    </div>
  )
}

// import React from 'react'
// import Search from './components/Search'

// export default function HomePage() {
//   return (
//     <main className="min-h-screen p-8">
//       <Search />
//     </main>
//   )
// }
