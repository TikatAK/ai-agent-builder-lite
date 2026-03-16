"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { 
  Save, 
  Play, 
  Upload, 
  Download, 
  Settings, 
  MessageSquare,
  Cpu,
  Zap,
  Sparkles,
  Eye,
  Code,
  Bot
} from "lucide-react"
import AgentFlowEnhanced from "@/components/agent/AgentFlowEnhanced"
import SkillLibrary from "@/components/agent/SkillLibrary"
import PreviewPanel from "@/components/agent/PreviewPanel"

export default function CreateAgentPage() {
  const [agentName, setAgentName] = useState("我的AI助手")
  const [description, setDescription] = useState("一个帮助我处理日常任务的AI助手")
  const [systemPrompt, setSystemPrompt] = useState("你是一个有帮助的AI助手，请用友好、专业的语气回答用户的问题。")
  const [selectedModel, setSelectedModel] = useState("gpt-4-turbo")
  const [temperature, setTemperature] = useState([0.7])
  const [maxTokens, setMaxTokens] = useState(2048)
  const [isPublic, setIsPublic] = useState(false)
  const [activeTab, setActiveTab] = useState("config")

  const models = [
    { id: "gpt-4-turbo", name: "GPT-4 Turbo", provider: "OpenAI" },
    { id: "gpt-3.5-turbo", name: "GPT-3.5 Turbo", provider: "OpenAI" },
    { id: "claude-3-opus", name: "Claude 3 Opus", provider: "Anthropic" },
    { id: "claude-3-sonnet", name: "Claude 3 Sonnet", provider: "Anthropic" },
    { id: "deepseek-chat", name: "DeepSeek Chat", provider: "DeepSeek" },
    { id: "moonshot-v1", name: "Moonshot v1", provider: "Moonshot" },
  ]

  const handleSave = () => {
    // 这里会实现保存逻辑
    console.log("保存Agent配置")
  }

  const handleTest = () => {
    // 这里会实现测试逻辑
    console.log("测试Agent")
  }

  const handleExport = () => {
    // 这里会实现导出逻辑
    console.log("导出配置")
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">创建AI助手</h1>
              <p className="text-gray-600 mt-2">
                通过可视化界面配置你的专属AI助手
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="gap-1">
                <Sparkles className="h-3 w-3" />
                预览版
              </Badge>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 左侧配置面板 */}
          <div className="lg:col-span-2 space-y-6">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid grid-cols-3">
                <TabsTrigger value="config" className="gap-2">
                  <Settings className="h-4 w-4" />
                  基础配置
                </TabsTrigger>
                <TabsTrigger value="skills" className="gap-2">
                  <Zap className="h-4 w-4" />
                  技能配置
                </TabsTrigger>
                <TabsTrigger value="flow" className="gap-2">
                  <Code className="h-4 w-4" />
                  流程设计
                </TabsTrigger>
              </TabsList>

              {/* 基础配置标签页 */}
              <TabsContent value="config" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Bot className="h-5 w-5" />
                      Agent基本信息
                    </CardTitle>
                    <CardDescription>
                      设置你的AI助手的基本信息和身份
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="agent-name">Agent名称</Label>
                      <Input
                        id="agent-name"
                        placeholder="例如：学习助手、工作伙伴"
                        value={agentName}
                        onChange={(e) => setAgentName(e.target.value)}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="description">描述</Label>
                      <Textarea
                        id="description"
                        placeholder="描述你的AI助手的主要功能和特点"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        rows={3}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="system-prompt">系统提示词</Label>
                      <Textarea
                        id="system-prompt"
                        placeholder="定义AI助手的行为准则和角色设定"
                        value={systemPrompt}
                        onChange={(e) => setSystemPrompt(e.target.value)}
                        rows={6}
                        className="font-mono text-sm"
                      />
                      <p className="text-sm text-gray-500">
                        提示词越具体，AI助手的行为越符合预期
                      </p>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="public-mode"
                          checked={isPublic}
                          onCheckedChange={setIsPublic}
                        />
                        <Label htmlFor="public-mode">公开此Agent</Label>
                      </div>
                      <Badge variant={isPublic ? "default" : "outline"}>
                        {isPublic ? "公开" : "私有"}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Cpu className="h-5 w-5" />
                      模型配置
                    </CardTitle>
                    <CardDescription>
                      选择AI模型和调整参数
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-2">
                      <Label>选择模型</Label>
                      <Select value={selectedModel} onValueChange={setSelectedModel}>
                        <SelectTrigger>
                          <SelectValue placeholder="选择AI模型" />
                        </SelectTrigger>
                        <SelectContent>
                          {models.map((model) => (
                            <SelectItem key={model.id} value={model.id}>
                              <div className="flex items-center justify-between">
                                <span>{model.name}</span>
                                <Badge variant="outline" className="ml-2">
                                  {model.provider}
                                </Badge>
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <Label>温度：{temperature[0].toFixed(1)}</Label>
                          <span className="text-sm text-gray-500">
                            {temperature[0] < 0.3 ? "确定性高" : 
                             temperature[0] < 0.7 ? "平衡" : "创造性高"}
                          </span>
                        </div>
                        <Slider
                          value={temperature}
                          onValueChange={setTemperature}
                          max={1}
                          step={0.1}
                          className="w-full"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>精确</span>
                          <span>平衡</span>
                          <span>创意</span>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <Label htmlFor="max-tokens">最大Token数</Label>
                          <span className="text-sm font-medium">{maxTokens}</span>
                        </div>
                        <Slider
                          id="max-tokens"
                          value={[maxTokens]}
                          onValueChange={(value) => setMaxTokens(value[0])}
                          max={4096}
                          step={256}
                          className="w-full"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>简短</span>
                          <span>适中</span>
                          <span>详细</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* 技能配置标签页 */}
              <TabsContent value="skills">
                <SkillLibrary />
              </TabsContent>

              {/* 流程设计标签页 */}
              <TabsContent value="flow">
                <AgentFlowEnhanced />
              </TabsContent>
            </Tabs>
          </div>

          {/* 右侧预览和操作面板 */}
          <div className="space-y-6">
            {/* 预览面板 */}
            <PreviewPanel
              agentName={agentName}
              description={description}
              model={selectedModel}
              temperature={temperature[0]}
            />

            {/* 操作按钮 */}
            <Card>
              <CardHeader>
                <CardTitle>操作</CardTitle>
                <CardDescription>保存、测试或导出你的Agent</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="w-full gap-2" onClick={handleSave}>
                  <Save className="h-4 w-4" />
                  保存Agent
                </Button>
                <Button variant="outline" className="w-full gap-2" onClick={handleTest}>
                  <Play className="h-4 w-4" />
                  测试对话
                </Button>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm" className="gap-2" onClick={handleExport}>
                    <Download className="h-4 w-4" />
                    导出
                  </Button>
                  <Button variant="outline" size="sm" className="gap-2">
                    <Upload className="h-4 w-4" />
                    导入
                  </Button>
                </div>
              </CardContent>
              <CardFooter className="border-t pt-4">
                <div className="text-sm text-gray-500 w-full">
                  <div className="flex justify-between mb-1">
                    <span>预计成本</span>
                    <span className="font-medium">$0.02/次</span>
                  </div>
                  <div className="flex justify-between">
                    <span>响应时间</span>
                    <span className="font-medium">~2秒</span>
                  </div>
                </div>
              </CardFooter>
            </Card>

            {/* 快速提示 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-sm">
                  <MessageSquare className="h-4 w-4" />
                  配置提示
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-gray-600 space-y-2">
                <p>• 给Agent起一个具体的名字，更容易记住</p>
                <p>• 系统提示词要明确AI助手的角色和边界</p>
                <p>• 温度值影响回答的创造性，建议从0.7开始</p>
                <p>• 可以先保存基础配置，后续再添加技能</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}