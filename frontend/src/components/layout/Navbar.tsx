import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Bot, Home, Users, Book, Settings, User } from "lucide-react"

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <Link href="/" className="flex items-center gap-2">
            <div className="p-1.5 bg-primary/10 rounded-lg">
              <Bot className="h-5 w-5 text-primary" />
            </div>
            <span className="font-bold text-lg">AI Agent Builder</span>
            <span className="text-xs px-2 py-0.5 bg-primary/10 text-primary rounded-full">
              Lite
            </span>
          </Link>
        </div>

        {/* 导航链接 */}
        <div className="hidden md:flex items-center gap-1">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/" className="gap-2">
              <Home className="h-4 w-4" />
              首页
            </Link>
          </Button>
          <Button variant="ghost" size="sm" asChild>
            <Link href="/agents" className="gap-2">
              <Bot className="h-4 w-4" />
              我的Agents
            </Link>
          </Button>
          <Button variant="ghost" size="sm" asChild>
            <Link href="/skills" className="gap-2">
              <Users className="h-4 w-4" />
              技能市场
            </Link>
          </Button>
          <Button variant="ghost" size="sm" asChild>
            <Link href="/docs" className="gap-2">
              <Book className="h-4 w-4" />
              文档
            </Link>
          </Button>
        </div>

        {/* 用户操作 */}
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link href="/agents/create" className="gap-2">
              <Bot className="h-4 w-4" />
              创建Agent
            </Link>
          </Button>
          <Button size="sm" variant="ghost" className="h-9 w-9 p-0">
            <User className="h-4 w-4" />
          </Button>
          <Button size="sm" variant="ghost" className="h-9 w-9 p-0">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </nav>
  )
}