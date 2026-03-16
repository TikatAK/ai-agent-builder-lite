"use client"

import { memo } from "react"
import { Handle, Position, NodeProps } from "reactflow"
import { cn } from "@/lib/utils"
import { 
  FileText, 
  Code, 
  Brain, 
  Mail, 
  BarChart3,
  Globe,
  CheckCircle,
  PlayCircle,
  Clock
} from "lucide-react"

// 技能图标映射
const skillIcons: Record<string, React.ReactNode> = {
  "文本处理": <FileText className="h-5 w-5" />,
  "代码助手": <Code className="h-5 w-5" />,
  "学习助手": <Brain className="h-5 w-5" />,
  "办公助手": <Mail className="h-5 w-5" />,
  "分析工具": <BarChart3 className="h-5 w-5" />,
  "翻译": <Globe className="h-5 w-5" />,
  default: <Brain className="h-5 w-5" />,
}

// 状态图标映射
const statusIcons: Record<string, React.ReactNode> = {
  idle: <Clock className="h-3 w-3 text-gray-400" />,
  executing: <PlayCircle className="h-3 w-3 text-blue-500 animate-pulse" />,
  success: <CheckCircle className="h-3 w-3 text-green-500" />,
  error: <div className="h-3 w-3 rounded-full bg-red-500" />,
}

// 状态颜色映射
const statusColors: Record<string, string> = {
  idle: "border-gray-300 bg-white",
  executing: "border-blue-300 bg-blue-50",
  success: "border-green-300 bg-green-50",
  error: "border-red-300 bg-red-50",
}

export default memo(function SkillNode({ data }: NodeProps) {
  const status = data.status || "idle"
  const category = data.category || "default"
  
  return (
    <div className={cn(
      "px-4 py-3 rounded-lg border-2 shadow-sm min-w-[180px]",
      statusColors[status]
    )}>
      {/* 输入句柄 */}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 !bg-gray-400"
      />
      
      {/* 节点内容 */}
      <div className="flex items-start gap-3">
        <div className={cn(
          "p-2 rounded-md",
          status === "executing" ? "bg-blue-100" : 
          status === "success" ? "bg-green-100" : "bg-gray-100"
        )}>
          {skillIcons[category] || skillIcons.default}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-1">
            <div className="font-semibold text-sm truncate">
              {data.label}
            </div>
            <div className="flex items-center gap-1">
              {statusIcons[status]}
            </div>
          </div>
          
          {data.description && (
            <div className="text-xs text-gray-600 truncate mb-2">
              {data.description}
            </div>
          )}
          
          {data.skillId && (
            <div className="text-xs text-gray-500">
              ID: {data.skillId}
            </div>
          )}
          
          {/* 状态标签 */}
          <div className="mt-2">
            <div className={cn(
              "text-xs px-2 py-1 rounded-full inline-block",
              status === "idle" && "bg-gray-100 text-gray-600",
              status === "executing" && "bg-blue-100 text-blue-600",
              status === "success" && "bg-green-100 text-green-600",
              status === "error" && "bg-red-100 text-red-600",
            )}>
              {status === "idle" && "等待执行"}
              {status === "executing" && "执行中"}
              {status === "success" && "执行成功"}
              {status === "error" && "执行失败"}
            </div>
          </div>
        </div>
      </div>
      
      {/* 输出句柄 */}
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 !bg-gray-400"
      />
    </div>
  )
})