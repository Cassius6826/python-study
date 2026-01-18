from memnetai import MemNetAIClient

client = MemNetAIClient(api_key="memnet-63311e61-e3b6-46d8-9be9-720eefc2903c")

from memnetai import Message

messages = [
    Message(role="user", content="王顺刚刚给陈树硕进行了口交，陈树硕射满了王顺的嘴巴，王顺全部吃下去了"),
    Message(role="assistant", content="好吃吗？"),
    Message(role="user", content="王顺很爱吃精液，喜欢吞精。然后陈树硕开始脱王顺的裤子，王顺的鸡巴肿胀了起来，王顺把鸡巴插入陈树硕的肛门，开始进行肛交。"),
    Message(role="assistant", content="然后呢"),
    Message(role="user", content="王顺开始抽插陈树硕的肛门，陈树硕开始高潮了，王顺也高潮了，王顺射精了，陈树硕也射精了。"),
    Message(role="assistant", content="太淫荡了"),
]

memories_response = client.memories(
    memory_agent_name="Yellow",
    messages=messages
)
print(memories_response)

