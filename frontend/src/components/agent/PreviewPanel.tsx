"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Bot, Cpu, Zap, Eye, CheckCircle, Clock } from "lucide-react"

interface PreviewPanelProps {
  agentName: string
  description: string
  model: string
  temperature: number
}

export default function PreviewPanel({ 
  agentName, 
  description, 
  model, 
  temperature 
}: PreviewPanelProps) {
  
  const getModelInfo = (modelId: string) => {
    const models: Record<string, { name: string, provider: string, cost: string }> = {
      "gpt-4-turbo": { name: "GPT-4 Turbo", provider: "OpenAI", cost: "$0.03/1K tokens" },
      "gpt-3.5-turbo": { name: "GPT-3.5 Turbo", provider: "OpenAI", cost: "$0.002/1K tokens" },
      "claude-3-opus": { name: "Claude 3 Opus", provider: "Anthropic", cost: "$0.15/1K tokens" },
      "claude-3-sonnet": { name: "Claude 3 Sonnet", provider: "Anthropic", cost: "$0.03/1K tokens" },
      "deepseek-chat": { name: "DeepSeek Chat", provider: "DeepSeek", cost: "免费" },
      "moonshot-v1": { name: "Moonshot v1", provider: "Moonshot", cost: "$0.012/1K tokens" },
    }
    return models[modelId] || { name: "未知模型", provider: "未知", cost: "未知" }
  }

  const modelInfo = getModelInfo(model)
  
  const getTemperatureColor = (temp: number) => {
    if (temp < 0.3) return "text-blue-600 bg-blue-100"
    if (temp < 0.7) return "text-green-600 bg-green-100"
    return "text-orange-600 bg-orange-100"
  }

  const getTemperatureLabel = (temp: number) => {
    if (temp < 0.3) return "精确模式"
    if (temp < 0.7) return "平衡模式"
    return "创意模式"
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Eye className="h-5 w-5" />
          实时预览
        </CardTitle>
        <CardDescription>
          查看你的AI助手配置效果
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Agent概览 */}
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Bot className="h-6 w-6 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-lg">{agentName || "未命名Agent"}</h3>
              <p className="text-sm text-gray-600 mt-1">
                {description || "暂无描述"}
              </p>
            </div>
            <Badge variant="outline" className="gap-1">
              <CheckCircle className="h-3 w-3" />
              就绪
            </Badge>
          </div>

          {/* 配置状态 */}
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <div className="flex items-center gap-1 text-sm text-gray-500">
                <Cpu className="h-4 w-4" />
                <span>模型</span>
              </div>
              <div className="font-medium">{modelInfo.name}</div>
              <div className="text-xs text-gray-500">{modelInfo.provider}</div>
            </div>
            
            <div className="space-y-1">
              <div className="flex items-center gap-1 text-sm text-gray-500">
                <Zap className="h-4 w-4" />
                <span>温度</span>
              </div>
              <div className="font-medium">{temperature.toFixed(1)}</div>
              <div className={`text-xs px-2 py-0.5 rounded-full w-fit ${getTemperatureColor(temperature)}`}>
                {getTemperatureLabel(temperature)}
              </div>
            </div>
          </div>
        </div>

        {/* 成本估算 */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">预计成本</span>
            <span className="text-sm font-semibold">{modelInfo.cost}</span>
          </div>
          <Progress value={temperature * 100} className="h-2" />
          <div className="flex justify-between text-xs text-gray-500">
            <span>低成本</span>
            <span>平衡</span>
            <span>高质量</span>
          </div>
        </div>

        {/* 性能指标 */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">响应速度</span>
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span className="font-medium">~2秒</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">上下文长度</span>
            <span className="font-medium">128K tokens</span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">支持格式</span>
            <div className="flex gap-1">
              <Badge variant="outline" className="text-xs">文本</Badge>
              <Badge variant="outline" className="text-xs">JSON</Badge>
              <Badge variant="outline" className="text-xs">Markdown</Badge>
            </div>
          </div>
        </div>

        {/* 预览对话 */}
        <div className="space-y-3">
          <h4 className="text-sm font-medium">对话预览</h4>
          <div className="space-y-2">
            <div className="bg-gray-100 rounded-lg p-3">
              <div className="text-xs text-gray-500 mb-1">用户</div>
              <div className="text-sm">你好，请介绍一下你自己</div>
            </div>
            <div className="bg-primary/5 rounded-lg p-3">
              <div className="text-xs text-gray-500 mb-1">AI助手</div>
              <div className="text-sm">
                你好！我是{agentName || "你的AI助手"}，{description || "一个帮助你的AI助手"}。
                有什么我可以帮助你的吗？
              </div>
            </div>
          </div>
        </div>

        {/* 部署状态 */}
        <div className="pt-4 border-t">
          <div className="flex items-center justify-between">
            <div className="text-sm">
              <div className="font-medium">部署状态</div>
              <div className="text-gray-500">本地测试环境</div>
            </div>
            <Badge variant="secondary">可部署</Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}