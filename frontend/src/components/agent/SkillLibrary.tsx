"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Search, Plus, Star, Zap, Globe, Calculator, Calendar, FileText, MessageSquare, Database } from "lucide-react"

const skills = [
  { id: 1, name: "网页搜索", icon: Globe, description: "搜索最新网页信息", category: "工具", popularity: 95 },
  { id: 2, name: "计算器", icon: Calculator, description: "数学计算和单位转换", category: "工具", popularity: 88 },
  { id: 3, name: "日历管理", icon: Calendar, description: "查看和添加日历事件", category: "生产力", popularity: 76 },
  { id: 4, name: "文档分析", icon: FileText, description: "读取和分析文档内容", category: "办公", popularity: 82 },
  { id: 5, name: "对话记忆", icon: MessageSquare, description: "记住对话历史和上下文", category: "核心", popularity: 92 },
  { id: 6, name: "数据查询", icon: Database, description: "查询数据库和API数据", category: "开发", popularity: 68 },
  { id: 7, name: "天气查询", icon: Globe, description: "获取实时天气信息", category: "工具", popularity: 85 },
  { id: 8, name: "代码生成", icon: Zap, description: "生成和解释代码", category: "开发", popularity: 90 },
]

const categories = ["全部", "工具", "生产力", "办公", "核心", "开发"]

export default function SkillLibrary() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("全部")
  const [selectedSkills, setSelectedSkills] = useState<number[]>([])

  const filteredSkills = skills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         skill.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === "全部" || skill.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const toggleSkill = (skillId: number) => {
    setSelectedSkills(prev => 
      prev.includes(skillId) 
        ? prev.filter(id => id !== skillId)
        : [...prev, skillId]
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              技能市场
            </CardTitle>
            <CardDescription>
              选择并添加技能到你的AI助手
            </CardDescription>
          </div>
          <Badge variant="outline">
            {selectedSkills.length} 个已选择
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* 搜索和筛选 */}
        <div className="space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="搜索技能..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <div className="flex flex-wrap gap-2">
            {categories.map(category => (
              <Button
                key={category}
                size="sm"
                variant={selectedCategory === category ? "default" : "outline"}
                onClick={() => setSelectedCategory(category)}
              >
                {category}
              </Button>
            ))}
          </div>
        </div>

        {/* 技能网格 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredSkills.map(skill => {
            const Icon = skill.icon
            const isSelected = selectedSkills.includes(skill.id)
            
            return (
              <Card 
                key={skill.id} 
                className={`cursor-pointer transition-all hover:shadow-md ${
                  isSelected ? "ring-2 ring-primary" : ""
                }`}
                onClick={() => toggleSkill(skill.id)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      <div className={`p-2 rounded-lg ${
                        isSelected ? "bg-primary/10" : "bg-gray-100"
                      }`}>
                        <Icon className={`h-5 w-5 ${
                          isSelected ? "text-primary" : "text-gray-600"
                        }`} />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-semibold">{skill.name}</h4>
                          <Badge variant="outline" className="text-xs">
                            {skill.category}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{skill.description}</p>
                      </div>
                    </div>
                    <Button
                      size="sm"
                      variant={isSelected ? "default" : "outline"}
                      className="ml-2"
                      onClick={(e) => {
                        e.stopPropagation()
                        toggleSkill(skill.id)
                      }}
                    >
                      {isSelected ? "已添加" : "添加"}
                    </Button>
                  </div>
                  
                  <div className="flex items-center justify-between mt-4">
                    <div className="flex items-center gap-1 text-sm text-gray-500">
                      <Star className="h-4 w-4 text-yellow-500" />
                      <span>{skill.popularity}%</span>
                      <span className="ml-2">使用率</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      点击{isSelected ? "移除" : "添加"}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* 空状态 */}
        {filteredSkills.length === 0 && (
          <div className="text-center py-8">
            <div className="p-3 bg-gray-100 rounded-full w-fit mx-auto mb-4">
              <Search className="h-6 w-6 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold mb-2">未找到相关技能</h3>
            <p className="text-gray-600">
              尝试不同的搜索词或选择其他分类
            </p>
          </div>
        )}

        {/* 操作按钮 */}
        <div className="flex items-center justify-between pt-4 border-t">
          <div className="text-sm text-gray-600">
            已选择 {selectedSkills.length} 个技能，最多可添加 10 个技能
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => setSelectedSkills([])}>
              清空选择
            </Button>
            <Button className="gap-2" disabled={selectedSkills.length === 0}>
              <Plus className="h-4 w-4" />
              添加到Agent
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}