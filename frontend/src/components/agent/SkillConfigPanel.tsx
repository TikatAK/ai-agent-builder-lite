"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  Settings, 
  Play, 
  Save, 
  RefreshCw,
  Code,
  FileText,
  Globe,
  Brain,
  Zap,
  CheckCircle,
  XCircle
} from "lucide-react"
import { toast } from "sonner"

// 技能类型定义
interface SkillParameter {
  type: string
  default?: any
  required?: boolean
  description: string
  options?: string[]
  min?: number
  max?: number
  step?: number
}

interface SkillConfig {
  id: string
  name: string
  description: string
  type: string
  parameters: Record<string, SkillParameter>
  example_input?: string
  example_output?: string
}

interface SkillConfigPanelProps {
  skillId?: string
  onSave?: (config: any) => void
  onTest?: (config: any) => void
  className?: string
}

// 模拟技能数据 - 实际应该从API获取
const mockSkills: Record<string, SkillConfig> = {
  "text_summarize": {
    id: "text_summarize",
    name: "文本总结",
    description: "将长文本总结为简洁的要点",
    type: "文本处理",
    parameters: {
      "max_length": {
        type: "int",
        default: 500,
        required: false,
        description: "最大输出长度",
        min: 100,
        max: 2000,
        step: 100
      },
      "language": {
        type: "string",
        default: "中文",
        required: false,
        description: "输出语言",
        options: ["中文", "英文", "日文", "韩文"]
      },
      "format": {
        type: "string",
        default: "要点",
        required: false,
        description: "总结格式",
        options: ["要点", "段落", "表格", "思维导图"]
      }
    },
    example_input: "这是一段很长的文本内容，需要被总结...",
    example_output: "1. 第一要点\n2. 第二要点\n3. 第三要点"
  },
  "translate": {
    id: "translate",
    name: "翻译",
    description: "文本翻译",
    type: "文本处理",
    parameters: {
      "source_lang": {
        type: "string",
        default: "auto",
        required: false,
        description: "源语言",
        options: ["auto", "中文", "英文", "日文", "韩文", "法文", "德文"]
      },
      "target_lang": {
        type: "string",
        default: "英文",
        required: true,
        description: "目标语言",
        options: ["中文", "英文", "日文", "韩文", "法文", "德文"]
      },
      "formality": {
        type: "string",
        default: "default",
        required: false,
        description: "正式程度",
        options: ["formal", "default", "informal"]
      }
    },
    example_input: "你好，世界！",
    example_output: "Hello, World!"
  },
  "code_explain": {
    id: "code_explain",
    name: "代码解释",
    description: "解释代码的功能和逻辑",
    type: "代码助手",
    parameters: {
      "language": {
        type: "string",
        default: "python",
        required: true,
        description: "编程语言",
        options: ["python", "javascript", "typescript", "java", "cpp", "go", "rust"]
      },
      "detail_level": {
        type: "string",
        default: "medium",
        required: false,
        description: "详细程度",
        options: ["simple", "medium", "detailed"]
      },
      "include_examples": {
        type: "boolean",
        default: true,
        required: false,
        description: "包含示例"
      }
    },
    example_input: "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    example_output: "这是一个计算斐波那契数列的递归函数..."
  }
}

export default function SkillConfigPanel({ 
  skillId = "text_summarize", 
  onSave,
  onTest,
  className 
}: SkillConfigPanelProps) {
  const [skill, setSkill] = useState<SkillConfig | null>(null)
  const [parameterValues, setParameterValues] = useState<Record<string, any>>({})
  const [testInput, setTestInput] = useState("")
  const [testOutput, setTestOutput] = useState("")
  const [isTesting, setIsTesting] = useState(false)
  const [activeTab, setActiveTab] = useState("config")

  // 加载技能配置
  useEffect(() => {
    const loadSkill = async () => {
      try {
        // TODO: 从API获取真实数据
        const skillData = mockSkills[skillId]
        if (skillData) {
          setSkill(skillData)
          
          // 初始化参数值
          const initialValues: Record<string, any> = {}
          Object.entries(skillData.parameters).forEach(([key, param]) => {
            initialValues[key] = param.default
          })
          setParameterValues(initialValues)
          
          // 设置测试输入
          if (skillData.example_input) {
            setTestInput(skillData.example_input)
          }
        }
      } catch (error) {
        console.error("加载技能失败:", error)
        toast.error("加载技能配置失败")
      }
    }
    
    loadSkill()
  }, [skillId])

  // 处理参数值变化
  const handleParameterChange = (paramName: string, value: any) => {
    setParameterValues(prev => ({
      ...prev,
      [paramName]: value
    }))
  }

  // 保存配置
  const handleSave = () => {
    if (!skill) return
    
    const config = {
      skillId: skill.id,
      parameters: parameterValues,
      timestamp: new Date().toISOString()
    }
    
    if (onSave) {
      onSave(config)
    }
    
    toast.success("配置已保存", {
      description: `已保存 ${skill.name} 的配置`
    })
  }

  // 测试技能
  const handleTest = async () => {
    if (!skill || !testInput.trim()) {
      toast.error("请输入测试内容")
      return
    }
    
    setIsTesting(true)
    setTestOutput("")
    
    try {
      // TODO: 调用真实API
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // 模拟响应
      const mockResponse = `这是 ${skill.name} 的测试输出。\n\n参数配置：${JSON.stringify(parameterValues, null, 2)}\n\n输入内容：${testInput}\n\n输出结果：${skill.example_output || "测试输出内容"}`
      
      setTestOutput(mockResponse)
      toast.success("测试完成", {
        description: `${skill.name} 执行成功`
      })
      
      if (onTest) {
        onTest({
          skillId: skill.id,
          input: testInput,
          output: mockResponse,
          parameters: parameterValues
        })
      }
    } catch (error) {
      console.error("测试失败:", error)
      toast.error("测试失败", {
        description: "请检查网络连接或参数配置"
      })
    } finally {
      setIsTesting(false)
    }
  }

  // 重置配置
  const handleReset = () => {
    if (!skill) return
    
    const initialValues: Record<string, any> = {}
    Object.entries(skill.parameters).forEach(([key, param]) => {
      initialValues[key] = param.default
    })
    setParameterValues(initialValues)
    
    toast.info("配置已重置", {
      description: "已恢复默认参数"
    })
  }

  // 渲染参数输入控件
  const renderParameterInput = (paramName: string, param: SkillParameter) => {
    const value = parameterValues[paramName]
    
    switch (param.type) {
      case "string":
        if (param.options) {
          return (
            <Select value={value} onValueChange={(val) => handleParameterChange(paramName, val)}>
              <SelectTrigger>
                <SelectValue placeholder={`选择${param.description}`} />
              </SelectTrigger>
              <SelectContent>
                {param.options.map(option => (
                  <SelectItem key={option} value={option}>
                    {option}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )
        }
        return (
          <Input
            value={value || ""}
            onChange={(e) => handleParameterChange(paramName, e.target.value)}
            placeholder={param.description}
          />
        )
      
      case "int":
      case "number":
        if (param.min !== undefined && param.max !== undefined) {
          return (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">{value}</span>
                {param.description && (
                  <span className="text-sm text-gray-500">{param.description}</span>
                )}
              </div>
              <Slider
                value={[value]}
                onValueChange={(vals) => handleParameterChange(paramName, vals[0])}
                min={param.min}
                max={param.max}
                step={param.step || 1}
              />
            </div>
          )
        }
        return (
          <Input
            type="number"
            value={value}
            onChange={(e) => handleParameterChange(paramName, Number(e.target.value))}
            placeholder={param.description}
          />
        )
      
      case "boolean":
        return (
          <div className="flex items-center space-x-2">
            <Switch
              checked={value}
              onCheckedChange={(checked) => handleParameterChange(paramName, checked)}
            />
            <Label>{param.description}</Label>
          </div>
        )
      
      case "text":
        return (
          <Textarea
            value={value || ""}
            onChange={(e) => handleParameterChange(paramName, e.target.value)}
            placeholder={param.description}
            rows={3}
          />
        )
      
      default:
        return (
          <Input
            value={value || ""}
            onChange={(e) => handleParameterChange(paramName, e.target.value)}
            placeholder={param.description}
          />
        )
    }
  }

  if (!skill) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-gray-400" />
            <div className="text-gray-500">加载技能配置中...</div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              {skill.name} 配置
            </CardTitle>
            <CardDescription>{skill.description}</CardDescription>
          </div>
          <Badge variant="outline" className="gap-1">
            {skill.type === "文本处理" && <FileText className="h-3 w-3" />}
            {skill.type === "代码助手" && <Code className="h-3 w-3" />}
            {skill.type === "学习助手" && <Brain className="h-3 w-3" />}
            {skill.type === "翻译" && <Globe className="h-3 w-3" />}
            {skill.type}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid grid-cols-2">
            <TabsTrigger value="config" className="gap-2">
              <Settings className="h-4 w-4" />
              参数配置
            </TabsTrigger>
            <TabsTrigger value="test" className="gap-2">
              <Play className="h-4 w-4" />
              测试执行
            </TabsTrigger>
          </TabsList>

          {/* 参数配置标签页 */}
          <TabsContent value="config" className="space-y-6">
            <div className="space-y-4">
              {Object.entries(skill.parameters).map(([paramName, param]) => (
                <div key={paramName} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor={paramName} className="capitalize">
                      {paramName}
                      {param.required && (
                        <span className="text-red-500 ml-1">*</span>
                      )}
                    </Label>
                    {param.required && (
                      <span className="text-xs text-gray-500">必填</span>
                    )}
                  </div>
                  
                  {renderParameterInput(paramName, param)}
                  
                  <div className="text-xs text-gray-500">
                    {param.description}
                    {param.default !== undefined && (
                      <span className="ml-2">
                        默认值: <code className="bg-gray-100 px-1 rounded">{String(param.default)}</code>
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-2 pt-4 border-t">
              <Button onClick={handleSave} className="flex-1 gap-2">
                <Save className="h-4 w-4" />
                保存配置
              </Button>
              <Button variant="outline" onClick={handleReset} className="gap-2">
                <RefreshCw className="h-4 w-4" />
                重置
              </Button>
            </div>
          </TabsContent>

          {/* 测试执行标签页 */}
          <TabsContent value="test" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="test-input">测试输入</Label>
              <Textarea
                id="test-input"
                value={testInput}
                onChange={(e) => setTestInput(e.target.value)}
                placeholder="输入测试内容..."
                rows={4}
                className="font-mono text-sm"
              />
              {skill.example_input && (
                <div className="text-xs text-gray-500">
                  示例: {skill.example_input}
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label>当前参数配置</Label>
              <div className="bg-gray-50 p-3 rounded-md text-sm">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(parameterValues, null, 2)}
                </pre>
              </div>
            </div>

            <Button 
              onClick={handleTest} 
              disabled={isTesting || !testInput.trim()}
              className="w-full gap-2"
            >
              {isTesting ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  测试中...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  执行测试
                </>
              )}
            </Button>

            {testOutput && (
              <div className="space-y-2 pt-4 border-t">
                <Label className="flex items-center gap-2">
                  <Zap className="h-4 w-4" />
                  测试输出
                </Label>
                <div className="bg-green-50 border border-green-200 p-3 rounded-md">
                  <pre className="whitespace-pre-wrap text-sm">{testOutput}</pre>
                </div>
                <div className="flex items-center gap-2 text-sm text-green-600">
                  <CheckCircle className="h-4 w-4" />
                  测试成功完成
                </div>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}