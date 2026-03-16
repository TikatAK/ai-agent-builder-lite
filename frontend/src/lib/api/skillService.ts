/**
 * 技能API服务
 * 提供技能执行、配置和管理的API调用
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// 技能执行请求接口
export interface SkillExecutionRequest {
  skill_id: string
  input_text: string
  parameters?: Record<string, any>
  temperature?: number
  max_tokens?: number
}

// 技能执行响应接口
export interface SkillExecutionResponse {
  success: boolean
  output: string
  skill_used?: string
  execution_time?: number
  error?: string
}

// 技能配置接口
export interface SkillConfig {
  id: string
  name: string
  description: string
  type: string
  parameters: Record<string, SkillParameter>
  example_input?: string
  example_output?: string
}

// 技能参数接口
export interface SkillParameter {
  type: string
  default?: any
  required?: boolean
  description: string
  options?: string[]
  min?: number
  max?: number
  step?: number
}

// 技能列表响应接口
export interface SkillListResponse {
  skills: SkillConfig[]
  total: number
  skill_types: string[]
}

class SkillService {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || API_BASE_URL
    this.loadToken()
  }

  // 加载token
  private loadToken() {
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token')
    }
  }

  // 获取请求头
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }
    
    return headers
  }

  // 处理API响应
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `API请求失败: ${response.status}`)
    }
    
    return response.json()
  }

  /**
   * 执行单个技能
   */
  async executeSkill(request: SkillExecutionRequest): Promise<SkillExecutionResponse> {
    const response = await fetch(`${this.baseUrl}/skill-execution/execute`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(request),
    })
    
    return this.handleResponse<SkillExecutionResponse>(response)
  }

  /**
   * 批量执行多个技能
   */
  async executeSkillsBatch(requests: SkillExecutionRequest[]): Promise<SkillExecutionResponse[]> {
    const response = await fetch(`${this.baseUrl}/skill-execution/execute/batch`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(requests),
    })
    
    return this.handleResponse<SkillExecutionResponse[]>(response)
  }

  /**
   * 获取所有可用技能列表
   */
  async listSkills(skillType?: string): Promise<SkillListResponse> {
    const url = new URL(`${this.baseUrl}/skill-execution/list`)
    if (skillType) {
      url.searchParams.append('skill_type', skillType)
    }
    
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: this.getHeaders(),
    })
    
    return this.handleResponse<SkillListResponse>(response)
  }

  /**
   * 获取特定技能详情
   */
  async getSkillDetail(skillId: string): Promise<SkillConfig> {
    const response = await fetch(`${this.baseUrl}/skill-execution/${skillId}`, {
      method: 'GET',
      headers: this.getHeaders(),
    })
    
    return this.handleResponse<SkillConfig>(response)
  }

  /**
   * 测试技能执行（不保存历史）
   */
  async testSkillExecution(request: SkillExecutionRequest): Promise<any> {
    const response = await fetch(`${this.baseUrl}/skill-execution/test`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(request),
    })
    
    return this.handleResponse(response)
  }

  /**
   * 获取技能执行历史
   */
  async getExecutionHistory(limit: number = 10, offset: number = 0): Promise<any[]> {
    const url = new URL(`${this.baseUrl}/skill-execution/history`)
    url.searchParams.append('limit', limit.toString())
    url.searchParams.append('offset', offset.toString())
    
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: this.getHeaders(),
    })
    
    return this.handleResponse<any[]>(response)
  }

  /**
   * 保存技能配置
   */
  async saveSkillConfig(skillId: string, config: any): Promise<void> {
    // TODO: 实现保存到后端的逻辑
    // 目前先保存到localStorage
    if (typeof window !== 'undefined') {
      const key = `skill_config_${skillId}`
      localStorage.setItem(key, JSON.stringify(config))
    }
    
    // 模拟API调用
    return Promise.resolve()
  }

  /**
   * 加载技能配置
   */
  async loadSkillConfig(skillId: string): Promise<any> {
    // TODO: 实现从后端加载的逻辑
    // 目前先从localStorage加载
    if (typeof window !== 'undefined') {
      const key = `skill_config_${skillId}`
      const config = localStorage.getItem(key)
      return config ? JSON.parse(config) : null
    }
    
    return null
  }

  /**
   * 获取技能统计信息
   */
  async getSkillStats(): Promise<{
    total_skills: number
    total_executions: number
    success_rate: number
    avg_execution_time: number
  }> {
    const response = await fetch(`${this.baseUrl}/skill-execution/stats`, {
      method: 'GET',
      headers: this.getHeaders(),
    })
    
    return this.handleResponse(response)
  }

  /**
   * 搜索技能
   */
  async searchSkills(query: string): Promise<SkillConfig[]> {
    const response = await fetch(`${this.baseUrl}/skill-execution/search?q=${encodeURIComponent(query)}`, {
      method: 'GET',
      headers: this.getHeaders(),
    })
    
    return this.handleResponse<SkillConfig[]>(response)
  }

  /**
   * 创建自定义技能
   */
  async createCustomSkill(skillData: Partial<SkillConfig>): Promise<SkillConfig> {
    const response = await fetch(`${this.baseUrl}/skill-execution/custom`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(skillData),
    })
    
    return this.handleResponse<SkillConfig>(response)
  }

  /**
   * 更新技能
   */
  async updateSkill(skillId: string, skillData: Partial<SkillConfig>): Promise<SkillConfig> {
    const response = await fetch(`${this.baseUrl}/skill-execution/${skillId}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(skillData),
    })
    
    return this.handleResponse<SkillConfig>(response)
  }

  /**
   * 删除技能
   */
  async deleteSkill(skillId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/skill-execution/${skillId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    })
    
    if (!response.ok) {
      throw new Error(`删除技能失败: ${response.status}`)
    }
  }
}

// 创建单例实例
export const skillService = new SkillService()

// 导出类型
export type {
  SkillExecutionRequest,
  SkillExecutionResponse,
  SkillConfig,
  SkillParameter,
  SkillListResponse,
}

export default skillService