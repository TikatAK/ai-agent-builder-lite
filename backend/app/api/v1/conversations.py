from fastapi import APIRouter

router = APIRouter(tags=["conversations"])

@router.get("/")
async def list_conversations():
    """获取对话列表"""
    return {"message": "对话列表功能开发中"}

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """获取单个对话"""
    return {"message": f"获取对话 {conversation_id} 功能开发中"}

@router.post("/{conversation_id}/messages")
async def send_message(conversation_id: str):
    """发送消息"""
    return {"message": f"发送消息到对话 {conversation_id} 功能开发中"}