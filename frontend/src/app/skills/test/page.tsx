"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { 
  Play, 
  Settings, 
  Zap, 
  Code, 
  FileText, 
  Globe, 
  Brain,
  Mail,
  BarChart3,
  Sparkles,
  ArrowRight
} from "lucide-react"
import SkillConfigPanel from "@/components/agent/SkillConfigPanel"
import { toast } from "sonner"

// 技能列表
const skills = [
  { id: "text_summarize", name: "文本总结", icon: FileText, category: "文本处理", color: "blue" },
  { id: "translate", name: "翻译", icon: Globe, category: "文本处理", color: "green" },
  { id: "code_explain", name: "代码解释", icon: Code, category: "代码助手", color: "purple" },
  { id: "learning_plan", name: "学习计划", icon: Brain, category: "学习助手", color: "orange" },
  { id: "email_writer", name: "邮件撰写", icon: Mail, category: "办公助手", color: "red" },
  { id: "data_analysis", name: "数据分析", icon: BarChart3, category: "分析工具", color: "indigo" },
]

export default function SkillsTestPage() {
  const [selectedSkill, setSelectedSkill] = useState(skills[0])
  const [activeTab, setActiveTab] = useState("config")
  const [testHistory, setTestHistory] = useState<any[]>([])
  const [isExecuting, setIsExecuting] = useState(false)

  // 处理保存配置
  const handleSaveConfig = (config: any) => {
    console.log("保存配置:", config)
    // TODO: 保存到本地存储或API
  }

  // 处理测试执行
  const handleTestSkill = (testData: any) => {
    console.log("测试数据:", testData)
    
    // 添加到测试历史
    setTestHistory(prev => [{
      ...testData,
      id: Date.now(),
      timestamp: new Date().toLocaleTimeString(),
      skillName: selectedSkill.name
    }, ...prev.slice(0, 9)]) // 保留最近10条
    
    toast.success("测试已记录", {
      description: `${selectedSkill.name} 测试完成`
    })
  }

  // 批量测试所有技能
  const handleBatchTest = async () => {
    setIsExecuting(true)
    toast.info("开始批量测试...")
    
    try {
      // 模拟批量测试
      for (let i = 0; i < Math.min(3, skills.length); i++) {
        const skill = skills[i]
        
        toast.info(`测试: ${skill.name}`)
        
        // 模拟执行延迟
        await new Promise(resolve => setTimeout(resolve, 800))
        
        // 添加到历史
        setTestHistory(prev => [{
          id: Date.now() + i,
          skillId: skill.id,
          skillName: skill.name,
          input: `测试 ${skill.name} 的输入内容`,
          output: `这是 ${skill.name} 的模拟输出结果`,
          timestamp: new Date().toLocaleTimeString(),
          success: true
        }, ...prev])
      }
      
      toast.success("批量测试完成", {
        description: `已测试 ${Math.min(3, skills.length)} 个技能`
      })
    } catch (error) {
      toast.error("批量测试失败")
    } finally {
      setIsExecuting(false)
    }
  }

  // 清除测试历史
  const handleClearHistory = () => {
    setTestHistory([])
    toast.info("测试历史已清除")
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">技能测试中心</h1>
              <p className="text-gray-600 mt-2">
                测试和配置AI助手的各种技能，确保它们按预期工作
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="gap-1">
                <Sparkles className="h-3 w-3" />
                开发中
              </Badge>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 左侧技能列表 */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  技能库
                </CardTitle>
                <CardDescription>
                  选择要测试和配置的技能
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {skills.map((skill) => {
                  const Icon = skill.icon
                  const isSelected = selectedSkill.id === skill.id
                  
                  return (
                    <div
                      key={skill.id}
                      className={`p-3 rounded-lg cursor-pointer transition-all ${
                        isSelected 
                          ? `bg-${skill.color}-50 border-2 border-${skill.color}-200` 
                          : "hover:bg-gray-50 border border-transparent"
                      }`}
                      onClick={() => setSelectedSkill(skill)}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`p-2 rounded-md bg-${skill.color}-100`}>
                          <Icon className={`h-5 w-5 text-${skill.color}-600`} />
                        </div>
                        <div className="flex-1">
                          <div className="font-medium">{skill.name}</div>
                          <div className="text-xs text-gray-500">{skill.category}</div>
                        </div>
                        {isSelected && (
                          <ArrowRight className="h-4 w-4 text-gray-400" />
                        )}
                      </div>
                    </div>
                  )
                })}
                
                <div className="pt-4 border-t">
                  <Button 
                    variant="outline" 
                    className="w-full gap-2"
                    onClick={handleBatchTest}
                    disabled={isExecuting}
                  >
                    <Play className="h-4 w-4" />
                    {isExecuting ? "批量测试中..." : "快速批量测试"}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* 测试历史 */}
            {testHistory.length > 0 && (
              <Card className="mt-6">
                <CardHeader>
                  <CardTitle className="text-sm">最近测试</CardTitle>
                  <CardDescription>
                    最近10次测试记录
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-2 max-h-60 overflow-y-auto">
                  {testHistory.map((test) => (
                    <div key={test.id} className="p-2 border rounded text-sm">
                      <div className="flex justify-between">
                        <span className="font-medium">{test.skillName}</span>
                        <span className="text-gray-500 text-xs">{test.timestamp}</span>
                      </div>
                      <div className="text-xs text-gray-600 truncate">
                        输入: {test.input}
                      </div>
                      {test.success !== undefined && (
                        <div className={`text-xs ${test.success ? 'text-green-600' : 'text-red-600'}`}>
                          {test.success ? '✅ 成功' : '❌ 失败'}
                        </div>
                      )}
                    </div>
                  ))}
                </CardContent>
                <div className="px-6 pb-4">
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="w-full text-xs"
                    onClick={handleClearHistory}
                  >
                    清除历史
                  </Button>
                </div>
              </Card>
            )}
          </div>

          {/* 中间配置和测试区域 */}
          <div className="lg:col-span-2">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid grid-cols-2">
                <TabsTrigger value="config" className="gap-2">
                  <Settings className="h-4 w-4" />
                  技能配置
                </TabsTrigger>
                <TabsTrigger value="api" className="gap-2">
                  <Code className="h-4 w-4" />
                  API测试
                </TabsTrigger>
              </TabsList>

              {/* 技能配置标签页 */}
              <TabsContent value="config" className="space-y-6">
                <SkillConfigPanel
                  skillId={selectedSkill.id}
                  onSave={handleSaveConfig}
                  onTest={handleTestSkill}
                />

                <Card>
                  <CardHeader>
                    <CardTitle>技能说明</CardTitle>
                    <CardDescription>
                      {selectedSkill.name} 的使用方法和最佳实践
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <h4 className="font-medium">使用场景</h4>
                      <ul className="text-sm text-gray-600 space-y-1 list-disc pl-5">
                        <li>处理长文档和报告</li>
                        <li>提取关键信息和要点</li>
                        <li>准备会议摘要和简报</li>
                        <li>学习材料的快速复习</li>
                      </ul>
                    </div>
                    
                    <div className="space-y-2">
                      <h4 className="font-medium">最佳实践</h4>
                      <ul className="text-sm text-gray-600 space-y-1 list-disc pl-5">
                        <li>输入文本尽量清晰有条理</li>
                        <li>明确指定总结的重点方向</li>
                        <li>根据用途调整输出格式</li>
                        <li>多次测试优化参数配置</li>
                      </ul>
                    </div>
                    
                    <div className="space-y-2">
                      <h4 className="font-medium">技术细节</h4>
                      <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                        <div className="grid grid-cols-2 gap-2">
                          <div>技能ID: <code className="bg-gray-100 px-1 rounded">{selectedSkill.id}</code></div>
                          <div>类别: {selectedSkill.category}</div>
                          <div>类型: 文本处理</div>
                          <div>状态: 可用</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* API测试标签页 */}
              <TabsContent value="api" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>API测试</CardTitle>
                    <CardDescription>
                      直接调用技能执行API进行测试
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <h4 className="font-medium">API端点</h4>
                      <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm">
                        POST /api/v1/skill-execution/execute
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <h4 className="font-medium">请求示例</h4>
                      <pre className="bg-gray-900 text-gray-100 p-3 rounded text-sm overflow-x-auto">
{`{
  "skill_id": "${selectedSkill.id}",
  "input_text": "测试输入内容",
  "parameters": {
    "max_length": 500,
    "language": "中文"
  },
  "temperature": 0.7,
  "max_tokens": 1000
}`}</pre>
                    </div>
                    
                    <div className="space-y-2">
                      <h4 className="font-medium">响应示例</h4>
                      <pre className="bg-gray-900 text-gray-100 p-3 rounded text-sm overflow-x-auto">
{`{
  "success": true,
  "output": "这是技能执行的输出结果...",
  "skill_used": "${selectedSkill.name}",
  "execution_time": 1.23
}`}</pre>
                    </div>
                    
                    <div className="pt-4">
                      <Button className="w-full gap-2">
                        <Play className="h-4 w-4" />
                        调用API测试
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>批量API测试</CardTitle>
                    <CardDescription>
                      同时测试多个技能
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <h4 className="font-medium">批量API端点</h4>
                      <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm">
                        POST /api/v1/skill-execution/execute/batch
                      </div>
                    </div>
                    
                    <div className="mt-4">
                      <Button variant="outline" className="w-full gap-2">
                        <Zap className="h-4 w-4" />
                        批量测试所有技能
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>

        {/* 底部统计信息 */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{skills.length}</div>
              <div className="text-sm text-gray-500">可用技能</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{testHistory.length}</div>
              <div className="text-sm text-gray-500">测试次数</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">100%</div>
              <div className="text-sm text-gray-500">技能可用率</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">~2s</div>
              <div className="text-sm text-gray-500">平均响应时间</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}