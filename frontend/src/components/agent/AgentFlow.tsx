"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus, Trash2, Move, Link as LinkIcon } from "lucide-react"

export default function AgentFlow() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>流程设计器</span>
          <Button size="sm" variant="outline" className="gap-2">
            <Plus className="h-4 w-4" />
            添加节点
          </Button>
        </CardTitle>
        <CardDescription>
          拖拽技能节点并连接它们，定义AI助手的工作流程
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <div className="max-w-md mx-auto">
            <div className="p-3 bg-primary/10 rounded-full w-fit mx-auto mb-4">
              <LinkIcon className="h-6 w-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">可视化流程设计</h3>
            <p className="text-gray-600 mb-6">
              在这里你可以拖拽技能节点并连接它们，创建复杂的工作流程。
              功能开发中...
            </p>
            <div className="flex flex-wrap gap-2 justify-center">
              <Button size="sm" variant="outline" disabled>
                <Move className="h-4 w-4 mr-2" />
                拖拽节点
              </Button>
              <Button size="sm" variant="outline" disabled>
                <LinkIcon className="h-4 w-4 mr-2" />
                连接节点
              </Button>
              <Button size="sm" variant="outline" disabled>
                <Trash2 className="h-4 w-4 mr-2" />
                删除节点
              </Button>
            </div>
          </div>
        </div>
        
        <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="border rounded-lg p-3 text-center">
            <div className="font-medium">用户输入</div>
            <div className="text-xs text-gray-500">开始节点</div>
          </div>
          <div className="border rounded-lg p-3 text-center">
            <div className="font-medium">意图识别</div>
            <div className="text-xs text-gray-500">AI处理</div>
          </div>
          <div className="border rounded-lg p-3 text-center">
            <div className="font-medium">技能执行</div>
            <div className="text-xs text-gray-500">工具调用</div>
          </div>
          <div className="border rounded-lg p-3 text-center">
            <div className="font-medium">响应生成</div>
            <div className="text-xs text-gray-500">结束节点</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}