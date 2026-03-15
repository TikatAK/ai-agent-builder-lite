import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Rocket, Sparkles, Zap, Users, Code, Globe } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 md:py-24">
        <div className="text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center justify-center p-2 bg-primary/10 rounded-full mb-6">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="ml-2 text-sm font-semibold text-primary">AI Agent Builder Lite</span>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
            让每个人都能轻松创建
            <span className="text-primary block mt-2">专属AI助手</span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            无需编程经验，通过可视化界面配置你的AI助手。支持多模型、技能市场、一键部署。
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="gap-2" asChild>
              <Link href="/agents/create">
                <Rocket className="h-5 w-5" />
                立即创建Agent
              </Link>
            </Button>
            <Button size="lg" variant="outline" className="gap-2" asChild>
              <Link href="/docs">
                <Code className="h-5 w-5" />
                查看文档
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">核心功能</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            专为大学生、个人开发者和小团队设计的AI助手创建平台
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <div className="p-2 bg-blue-100 rounded-lg w-fit mb-4">
                <Zap className="h-6 w-6 text-blue-600" />
              </div>
              <CardTitle>可视化配置</CardTitle>
              <CardDescription>拖拽式界面，无需代码</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                通过直观的拖拽界面配置AI助手的行为、技能和响应方式。
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="p-2 bg-green-100 rounded-lg w-fit mb-4">
                <Globe className="h-6 w-6 text-green-600" />
              </div>
              <CardTitle>多模型支持</CardTitle>
              <CardDescription>OpenAI、Claude、DeepSeek等</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                支持主流AI模型，可根据需求灵活切换，平衡性能与成本。
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="p-2 bg-purple-100 rounded-lg w-fit mb-4">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <CardTitle>技能市场</CardTitle>
              <CardDescription>预置技能和社区贡献</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                丰富的技能库，从基础对话到专业工具，一键添加到你的Agent。
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16">
        <Card className="max-w-4xl mx-auto bg-gradient-to-r from-primary/5 to-primary/10 border-primary/20">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">立即开始你的AI助手之旅</CardTitle>
            <CardDescription>
              完全免费开始，无需信用卡。学生和开发者友好。
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary mb-2">0元</div>
                <div className="text-gray-600">开始使用</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary mb-2">5分钟</div>
                <div className="text-gray-600">创建第一个Agent</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary mb-2">无限</div>
                <div className="text-gray-600">自定义可能性</div>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-center">
            <Button size="lg" className="gap-2" asChild>
              <Link href="/agents/create">
                <Sparkles className="h-5 w-5" />
                免费开始创建
              </Link>
            </Button>
          </CardFooter>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>AI Agent Builder Lite © 2026 - 开源项目，遵循 MIT 许可证</p>
          <p className="mt-2 text-sm">
            GitHub:{" "}
            <a 
              href="https://github.com/TikatAK/ai-agent-builder-lite" 
              className="text-primary hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              TikatAK/ai-agent-builder-lite
            </a>
          </p>
        </div>
      </footer>
    </div>
  )
}