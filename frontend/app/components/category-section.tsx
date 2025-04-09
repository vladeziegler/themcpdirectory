import type { ServerData } from "@/lib/types"
import { ServerCard } from "@/components/server-card"
import { ArrowRight } from "lucide-react"
import Link from "next/link"

interface CategorySectionProps {
  title: string
  servers: ServerData[]
}

export function CategorySection({ title, servers }: CategorySectionProps) {
  return (
    <section className="mb-12">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">{title}</h2>
        <Link href="#" className="text-red-500 hover:underline flex items-center">
          View All <ArrowRight className="ml-1 h-4 w-4" />
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {servers.map((server) => (
          <ServerCard key={server.id} server={server} />
        ))}
      </div>
    </section>
  )
}

// export default CategorySection
