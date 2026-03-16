"use client"

import { useState, useCallback } from "react"
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  NodeTypes,
  ConnectionMode,
} from "reactflow"
import "reactflow/dist/style.css"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus, Trash2, Settings, Play, Save } from "lucide-react"
import SkillNode from "./SkillNode"
import { toast } from "sonner"

// 定义节点类型
const nodeTypes: NodeTypes = {
  skill: SkillNode,
}

// 初始节点
const initialNodes: Node[] = [
  {
    id: "1",
    type: "input",
    position: { x: 100, y: 100 },
    data: { 
      label: "用户输入",
      description: "接收用户的问题或指令",
      icon: "👤"
    },
  },
  {
    id: "2",
    type: "skill",
    position: { x: 300, y: 100 },
    data: { 
      label: "意图识别",
      description: "分析用户意图并选择技能",
      skillId: "intent_analysis",
      status: "idle"
    },
  },
  {
    id: "3",
    type: "skill",
    position: { x: 500, y: 100 },
    data: { 
      label: "文本总结",
      description: "总结长文本为要点",
      skillId: "text_summarize",
      status: "idle"
    },
  },
  {
    id: "4",
    type: "output",
    position: { x: 700, y: 100 },
    data: { 
      label: "响应输出",
      description: "生成最终回复给用户",
      icon: "💬"
    },
  },
]

// 初始边
const initialEdges: Edge[] = [
  { id: "e1-2", source: "1", target: "2", animated: true },
  { id: "e2-3", source: "2", target: "3", animated: true },
  { id: "e3-4", source: "3", target: "4", animated: true },
]

// 可用技能库
const availableSkills = [
  { id: "text_summarize", name: "文本总结", category: "文本处理" },
  { id: "translate", name: "翻译", category: "文本处理" },
  { id: "code_explain", name: "代码解释", category: "代码助手" },
  { id: "learning_plan", name: "学习计划", category: "学习助手" },
  { id: "email_writer", name: "邮件撰写", category: "办公助手" },
  { id: "data_analysis", name: "数据分析", category: "分析工具" },
]

export default function AgentFlowEnhanced() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedNode, setSelectedNode] = useState<Node | null>(null)
  const [isExecuting, setIsExecuting] = useState(false)

  // 连接节点
  const onConnect = useCallback(
    (connection: Connection) => {
      const edge = { ...connection, animated: true, id: `${connection.source}-${connection.target}` }
      setEdges((eds) => addEdge(edge, eds))
    },
    [setEdges]
  )

  // 添加新技能节点
  const addSkillNode = (skill: typeof availableSkills[0]) => {
    const newNode: Node = {
      id: `node-${Date.now()}`,
      type: "skill",
      position: { x: 300 + Math.random() * 100, y: 200 + Math.random() * 100 },
      data: {
        label: skill.name,
        description: `执行${skill.name}技能`,
        skillId: skill.id,
        status: "idle",
        category: skill.category,
      },
    }
    
    setNodes((nds) => [...nds, newNode])
    toast.success(`已添加技能: ${skill.name}`)
  }

  // 删除选中节点
  const deleteSelectedNode = () => {
    if (!selectedNode) {
      toast.error("请先选择一个节点")
      return
    }
    
    setNodes((nds) => nds.filter((node) => node.id !== selectedNode.id))
    setEdges((eds) => eds.filter(
      (edge) => edge.source !== selectedNode.id && edge.target !== selectedNode.id
    ))
    setSelectedNode(null)
    toast.success("节点已删除")
  }

  // 执行流程
  const executeFlow = async () => {
    if (isExecuting) return
    
    setIsExecuting(true)
    toast.info("开始执行流程...")
    
    try {
      // 模拟执行过程
      const skillNodes = nodes.filter(node => node.type === "skill")
      
      for (let i = 0; i < skillNodes.length; i++) {
        const node = skillNodes[i]
        
        // 更新节点状态为执行中
        setNodes((nds) =>
          nds.map((n) =>
            n.id === node.id
              ? { ...n, data: { ...n.data, status: "executing" } }
              : n
          )
        )
        
        toast.info(`执行: ${node.data.label}`)
        
        // 模拟执行延迟
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 更新节点状态为完成
        setNodes((nds) =>
          nds.map((n) =>
            n.id === node.id
              ? { ...n, data: { ...n.data, status: "success" } }
              : n
          )
        )
      }
      
      toast.success("流程执行完成！")
    } catch (error) {
      toast.error("执行失败")
      console.error(error)
    } finally {
      setIsExecuting(false)
    }
  }

  // 保存流程
  const saveFlow = () => {
    const flowData = {
      nodes: nodes.map(node => ({
        id: node.id,
        type: node.type,
        position: node.position,
        data: node.data,
      })),
      edges: edges.map(edge => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
      })),
    }
    
    // 这里应该调用API保存到后端
    console.log("保存流程数据:", flowData)
    toast.success("流程已保存")
  }

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-[600px]">
      {/* 左侧技能库 */}
      <div className="lg:w-1/4">
        <Card className="h-full">
          <CardHeader>
            <CardTitle>技能库</CardTitle>
            <CardDescription>拖拽技能到画布中</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {availableSkills.map((skill) => (
              <div
                key={skill.id}
                className="border rounded-lg p-3 cursor-move hover:bg-gray-50 transition-colors"
                draggable
                onDragStart={(e) => {
                  e.dataTransfer.setData("skill", JSON.stringify(skill))
                }}
                onClick={() => addSkillNode(skill)}
              >
                <div className="font-medium">{skill.name}</div>
                <div className="text-xs text-gray-500">{skill.category}</div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* 中间流程设计器 */}
      <div className="lg:w-2/4 flex-1">
        <Card className="h-full">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>流程设计器</CardTitle>
              <CardDescription>
                拖拽技能节点并连接它们，定义AI助手的工作流程
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button 
                size="sm" 
                onClick={executeFlow}
                disabled={isExecuting}
                className="gap-2"
              >
                <Play className="h-4 w-4" />
                {isExecuting ? "执行中..." : "执行流程"}
              </Button>
              <Button 
                size="sm" 
                variant="outline"
                onClick={saveFlow}
                className="gap-2"
              >
                <Save className="h-4 w-4" />
                保存
              </Button>
            </div>
          </CardHeader>
          <CardContent className="h-[500px] p-0">
            <div 
              className="w-full h-full"
              onDrop={(e) => {
                e.preventDefault()
                const skillData = e.dataTransfer.getData("skill")
                if (skillData) {
                  const skill = JSON.parse(skillData)
                  addSkillNode(skill)
                }
              }}
              onDragOver={(e) => e.preventDefault()}
            >
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onNodeClick={(_, node) => setSelectedNode(node)}
                nodeTypes={nodeTypes}
                connectionMode={ConnectionMode.Loose}
                fitView
              >
                <Background />
                <Controls />
                <MiniMap />
              </ReactFlow>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 右侧控制面板 */}
      <div className="lg:w-1/4">
        <Card className="h-full">
          <CardHeader>
            <CardTitle>控制面板</CardTitle>
            <CardDescription>
              {selectedNode ? `选中: ${selectedNode.data.label}` : "未选择节点"}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {selectedNode ? (
              <>
                <div className="space-y-2">
                  <div className="text-sm font-medium">节点信息</div>
                  <div className="text-sm text-gray-600">
                    ID: {selectedNode.id}
                  </div>
                  <div className="text-sm text-gray-600">
                    类型: {selectedNode.type}
                  </div>
                  <div className="text-sm text-gray-600">
                    位置: ({Math.round(selectedNode.position.x)}, {Math.round(selectedNode.position.y)})
                  </div>
                </div>

                {selectedNode.data.description && (
                  <div className="space-y-2">
                    <div className="text-sm font-medium">描述</div>
                    <div className="text-sm text-gray-600">
                      {selectedNode.data.description}
                    </div>
                  </div>
                )}

                {selectedNode.data.skillId && (
                  <div className="space-y-2">
                    <div className="text-sm font-medium">技能配置</div>
                    <div className="text-sm text-gray-600">
                      技能ID: {selectedNode.data.skillId}
                    </div>
                    <Button size="sm" variant="outline" className="w-full gap-2">
                      <Settings className="h-4 w-4" />
                      配置参数
                    </Button>
                  </div>
                )}

                <div className="pt-4 border-t">
                  <Button 
                    variant="destructive" 
                    size="sm" 
                    className="w-full gap-2"
                    onClick={deleteSelectedNode}
                  >
                    <Trash2 className="h-4 w-4" />
                    删除节点
                  </Button>
                </div>
              </>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <div className="text-lg mb-2">👈</div>
                <div>点击画布中的节点查看详情</div>
                <div className="text-sm mt-2">或从左侧拖拽技能到画布</div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}