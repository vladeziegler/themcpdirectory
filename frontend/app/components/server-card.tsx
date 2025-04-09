import { Star } from "lucide-react"
import Image from "next/image"
import { Button } from "@/app/components/ui/button"
import { Badge } from "@/app/components/ui/badge"
import type { ServerData } from "@/lib/types"

interface ServerCardProps {
  server: ServerData
}

export function ServerCard({ server }: ServerCardProps) {
  return (
    <div className="bg-white rounded-xl p-6 border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-3">
          <div className="bg-blue-50 p-2 rounded-lg">
            <Image
              src={server.logoUrl || "/placeholder.svg?height=40&width=40"}
              alt={server.name}
              width={40}
              height={40}
            />
          </div>
          <div>
            <h3 className="font-bold">{server.name}</h3>
            <p className="text-sm text-gray-500">by {server.provider}</p>
          </div>
        </div>
        <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
      </div>
      <p className="text-sm mb-4 line-clamp-2">{server.description}</p>
      <div className="flex flex-wrap gap-2 mb-4">
        {server.tags.map((tag, index) => (
          <Badge key={index} variant="secondary" className="text-xs bg-gray-100 hover:bg-gray-200">
            {tag}
          </Badge>
        ))}
      </div>
      <div className="flex justify-end">
        <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-600 hover:bg-red-50">
          Deploy
        </Button>
      </div>
    </div>
  )
}

// export default ServerCard
